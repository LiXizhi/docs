```javascript



'use strict';

const Controller = require('egg').Controller;

const suggestions_rule = {
  prefix: 'string',
};

const bulk_rule = {
  body: 'array',
};

const score_field = '_score';
const updated_at_field = 'updated_at';
const desc_sort = 'desc';

class baseController extends Controller {
  add_location(payload, data_type, index_only) {
    const { index, type } = this.config.elasticsearch.locations[data_type];
    payload.index = index;
    if (!index_only) { payload.type = type; }
    return payload;
  }

  async index() {
    await this.search();
  }

  async search(DSL = this.get_search_DSL()) {
    const { ctx, service } = this;
    const [ from, size ] = ctx.helper.paginate(ctx.query);
    const query = { from, size, body: DSL };
    const query_with_location = this.add_location(query);
    const result = await service.es.client.search(query_with_location)
      .catch(err => this.error(err));
    ctx.body = this.wrap_search_result(result);
  }

  async show() {
    const { ctx, service } = this;
    ctx.ensureAdmin();
    const query = { id: ctx.params.id };
    const query_with_location = this.add_location(query);
    const res = await service.es.client.get(query_with_location)
      .catch(err => this.error(err));
    ctx.body = res._source;
  }

  async create(payload) {
    const { ctx, service } = this;
    ctx.ensureAdmin();
    const payload_with_location = this.add_location(payload);
    await service.es.client.create(payload_with_location)
      .catch(err => this.error(err));
    this.created();
  }

  async update(payload) {
    const { ctx, service } = this;
    ctx.ensureAdmin();
    const payload_with_location = this.add_location(payload);
    await service.es.client.update(payload_with_location)
      .catch(err => this.error(err));
    this.updated();
  }

  async upsert(payload) {
    const { ctx, service } = this;
    ctx.ensureAdmin();
    const payload_with_location = this.add_location(payload);
    await service.es.client.index(payload_with_location)
      .catch(err => this.error(err));
    this.upserted();
  }

  async destroy() {
    const { ctx, service } = this;
    ctx.ensureAdmin();
    const query = { id: ctx.params.id };
    const query_with_location = this.add_location(query);
    await service.es.client.delete(query_with_location)
      .catch(err => this.error(err));
    this.deleted();
  }

  async bulk() {
    const { ctx, service } = this;
    ctx.validate(bulk_rule);
    ctx.ensureAdmin();
    const params = {
      body: ctx.params.body,
      type: ctx.params.type,
      index: ctx.params.index,
    };
    const response = await service.es.client.bulk(params)
      .catch(err => this.error(err));
    ctx.body = response;
  }

  add_highlight_DSL(DSL, ... fields) {
    const tag = this.config.highlight_tag;
    if (fields.length > 0) {
      DSL.highlight = {
        fields: {},
        pre_tags: `<${tag}>`,
        post_tags: `</${tag}>`,
      };
      for (const field of fields) {
        DSL.highlight.fields[field] = {};
      }
    }
    return DSL;
  }

  get max_expansions() {
    const { ctx } = this;
    const query_length = ctx.query.q;
    let max_expansions;
    switch (true) {
      case query_length > 36:
        max_expansions = 10;
        break;
      case query_length > 12:
        max_expansions = Math.floor(query_length / 4) + 1;
        break;
      case query_length > 3:
        max_expansions = Math.floor(query_length / 3);
        break;
      default:
        max_expansions = 1;
        break;
    }
    return max_expansions;
  }

  // method to add sorting condition into search DSL
  add_sort_DSL(DSL = {}, field = this.ctx.query.sort, order = this.ctx.query.order) {
    if (field) {
      DSL.sort = DSL.sort || [];
      DSL.sort.push({
        [field]: { order: order || desc_sort },
      });
    }
    return DSL;
  }

  add_multi_sort_DSL(DSL = {}, fields) {
    const { ctx } = this;
    if (!DSL.sort) {
      DSL = this.add_sort_DSL(
        DSL,
        ctx.query.sort,
        ctx.query.order
      );
    }

    if (!fields) {
      fields = [];
      if (ctx.query.q) fields.push(score_field);
      fields.push(updated_at_field);
    }

    for (const field of fields) {
      if (Object(field) instanceof String) {
        DSL = this.add_sort_DSL(DSL, field);
      } else if (field instanceof Object) {
        for (const name in field) {
          const order = field[name];
          DSL = this.add_sort_DSL(DSL, field, order);
        }
      }
    }
    return DSL;
  }

  get invisible_DSL() {
    return { term: { visibility: 'private' } };
  }

  // api for ranking such as hot, latest, etc
  async rank(field, order = desc_sort) {
    const DSL = this.get_rank_DSL(field, order);
    await this.search(DSL);
  }

  get_rank_DSL(field, order) {
    const DSL = this.add_sort_DSL({}, field, order);
    return DSL;
  }

  // api for query words suggestion
  async suggest() {
    const { ctx, service } = this;
    ctx.validate(suggestions_rule, ctx.query);
    const query = {
      body: {
        suggestions: {
          prefix: ctx.query.prefix,
          completion: {
            field: 'suggestions',
            size: Number(ctx.query.size) || 5,
          },
        },
      },
      index: 'suggestions',
    };
    const result = await service.es.client.suggest(query)
      .catch(err => this.error(err));
    ctx.body = this.wrap_suggestions(result);
  }

  async save_suggestions(...keywords) {
    const { ctx, service } = this;
    const tasks = [];
    const already_exist = {};
    for (const keyword of keywords) {
      if (!keyword || already_exist[keyword]) { continue; }
      already_exist[keyword] = true;
      const pinyin = ctx.helper.hanzi_to_pinyin(keyword);
      tasks.push(service.es.client.create({
        index: 'suggestions',
        type: 'suggestions',
        id: ctx.helper.to_sha1(keyword),
        body: {
          keyword,
          pinyin,
          suggestions: [ keyword, pinyin ],
        },
      }).catch(err => {
        if (err.statusCode !== 409) {
          ctx.logger.error(err);
        }
      }));
    }
    await Promise.all(tasks).catch();
  }

  wrap_suggestions(result) {
    return result.suggestions[0].options.map(suggestion => {
      suggestion._source.hit = suggestion.text;
      return suggestion._source;
    });
  }

  success(action = 'success') {
    const { ctx } = this;
    ctx.body = {};
    ctx.body[action] = true;
  }

  created() {
    const { ctx } = this;
    ctx.status = 201;
    this.success('created');
  }

  updated() {
    this.success('updated');
  }

  upserted() {
    this.success('upserted');
  }


  deleted() {
    this.success('deleted');
  }

  moved() {
    this.success('moved');
  }

  error(err) {
    const { ctx } = this;
    ctx.logger.error(err);
    ctx.throw(err.statusCode);
  }
}

module.exports = baseController;



'use strict';

const Controller = require('egg').Controller;

class HomeController extends Controller {
  async index() {
    this.ctx.body = 'hi, es-gateway';
  }
}

module.exports = HomeController;



'use strict';

const Controller = require('./base');

const create_rule = {
  id: 'int',
  title: 'string',
  prize: { type: 'int', required: false },
  total_lessons: { type: 'int', required: false },
  description: { type: 'string', required: false, allowEmpty: true },
  age_min: { type: 'int', required: false },
  age_max: { type: 'int', required: false },
  created_at: 'string',
  updated_at: { type: 'string', required: false },
};

const update_rule = {
  title: { type: 'string', required: false },
  prize: { type: 'int', required: false },
  total_lessons: { type: 'int', required: false },
  description: { type: 'string', required: false, allowEmpty: true },
  recent_view: { type: 'int', required: false },
  age_min: { type: 'int', required: false },
  age_max: { type: 'int', required: false },
  updated_at: 'string',
};

const upsert_rule = {
  title: 'string',
  prize: { type: 'int', required: false },
  total_lessons: { type: 'int', required: false },
  description: { type: 'string', required: false, allowEmpty: true },
  age_min: { type: 'int', required: false },
  age_max: { type: 'int', required: false },
  recent_view: { type: 'int', required: false },
  created_at: 'string',
  updated_at: { type: 'string', required: false },
};

class PackageController extends Controller {
  async hots() {
    await this.rank('recent_view');
  }

  async create() {
    const { ctx } = this;
    ctx.validate(create_rule, ctx.params);
    const id = ctx.params.id;
    const data = ctx.params.permit(
      'id', 'title', 'cover', 'total_lessons', 'prize',
      'description', 'age_min', 'age_max', 'created_at',
      'updated_at'
    );
    data.updated_at = data.updated_at || data.created_at;
    const payload = { id, body: data };
    await super.create(payload);
    this.save_suggestions(data.title);
  }

  async update() {
    const { ctx } = this;
    ctx.validate(update_rule, ctx.params);
    const id = ctx.params.id;
    const doc = ctx.params.permit(
      'title', 'cover', 'total_lessons', 'prize',
      'description', 'recent_view', 'age_min', 'age_max',
      'updated_at'
    );
    const data = { doc };
    const payload = { id, body: data };
    await super.update(payload);
    if (doc.title) { this.save_suggestions(doc.title); }
  }

  async upsert() {
    const { ctx } = this;
    ctx.validate(upsert_rule, ctx.params);
    const id = ctx.params.id;
    const data = ctx.params.permit(
      'title', 'cover', 'total_lessons', 'description', 'prize',
      'age_min', 'age_max', 'recent_view', 'created_at', 'updated_at'
    );
    data.updated_at = data.updated_at || data.created_at;
    const payload = { id, body: data };
    await super.upsert(payload);
    this.save_suggestions(data.title);
  }

  add_location(payload) {
    const data_type = 'package';
    return super.add_location(payload, data_type);
  }

  get_search_DSL() {
    const DSL = {};
    this.add_query_DSL(DSL);
    this.add_highlight_DSL(DSL, 'title', 'description');
    this.add_multi_sort_DSL(DSL);
    return DSL;
  }

  add_query_DSL(DSL) {
    DSL.query = { bool: {
      should: this.get_should_query(),
    } };
    return DSL;
  }

  get_should_query() {
    const { ctx, max_expansions } = this;
    const q = ctx.query.q;
    let should;
    if (q) {
      should = [
        { term: { 'title.keyword': { value: this.ctx.query.q, boost: 3 } } },
        { prefix: { username: { value: this.ctx.query.q, boost: 2 } } },
        { multi_match: {
          fields: [ 'title', 'description' ], query: this.ctx.query.q,
          type: 'phrase_prefix', max_expansions,
        } },
        { wildcard: { title: `*${this.ctx.query.q}*` } },
      ];
    }
    return should;
  }

  wrap_search_result(result) {
    return {
      hits: result.hits.hits.map(hit => {
        hit._source.id = Number(hit._id);
        hit._source._score = hit._score;
        hit._source.highlight = hit.highlight;
        hit._source.suggestions = undefined;
        return hit._source;
      }),
      total: result.hits.total,
    };
  }
}

module.exports = PackageController;



'use strict';

const Controller = require('./base');

const create_rule = {
  id: 'string',
  url: 'string',
  site: 'string',
  username: 'string',
  title: 'string',
  visibility: [ 'public', 'private' ],
  content: 'string',
  created_at: 'string',
};

const update_rule = {
  url: { type: 'string', required: false, allowEmpty: true },
  title: { type: 'string', required: false, allowEmpty: true },
  visibility: {
    type: 'enum',
    values: [ 'public', 'private' ],
    required: false,
  },
  content: { type: 'string', required: false, allowEmpty: true },
  updated_at: 'string',
};

const delete_site_rule = {
  sitename: 'string',
  username: 'string',
};

const update_site_visibility_rule = {
  sitename: 'string',
  username: 'string',
  visibility: [ 'public', 'private' ],
};

class PagesController extends Controller {
  async create() {
    const { ctx } = this;
    ctx.validate(create_rule, ctx.params);
    const id = ctx.params.id;
    const body = ctx.params.permit(
      'id', 'url', 'site', 'username', 'title', 'visibility',
      'content', 'created_at', 'updated_at'
    );
    body.updated_at = body.updated_at || body.created_at;
    const payload = { id, body };
    await super.create(payload);
    this.save_suggestions(body.title);
  }

  async update() {
    const { ctx } = this;
    ctx.validate(update_rule, ctx.params);
    const id = ctx.params.id;
    const doc = ctx.params.permit(
      'url', 'title', 'visibility', 'content', 'updated_at'
    );
    const body = { doc };
    const payload = { id, body };
    await super.update(payload);
    if (doc.title) this.save_suggestions(doc.title);
  }

  async destroy_site() {
    const { ctx, service } = this;
    ctx.ensureAdmin();
    ctx.validate(delete_site_rule, ctx.params);
    const query = { body: this.get_site_DSL() };
    const query_with_location = this.add_location(query);
    const response = await service.es.client
      .deleteByQuery(query_with_location)
      .catch(err => this.error(err));
    ctx.body = response;
  }

  async update_visibility() {
    const { ctx, service } = this;
    ctx.ensureAdmin();
    ctx.validate(update_site_visibility_rule, ctx.params);
    const query = { body: this.get_update_visibility_DSL() };
    const query_with_location = this.add_location(query);
    const response = await service.es.client
      .updateByQuery(query_with_location)
      .catch(err => this.error(err));
    ctx.body = response;
  }

  get_site_DSL() {
    const DSL = {};
    this.add_site_query_DSL(DSL);
    return DSL;
  }

  get_update_visibility_DSL() {
    const DSL = this.get_site_DSL();
    this.add_update_visibility_DSL(DSL);
    return DSL;
  }

  add_update_visibility_DSL(DSL) {
    const { ctx } = this;
    DSL.script = {
      source: `ctx._source.visibility = "${ctx.params.visibility}"`,
      lang: 'painless',
    };
    return DSL;
  }

  add_site_query_DSL(DSL) {
    const { ctx } = this;
    const site = ctx.params.sitename;
    const username = ctx.params.username;
    DSL.query = {
      bool: {
        must: [
          { term: { username } },
          { term: { site } },
        ],
      },
    };
    return DSL;
  }

  get_search_DSL() {
    const DSL = {};
    this.add_query_DSL(DSL);
    this.add_highlight_DSL(DSL, 'title', 'url', 'content');
    this.add_multi_sort_DSL(DSL);
    return DSL;
  }

  add_query_DSL(DSL = {}) {
    DSL.query = { bool: {
      should: this.get_should_query(),
      must_not: this.invisible_DSL,
    } };
    return DSL;
  }

  get_should_query() {
    const { ctx, max_expansions } = this;
    const q = ctx.query.q;
    if (q) {
      const should = [
        { term: { 'title.keyword': { value: q, boost: 3 } } },
        { match_phrase: { content: { query: q } } },
        { match_phrase_prefix: { title: { query: q, max_expansions } } },
        { match_phrase_prefix: { url: { query: q, max_expansions } } },
      ];

      if (q.includes(' ')) {
        const filtered = ctx.helper.filterSubStr(q, ' ');
        should.push({ match_phrase: { content: { query: filtered } } });
      }
      return should;
    }
  }

  wrap_search_result(result) {
    return {
      hits: result.hits.hits.map(hit => {
        hit._source._score = hit._score;
        hit._source.highlight = hit.highlight;
        hit._source.id = undefined;
        return hit._source;
      }),
      total: result.hits.total,
    };
  }

  add_location(payload) {
    const data_type = 'page';
    return super.add_location(payload, data_type);
  }

  async index() {
    if (!this.ctx.params.q) {
      this.ctx.body = {
        total: 0,
        hits: [],
      };
      return;
    }
    await this.search();
  }
}

module.exports = PagesController;



'use strict';

const Controller = require('./base');

const create_rule = {
  id: 'int',
  name: 'string',
  username: 'string',
  visibility: [ 'public', 'private' ],
  type: 'string',
  recruiting: 'bool',
  description: { type: 'string', required: false, allowEmpty: true },
  tags: { type: 'array', itemType: 'string', required: false },
  sys_tags: { type: 'array', itemType: 'string', required: false },
  created_at: 'string',
};

const update_rule = {
  name: { type: 'string', required: false },
  visibility: { type: 'enum', values: [ 'public', 'private' ], required: false },
  description: { type: 'string', required: false, allowEmpty: true },
  type: { type: 'string', required: false },
  recruiting: { type: 'boolean', required: false },
  recommended: { type: 'boolean', required: false },
  tags: { type: 'array', itemType: 'string', required: false },
  sys_tags: { type: 'array', itemType: 'string', required: false },
  point: { type: 'number', required: false },
  total_like: { type: 'int', required: false },
  total_view: { type: 'int', required: false },
  total_mark: { type: 'int', required: false },
  total_comment: { type: 'int', required: false },
  recent_like: { type: 'int', required: false },
  recent_view: { type: 'int', required: false },
  updated_at: 'string',
};

const upsert_rule = {
  name: 'string',
  username: 'string',
  visibility: [ 'public', 'private' ],
  description: { type: 'string', required: false, allowEmpty: true },
  type: 'string',
  recruiting: 'bool',
  recommended: { type: 'bool', required: false },
  tags: { type: 'array', itemType: 'string', required: false },
  sys_tags: { type: 'array', itemType: 'string', required: false },
  point: { type: 'number', required: false },
  total_like: { type: 'int', required: false },
  total_view: { type: 'int', required: false },
  total_mark: { type: 'int', required: false },
  total_comment: { type: 'int', required: false },
  recent_like: { type: 'int', required: false },
  recent_view: { type: 'int', required: false },
  created_at: 'string',
  updated_at: { type: 'string', required: false },
};

class ProjectController extends Controller {
  async hots() {
    await this.rank('recent_view');
  }

  async likes() {
    await this.rank('recent_like');
  }

  async create() {
    const { ctx } = this;
    ctx.validate(create_rule, ctx.params);
    const id = ctx.params.id;
    const data = ctx.params.permit(
      'name', 'cover', 'username', 'user_portrait',
      'description', 'visibility', 'type', 'recruiting',
      'created_at', 'updated_at', 'id', 'tags',
      'sys_tags', 'video'
    );
    data.updated_at = data.created_at;
    const payload = { id, body: data };
    await super.create(payload);
    this.save_suggestions(data.name);
  }

  async update() {
    const { ctx } = this;
    ctx.validate(update_rule, ctx.params);
    const id = ctx.params.id;
    const doc = ctx.params.permit(
      'name', 'cover', 'user_portrait', 'visibility',
      'type', 'recruiting', 'tags', 'total_like',
      'total_view', 'total_mark', 'total_comment',
      'recent_like', 'recent_view', 'updated_at',
      'description', 'video', 'recommended', 'sys_tags',
      'point'
    );
    const data = { doc };
    const payload = { id, body: data };
    await super.update(payload);
    if (doc.name) this.save_suggestions(doc.name);
  }

  async upsert() {
    const { ctx } = this;
    ctx.validate(upsert_rule, ctx.params);
    const id = ctx.params.id;
    const data = ctx.params.permit(
      'name', 'cover', 'username', 'user_portrait', 'description',
      'visibility', 'type', 'recruiting', 'tags', 'total_like',
      'total_view', 'total_mark', 'total_comment', 'recent_like',
      'recent_view', 'video', 'id', 'recommended', 'created_at',
      'updated_at', 'sys_tags', 'point'
    );
    data.updated_at = data.updated_at || data.created_at;
    const payload = { id, body: data };
    await super.upsert(payload);
    this.save_suggestions(data.name);
  }

  add_location(payload) {
    const data_type = 'project';
    return super.add_location(payload, data_type);
  }

  get_rank_DSL(field, order) {
    const DSL = this.add_sort_DSL({}, field, order);
    DSL.query = {
      bool: { must_not: this.invisible_DSL },
    };
    return DSL;
  }

  get_search_DSL() {
    const DSL = {};
    this.add_query_DSL(DSL);
    this.add_highlight_DSL(DSL, 'id', 'name', 'username');
    this.add_multi_sort_DSL(DSL);
    return DSL;
  }

  add_query_DSL(DSL) {
    DSL.query = { bool: {
      must: this.get_must_query(),
      must_not: this.invisible_DSL,
    } };
    return DSL;
  }

  get_should_query() {
    const { ctx, max_expansions } = this;
    const q = ctx.query.q;
    let should;
    if (q) {
      should = [];
      if (Number(q)) {
        should.push({ term: { id: { value: q, boost: 5 } } });
      }
      should.push(
        { term: { 'name.keyword': { value: q, boost: 3 } } },
        { prefix: { username: { value: q, boost: 2 } } },
        { match_phrase_prefix: {
          name: { query: q, max_expansions, boost: 2 },
        } },
        { wildcard: { name: `*${q}*` } }
      );

      if (q.includes(' ')) {
        const filtered = ctx.helper.filterSubStr(q, ' ');
        should.push(
          { term: { 'name.keyword': { value: filtered, boost: 3 } } },
          { match_phrase_prefix: {
            name: { query: filtered, max_expansions, boost: 2 },
          } }
        );
      }
    }
    return should;
  }

  get_must_query() {
    const must = [];
    const should = this.get_should_query();
    const { type, tags, recruiting, recommended } = this.ctx.query;
    if (should) must.push({ bool: { should } });
    if (type) must.push({ term: { type } });
    if (tags) must.push({ term: { tags } });
    if (recruiting) must.push({ term: { recruiting: true } });
    if (recommended) must.push({ term: { recommended: true } });
    this.add_sys_tags_query(must);
    return must;
  }

  add_sys_tags_query(must) {
    const { ctx } = this;
    const { sys_tags } = this.ctx.query;
    if (sys_tags) {
      try {
        const parsed = ctx.helper.parseQuery(sys_tags);
        for (const sys_tag of parsed) {
          must.push({ term: { sys_tags: sys_tag } });
        }
      } catch (e) {
        ctx.throw(400, 'invalid sys_tags');
      }
    }
  }

  wrap_search_result(result) {
    return {
      hits: result.hits.hits.map(hit => {
        hit._source._score = hit._score;
        hit._source.id = Number(hit._source.id);
        hit._source.highlight = hit.highlight;
        hit._source.suggestions = undefined;
        return hit._source;
      }),
      total: result.hits.total,
    };
  }
}

module.exports = ProjectController;



'use strict';

const Controller = require('./base');

const create_rule = {
  id: 'int',
  username: { type: 'string', min: 4, max: 30 },
  sitename: 'string',
  cover: { type: 'string', required: false, allowEmpty: true },
  display_name: { type: 'string', required: false, allowEmpty: true },
  description: { type: 'string', required: false, allowEmpty: true },
  created_at: 'string',
};

const update_rule = {
  sitename: { type: 'string', required: false },
  cover: { type: 'string', required: false, allowEmpty: true },
  display_name: { type: 'string', required: false, allowEmpty: true },
  description: { type: 'string', required: false, allowEmpty: true },
  updated_at: 'string',
};

const upsert_rule = {
  username: { type: 'string', min: 4, max: 30 },
  sitename: 'string',
  cover: { type: 'string', required: false, allowEmpty: true },
  display_name: { type: 'string', required: false, allowEmpty: true },
  description: { type: 'string', required: false, allowEmpty: true },
  created_at: 'string',
  updated_at: { type: 'string', required: false },
};

class SiteController extends Controller {
  async create() {
    this.ctx.validate(create_rule);
    if (!this.ctx.request.body.display_name) {
      this.ctx.request.body.display_name = this.ctx.request.body.sitename;
    }
    const {
      id, username, sitename, cover,
      display_name, description, created_at,
    } = this.ctx.request.body;
    const data = {
      username, sitename, cover, display_name,
      description, created_at,
    };
    data.updated_at = created_at;
    const payload = { id, body: data };
    await super.create(payload);
    this.save_suggestions(sitename, display_name);
  }

  async update() {
    this.ctx.validate(update_rule);
    const { cover, display_name, description } = this.ctx.request.body;
    const data = { doc: { cover, display_name, description } };
    const payload = { id: this.ctx.params.id, body: data };
    await super.update(payload);
    if (display_name) { this.save_suggestions(display_name); }
  }

  async upsert() {
    this.ctx.validate(upsert_rule);
    if (!this.ctx.request.body.display_name) {
      this.ctx.request.body.display_name = this.ctx.request.body.sitename;
    }
    const {
      username, sitename, cover, display_name, description, created_at, updated_at,
    } = this.ctx.request.body;
    const data = {
      username, sitename, cover, display_name, description, created_at,
    };
    data.updated_at = updated_at || created_at;
    const payload = { id: this.ctx.params.id, body: data };
    await super.upsert(payload);
    this.save_suggestions(sitename, display_name);
  }

  add_location(payload) {
    const data_type = 'site';
    return super.add_location(payload, data_type);
  }

  get_search_DSL() {
    const DSL = { query: {} };
    if (this.ctx.query.q) {
      DSL.query.multi_match = {
        query: this.ctx.query.q,
        fields: [ 'sitename', 'display_name' ],
      };
    }
    this.add_highlight_DSL(DSL, 'sitename', 'display_name');
    this.add_sort_DSL(DSL);
    return this.add_sort_DSL(DSL);
  }

  wrap_search_result(result) {
    return {
      hits: result.hits.hits.map(hit => {
        hit._source._score = hit._score;
        hit._source.highlight = hit.highlight;
        hit._source.suggestions = undefined;
        return hit._source;
      }),
      total: result.hits.total,
    };
  }
}

module.exports = SiteController;



'use strict';

const Controller = require('./base');

const create_rule = {
  id: 'int',
  username: { type: 'string', min: 4, max: 30 },
  created_at: 'string',
};

const update_rule = {
  total_projects: { type: 'int', required: false },
  total_fans: { type: 'int', required: false },
  total_follows: { type: 'int', required: false },
  description: { type: 'string', required: false, allowEmpty: true },
  updated_at: 'string',
};

const upsert_rule = {
  username: { type: 'string', min: 4, max: 30 },
  total_projects: { type: 'int', required: false },
  total_fans: { type: 'int', required: false },
  total_follows: { type: 'int', required: false },
  description: { type: 'string', required: false, allowEmpty: true },
  created_at: 'string',
  updated_at: { type: 'string', required: false },
};

class UserController extends Controller {
  async create() {
    const { ctx } = this;
    ctx.validate(create_rule, ctx.params);
    const id = ctx.params.id;
    const data = ctx.params.permit(
      'id', 'username', 'portrait', 'nickname',
      'created_at', 'updated_at'
    );
    data.updated_at = data.updated_at || data.created_at;
    data.nickname = data.nickname || data.username;
    const payload = { id, body: data };
    await super.create(payload);
    this.save_suggestions(data.username, data.nickname);
  }

  async update() {
    const { ctx } = this;
    ctx.validate(update_rule, ctx.params);
    const id = ctx.params.id;
    const doc = ctx.params.permit(
      'nickname', 'portrait', 'total_projects', 'total_fans',
      'description', 'total_follows', 'updated_at'
    );
    const data = { doc };
    const payload = { id, body: data };
    await super.update(payload);
    if (doc.nickname) { this.save_suggestions(doc.nickname); }
  }

  async upsert() {
    const { ctx } = this;
    ctx.validate(upsert_rule, ctx.params);
    const id = ctx.params.id;
    const data = ctx.params.permit(
      'id', 'username', 'portrait', 'total_projects', 'total_fans',
      'total_follows', 'description', 'created_at', 'updated_at'
    );
    data.updated_at = data.updated_at || data.created_at;
    data.nickname = data.nickname || data.username;
    const payload = { id, body: data };
    await super.upsert(payload);
    this.save_suggestions(data.username, data.nickname);
  }

  add_location(payload) {
    const data_type = 'user';
    return super.add_location(payload, data_type);
  }

  get_search_DSL() {
    const DSL = {};
    this.add_query_DSL(DSL);
    this.add_highlight_DSL(DSL, 'username', 'nickname');
    this.add_multi_sort_DSL(DSL);
    return DSL;
  }

  add_query_DSL(DSL) {
    DSL.query = { bool: {
      should: this.get_should_query(),
    } };
    return DSL;
  }

  get_should_query() {
    const { ctx, max_expansions } = this;
    const q = ctx.query.q;
    let should;
    if (q) {
      should = [
        { term: { 'username.keyword': { value: q, boost: 3 } } },
        { prefix: { username: { value: q, boost: 2 } } },
        { multi_match: {
          fields: [ 'username', 'nickname' ], query: q,
          type: 'phrase_prefix', max_expansions,
        } },
        { wildcard: { username: `*${q}*` } },
        { wildcard: { nickname: `*${q}*` } },
      ];
    }
    return should;
  }

  wrap_search_result(result) {
    return {
      hits: result.hits.hits.map(hit => {
        hit._source.id = Number(hit._id);
        hit._source._score = hit._score;
        hit._source.suggestions = undefined;
        return hit._source;
      }),
      total: result.hits.total,
    };
  }
}

module.exports = UserController;



'use strict';

const isAdmin = user => {
  return user.roleId === 10;
};

module.exports = {
  ensureAdmin() {
    const errMsg = 'Admin Only';
    this.state = this.state || {};
    this.state.user = this.state.user || {};
    const not_permitted = !this.state.user.roleId || !isAdmin(this.state.user);
    if (not_permitted) { this.throw(401, errMsg); }
    this.user = this.state.user;
  },
};



'use strict';

const pinyin = require('pinyin');
const crypto = require('crypto');

module.exports = {
  hanzi_to_pinyin(han) {
    return pinyin(han, { style: pinyin.STYLE_NORMAL }).join('');
  },
  paginate(query) {
    const size = Number(query.per_page) || 20;
    const page = Number(query.page) || 1;
    const from = (page - 1) * size;
    return [ from, size ];
  },
  to_sha1(str) {
    const hasher = crypto.createHash('sha1');
    hasher.update(str);
    return hasher.digest('hex');
  },
  parseQuery(query) {
    return query.split('|');
  },
  filterSubStr(str, subStr) {
    const splited = str.split(subStr);
    let filtered = '';
    splited.forEach(v => {
      filtered += v;
    });
    return filtered;
  },
};



'use strict';

const jwt = require('keepwork-jwt-simple');

const get_token = ctx => {
  let token = null;
  if (ctx.headers.authorization) {
    const splited_authorization = ctx.headers.authorization.split(' ');
    if (splited_authorization[0] !== 'Bearer') { ctx.throw(401, 'Bearer token required'); }
    token = ctx.token = splited_authorization[1];
  }
  return token;
};

module.exports = config => {
  return async (ctx, next) => {
    const token = get_token(ctx);
    ctx.state = {
      get user() {
        if (!token) { ctx.throw(401, 'Authorization required'); }
        try {
          const payload = jwt.decode(token, config.secret, false, 'HS1');
          return payload;
        } catch (err) {
          ctx.throw(401, err.message);
        }
      },
    };
    return await next();
  };
};



'use strict';

const Service = require('egg').Service;
const elasticsearch = require('elasticsearch');

module.exports = app => {
  const config = app.config.elasticsearch;
  const Client = new elasticsearch.Client({
    host: config.url,
    apiVersion: config.version,
    log: config.log || 'info',
  });

  class EsService extends Service {
    get client() {
      return Client;
    }
  }

  return EsService;
};



'use strict';

/**
 * @param {Egg.Application} app - egg application
 */
module.exports = app => {
  const { router, controller } = app;
  const url_prefix = app.config.url_prefix;
  if (url_prefix) { router.prefix(url_prefix); }

  const { base, user, project, page } = controller;
  const lesson = controller.package;

  router.get('/', controller.home.index);

  router.post('/bulk', base.bulk);
  router.get('/suggestions', project.suggest);

  router.resources('/users', user);
  router.post('/users/:id/upsert', user.upsert);

  router.resources('/packages', lesson);
  router.post('/packages/:id/upsert', lesson.upsert);
  router.get('/hots/packages', lesson.hots);

  router.resources('/projects', project);
  router.post('/projects/:id/upsert', project.upsert);
  router.get('/hots/projects', project.hots);
  router.get('/likes/projects', project.likes);

  router.put('/sites/:username/:sitename/visibility', page.update_visibility);
  router.del('/sites/:username/:sitename', page.destroy_site);
  router.resources('/pages', page);

};



'use strict';

const { app } = require('egg-mock/bootstrap');

describe('test/app/test/controller/base.test.js', () => {
  it('should POST /bulk', () => {
    const body = [
      { create: { _id: 15 } },
      { username: 'test', title: 'test' },
      { delete: { _id: 13 } },
    ];
    const type = 'pages';
    const index = 'pages';
    return app.httpRequest()
      .post('/bulk')
      .set(app.auth_header)
      .send({ body, index, type })
      .expect(200);
  });
});



'use strict';

const { app, assert } = require('egg-mock/bootstrap');

describe('test/app/controller/home.test.js', () => {

  it('should assert', function* () {
    const pkg = require('../../../package.json');
    assert(app.config.keys.startsWith(pkg.name));

    // const ctx = app.mockContext({});
    // yield ctx.service.xx();
  });

  it('should GET /', () => {
    return app.httpRequest()
      .get('/')
      .expect('hi, es-gateway')
      .expect(200);
  });
});



'use strict';

const { app, assert } = require('egg-mock/bootstrap');
const faker = require('faker');

describe('test/app/controller/package.test.js', () => {
  const lessons_package = {
    id: faker.random.number(),
    title: faker.name.title(),
    prize: faker.random.number(),
    description: faker.lorem.text(),
    age_min: faker.random.number(),
    age_max: faker.random.number(),
    total_lessons: faker.random.number(),
    recent_view: faker.random.number(),
    created_at: faker.date.past(),
    updated_at: faker.date.past(),
  };

  it('should POST /packages', () => {
    return app.httpRequest()
      .post('/packages')
      .set(app.auth_header)
      .send(lessons_package)
      .expect(201);
  });

  it('should PUT /packages/:id', () => {
    return app.httpRequest()
      .put(`/packages/${lessons_package.id}`)
      .set(app.auth_header)
      .send(lessons_package)
      .expect(200);
  });

  it('should delete /packages/:id', () => {
    return app.httpRequest()
      .delete(`/packages/${lessons_package.id}`)
      .set(app.auth_header)
      .expect(200);
  });

  it('should post /packages/:id/upsert', () => {
    return app.httpRequest()
      .post(`/packages/${lessons_package.id}/upsert`)
      .set(app.auth_header)
      .send(lessons_package)
      .expect(200);
  });

  it('should get /packages', async () => {
    const res = await app.httpRequest()
      .get('/packages?q=123')
      .expect(200);

    const result = res.body;
    assert(result);
    assert(result.hits);
    assert(result.total);
  });
});



'use strict';

const { app, assert } = require('egg-mock/bootstrap');
const faker = require('faker');

describe('test/app/controller/page.test.js', () => {
  const username = faker.internet.userName();
  const sitename = faker.internet.domainName();

  const page = {
    id: faker.random.number(),
    title: faker.name.title(),
    url: faker.internet.url(),
    site: faker.internet.domainName(),
    username: faker.internet.userName(),
    visibility: faker.helpers.randomize([ 'private', 'public' ]),
    content: faker.lorem.text(),
    created_at: faker.date.past(),
    updated_at: faker.date.past(),
  };

  it('should PUT /sites/:username/:sitename/visibility', () => {
    const visibility = 'private';
    return app.httpRequest()
      .put(`/sites/${username}/${sitename}/visibility`)
      .set(app.auth_header)
      .send({ visibility })
      .expect(200);
  });

  it('should DELETE /sites/:username/:sitename', () => {
    return app.httpRequest()
      .delete(`/sites/${username}/${sitename}`)
      .set(app.auth_header)
      .expect(200);
  });

  it('should POST /pages', () => {
    return app.httpRequest()
      .post('/users')
      .set(app.auth_header)
      .send(page)
      .expect(201);
  });

  it('should PUT /pages/:id', () => {
    return app.httpRequest()
      .put(`/pages/${page.id}`)
      .set(app.auth_header)
      .send(page)
      .expect(200);
  });

  it('should delete /pages/:id', () => {
    return app.httpRequest()
      .delete(`/pages/${page.id}`)
      .set(app.auth_header)
      .expect(200);
  });

  it('should get /pages', async () => {
    const res = await app.httpRequest()
      .get('/pages?q=123')
      .expect(200);

    const result = res.body;
    assert(result);
    assert(result.hits);
    assert(result.total);
  });
});



'use strict';

const { app, assert } = require('egg-mock/bootstrap');
const faker = require('faker');

describe('test/app/controller/project.test.js', () => {
  const project = {
    id: faker.random.number(),
    name: faker.name.title(),
    username: faker.name.firstName(),
    visibility: faker.helpers.randomize([ 'public', 'private' ]),
    type: faker.helpers.randomize([ 'website', 'paracraft' ]),
    cover: faker.internet.avatar(),
    recruiting: faker.random.boolean(),
    recommended: faker.random.boolean(),
    tags: [ 'game' ],
    sys_tags: [ 'game' ],
    description: faker.lorem.text(),
    point: faker.random.number({ min: 70, max: 100 }),
    total_like: faker.random.number(),
    total_view: faker.random.number(),
    total_mark: faker.random.number(),
    total_comment: faker.random.number(),
    recent_like: faker.random.number(),
    recent_view: faker.random.number(),
    created_at: faker.date.past(),
    updated_at: faker.date.past(),
  };

  it('should POST /projects', () => {
    return app.httpRequest()
      .post('/projects')
      .set(app.auth_header)
      .send(project)
      .expect(201);
  });

  it('should PUT /projects/:id', () => {
    return app.httpRequest()
      .put(`/projects/${project.id}`)
      .set(app.auth_header)
      .send(project)
      .expect(200);
  });

  it('should delete /projects/:id', () => {
    return app.httpRequest()
      .delete(`/projects/${project.id}`)
      .set(app.auth_header)
      .expect(200);
  });

  it('should post /projects/:id/upsert', () => {
    return app.httpRequest()
      .post(`/projects/${project.id}/upsert`)
      .set(app.auth_header)
      .send(project)
      .expect(200);
  });

  it('should get /projects', async () => {
    const res = await app.httpRequest()
      .get('/projects?q=123')
      .expect(200);

    const result = res.body;
    assert(result);
    assert(result.hits);
    assert(result.total);
  });
});



'use strict';

const { app, assert } = require('egg-mock/bootstrap');
const faker = require('faker');

describe('test/app/controller/user.test.js', () => {
  const user = {
    id: faker.random.number(),
    username: faker.internet.userName(),
    nickname: faker.internet.userName(),
    portrait: faker.internet.avatar(),
    created_at: faker.date.past(),
    updated_at: faker.date.past(),
    total_projects: faker.random.number(),
    total_fans: faker.random.number(),
    total_follows: faker.random.number(),
    description: faker.lorem.text(),
  };

  it('should POST /users', () => {
    return app.httpRequest()
      .post('/users')
      .set(app.auth_header)
      .send(user)
      .expect(201);
  });

  it('should PUT /users/:id', () => {
    return app.httpRequest()
      .put(`/users/${user.id}`)
      .set(app.auth_header)
      .send(user)
      .expect(200);
  });

  it('should delete /users/:id', () => {
    return app.httpRequest()
      .delete(`/users/${user.id}`)
      .set(app.auth_header)
      .expect(200);
  });

  it('should post /users/:id/upsert', () => {
    return app.httpRequest()
      .post(`/users/${user.id}/upsert`)
      .set(app.auth_header)
      .send(user)
      .expect(200);
  });

  it('should get /users', async () => {
    const res = await app.httpRequest()
      .get('/users?q=123')
      .expect(200);

    const result = res.body;
    assert(result);
    assert(result.hits);
    assert(result.total);
  });
});



'use strict';

const { app, assert } = require('egg-mock/bootstrap');
const _ = require('lodash');

let helper;

before(async () => {
  await app.ready();
  const ctx = app.mockContext();
  helper = ctx.helper;
});

describe('test/app/extend/helper.test.js', () => {
  it('hanzi_to_pinyin', () => {
    const hanzi = '汉字';
    const expected = 'hanzi';
    assert(helper.hanzi_to_pinyin(hanzi) === expected);
  });

  it('paginate', () => {
    const query = {
      per_page: 10,
      page: 2,
    };
    const expected = [ 10, 10 ];
    assert(_.isEqual(helper.paginate(query), expected));
  });

  it('to_sha1', () => {
    const str = 'hello';
    assert(helper.to_sha1(str));
  });
});



'use strict';

const projects = require('./project');
const users = require('./user');
const pages = require('./page');
const packages = require('./page');

module.exports = { projects, users, pages, packages };



'use strict';

const faker = require('faker');
const _ = require('lodash');

const number_limit = { min: 0, max: 1000 };
const total = 20;

const packages = _.times(total, n => {
  const lesson = {
    _index: 'packages',
    _type: 'packages',
    _id: n,
    _score: (1 - n / total),
    _source: {
      id: n,
      title: faker.name.title(),
      prize: faker.random.number({ min: 0, max: 100 }),
      description: faker.lorem.text(),
      age_min: faker.random.number({ min: 0, max: 4 }),
      age_max: faker.random.number({ min: 4, max: 100 }),
      total_lessons: faker.random.number({ min: 1, max: 20 }),
      recent_view: faker.random.number(number_limit),
      created_at: faker.date.past(),
      updated_at: faker.date.past(),
    },
  };
  return lesson;
});

module.exports = packages;



'use strict';

const faker = require('faker');
const _ = require('lodash');
const total = 20;

const visibility = [ 'private', 'public' ];

const pages = _.times(total, n => {
  const page = {
    _index: 'projects',
    _type: 'projects',
    _id: n,
    _score: (1 - n / total),
    _source: {
      id: n,
      title: faker.name.title(),
      url: faker.internet.url(),
      site: faker.internet.domainName(),
      username: faker.internet.userName(),
      visibility: faker.helpers.randomize(visibility),
      content: faker.lorem.text(),
      created_at: faker.date.past(),
      updated_at: faker.date.past(),
    },
  };
  return page;
});

module.exports = pages;



'use strict';

const faker = require('faker');
const _ = require('lodash');

const number_limit = { min: 0, max: 1000 };
const types = [ 'website', 'paracraft' ];
const total = 20;

const projects = _.times(total, n => {
  const project = {
    _index: 'projects',
    _type: 'projects',
    _id: n,
    _score: (1 - n / total),
    _source: {
      name: faker.commerce.productName(),
      cover: faker.image.avatar(),
      username: faker.finance.accountName(),
      user_portrait: faker.image.avatar(),
      visibility: 'public',
      type: faker.helpers.randomize(types),
      recruiting: faker.random.boolean(),
      total_like: faker.random.number(number_limit),
      total_view: faker.random.number(number_limit),
      total_comment: faker.random.number(number_limit),
      recent_view: faker.random.number(number_limit),
      id: n,
      created_at: faker.date.past(),
      updated_at: faker.date.past(),
    },
  };
  return project;
});

module.exports = projects;


'use strict';

const faker = require('faker');
const _ = require('lodash');
const total = 20;

const users = _.times(total, n => {
  const user = {
    _index: 'projects',
    _type: 'projects',
    _id: n,
    _score: (1 - n / total),
    _source: {
      id: n,
      username: faker.internet.userName(),
      nickname: faker.internet.userName(),
      portrait: faker.internet.avatar(),
      created_at: faker.date.past(),
      updated_at: faker.date.past(),
      total_projects: faker.random.number(),
      total_fans: faker.random.number(),
      total_follows: faker.random.number(),
      description: faker.lorem.text(),
    },
  };
  return user;
});

module.exports = users;



'use strict';

const Router = require('koa-router');

module.exports = (app, data) => {
  const router = new Router();

  const OK = ctx => {
    ctx.body = { success: true };
  };

  router.post('/:index/:type/_search', ctx => {
    const { index } = ctx.params;
    const resources = data[index] || [];
    ctx.body = {
      timeout: false,
      hits: {
        hits: resources,
        total: resources.length,
      },
    };
  });

  router
    .all('/:index/:type', OK)
    .all('/:index/:type/:whatever', OK)
    .all('/:index/:type/:whatever1/:whatever2', OK);

  app.use(router.routes()).use(router.allowedMethods());
};



'use strict';

const Koa = require('koa');
const route = require('./router');
const data = require('./data/index');

module.exports = config => new Promise((resolve, reject) => {
  try {
    const app = new Koa();
    route(app, data);
    const port = config.port || 3000;
    const mockServer = app.listen(port, () => {
      resolve(mockServer);
    });
  } catch (error) {
    reject(error);
  }
});



'use strict';

const { app } = require('egg-mock/bootstrap');
const jwt = require('keepwork-jwt-simple');
const runMockServer = require('./mock-server/server');

let mockServer;

before(async () => {
  await app.ready();

  const mockServerConfig = app.config.mockServer;
  mockServer = await runMockServer(mockServerConfig);

  const secret = app.config.jwt.secret;
  const token = `Bearer ${jwt.encode({ roleId: 10 }, secret, 'HS1')}`;
  app.auth_header = { Authorization: token };
});

after(() => {
  mockServer.close();
});

<template>
  <div class="all-projects" v-loading="loading">
    <el-row class="all-projects-boxs">
      <el-col :sm="12" :md="6" :xs="12" v-for="(project,index) in allProjectsDataOptimize" :key="index">
        <project-cell :project="project"></project-cell>
      </el-col>
    </el-row>
    <div class="all-projects-pages" v-if="projectsCount > perPage">
      <el-pagination background @current-change="targetPage" layout="prev, pager, next" :page-size="perPage" :total="projectsCount">
      </el-pagination>
    </div>
    <transition name="fade">
      <div v-show="nothing" class="all-projects-nothing">
        <img class="all-projects-nothing-img" src="@/assets/pblImg/no_result.png" alt="">
        <p class="all-projects-nothing-tip">{{$t('explore.noResults')}}</p>
      </div>
    </transition>
  </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
import _ from 'lodash'
import TabMixin from './TabMixin'

export default {
  name: 'AllProjects',
  props: {
    searchKey: String,
    sortProjects: String
  },
  data() {
    return {
      loading: true
    }
  },
  mixins: [TabMixin],
  async mounted() {
    await this.targetPage(this.page)
  },
  computed: {
    ...mapGetters({
      allProjects: 'pbl/allProjects'
    }),
    nothing() {
      return this.allProjectsDataOptimize.length === 0 && !this.loading
    },
    projectsCount() {
      return _.get(this.allProjects, 'total', 0)
    },
    allProjectsDataOptimize() {
      let hits = _.get(this.allProjects, 'hits', [])
      return _.map(hits, i => {
        return {
          id: i.id,
          _id: this.searchKeyResult(i, 'id'),
          name: this.searchKeyResult(i, 'name'),
          visit: i.total_view,
          star: i.total_like,
          comment: i.total_comment || 0,
          user: { username: i.username, portrait: i.user_portrait || '' },
          updatedAt: i.updated_at,
          createdAt: i.created_at,
          type: i.type === 'site' ? 0 : 1,
          privilege: i.recruiting ? 1 : 0,
          choicenessNo: i.recommended ? 1 : 0,
          rate: i.point || 0,
          extra: {
            imageUrl: i.cover,
            videoUrl: i.video,
            rate: { count: i.point ? 8 : 0 }
          }
        }
      })
    }
  },
  methods: {
    ...mapActions({
      getAllProjects: 'pbl/getAllProjects'
    }),
    async targetPage(targetPage) {
      this.loading = true
      this.$nextTick(async () => {
        await this.getAllProjects({
          page: targetPage,
          per_page: this.perPage,
          q: this.searchKey,
          sort: this.sortProjects
        })
        this.loading = false
        this.$emit('getAmount', this.projectsCount)
      })
    }
  }
}
</script>
<style lang="scss" scoped>
.all-projects {
  min-height: 500px;
  .fade-enter-active {
    transition: opacity 2s;
  }
  .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }
  &-boxs {
    min-height: 560px;
  }
  &-pages {
    margin-top: 40px;
    text-align: center;
  }
  &-nothing {
    text-align: center;
    &-img {
      margin: 128px 0 32px;
    }
    &-tip {
      color: #606266;
      font-size: 14px;
    }
  }
}
</style>


<template>
  <div class="course-field" v-loading="loading">
    <el-row class="course-field-boxs">
      <el-col :sm="12" :md="6" :xs="12" v-for="(lessonPackage,index) in lessonPackagesData" :key="index">
        <lesson-package-cell :lessonPackage="lessonPackage"></lesson-package-cell>
      </el-col>
    </el-row>
    <div class="course-field-pages" v-if="lessonPackagesCount > perPage">
      <el-pagination background @current-change="targetPage" layout="prev, pager, next" :page-size="perPage" :total="lessonPackagesCount">
      </el-pagination>
    </div>
    <transition name="fade">
      <div v-show="nothing" class="course-field-nothing">
        <img class="course-field-nothing-img" src="@/assets/pblImg/no_result.png" alt="">
        <p class="course-field-nothing-tip">{{$t('explore.noResults')}}</p>
      </div>
    </transition>
  </div>
</template>
<script>
import LessonPackageCell from '../LessonPackageCell'
import _ from 'lodash'
import { EsAPI } from '@/api'
import TabMixin from './TabMixin'

export default {
  name: 'Course',
  props: {
    searchKey: String,
    sortProjects: String
  },
  data() {
    return {
      loading: true,
      lessonPackages: []
    }
  },
  mixins: [TabMixin],
  async mounted() {
    await this.targetPage(this.page)
  },
  computed: {
    nothing() {
      return this.lessonPackagesData.length === 0 && !this.loading
    },
    lessonPackagesCount() {
      return _.get(this.lessonPackages, 'total', 0)
    },
    lessonPackagesData() {
      let tempArr = _.get(this.lessonPackages, 'hits', [])
      let Arr = _.forEach(tempArr, i => {
        i.title = this.searchKeyResult(i, 'title')
        i.description = this.searchKeyResult(i, 'description')
      })
      return Arr
    }
  },
  methods: {
    async targetPage(targetPage) {
      this.loading = true
      this.$nextTick(async () => {
        await EsAPI.packages
          .getPackages({
            page: targetPage,
            per_page: this.perPage,
            q: this.searchKey,
            sort: this.sortProjects
          })
          .then(res => {
            this.lessonPackages = res
          })
          .catch(err => console.error(err))
        this.loading = false
        this.$emit('getAmount', this.lessonPackagesCount)
      })
    }
  },
  components: {
    LessonPackageCell
  }
}
</script>
<style lang="scss" scoped>
.course-field {
  min-height: 500px;
  .fade-enter-active {
    transition: opacity 2s;
  }
  .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }
  &-boxs {
    min-height: 560px;
  }
  &-pages {
    margin-top: 40px;
    text-align: center;
  }
  &-nothing {
    text-align: center;
    &-img {
      margin: 128px 0 32px;
    }
    &-tip {
      color: #606266;
      font-size: 14px;
    }
  }
}
</style>


<template>
  <div class="paracraft-field" v-loading="loading">
    <el-row class="paracraft-field-boxs">
      <el-col :sm="12" :md="6" :xs="12" v-for="(project,index) in pracraftData" :key="index">
        <project-cell :project="project"></project-cell>
      </el-col>
    </el-row>
    <div class="paracraft-field-pages" v-if="paracraftCount > perPage">
      <el-pagination background @current-change="targetPage" layout="prev, pager, next" :page-size="perPage" :total="paracraftCount">
      </el-pagination>
    </div>
    <transition name="fade">
      <div v-show="nothing" class="paracraft-field-nothing">
        <img class="paracraft-field-nothing-img" src="@/assets/pblImg/no_result.png" alt="">
        <p class="paracraft-field-nothing-tip">{{$t('explore.noResults')}}</p>
      </div>
    </transition>
  </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
import _ from 'lodash'
import TabMixin from './TabMixin'

export default {
  name: 'ParacraftField',
  props: {
    searchKey: String,
    sortProjects: String
  },
  data() {
    return {
      loading: true
    }
  },
  mixins: [TabMixin],
  async mounted() {
    await this.targetPage(this.page)
  },
  computed: {
    ...mapGetters({
      pblParacraft: 'pbl/diffTypeProject'
    }),
    nothing() {
      return this.pracraftData.length === 0 && !this.loading
    },
    paracraft() {
      return this.pblParacraft({ type: 'paracraft' })
    },
    paracraftCount() {
      return _.get(this.paracraft, 'total', 0)
    },
    pracraftData() {
      let hits = _.get(this.paracraft, 'hits', [])
      return _.map(hits, i => {
        return {
          id: i.id,
          _id: this.searchKeyResult(i, 'id'),
          name: this.searchKeyResult(i, 'name'),
          visit: i.total_view,
          star: i.total_like,
          comment: i.total_comment || 0,
          user: { username: i.username, portrait: i.user_portrait || '' },
          updatedAt: i.updated_at,
          createdAt: i.created_at,
          type: i.type === 'site' ? 0 : 1,
          privilege: i.recruiting ? 1 : 0,
          choicenessNo: i.recommended ? 1 : 0,
          rate: i.point || 0,
          extra: {
            imageUrl: i.cover,
            videoUrl: i.video,
            rate: { count: i.point ? 8 : 0 }
          }
        }
      })
    }
  },
  methods: {
    ...mapActions({
      getTypeProjects: 'pbl/getTypeProjects'
    }),
    async targetPage(targetPage) {
      this.loading = true
      this.$nextTick(async () => {
        await this.getTypeProjects({
          page: targetPage,
          per_page: this.perPage,
          type: 'paracraft',
          q: this.searchKey,
          sort: this.sortProjects
        })
        this.loading = false
        this.$emit('getAmount', this.paracraftCount)
      })
    }
  }
}
</script>
<style lang="scss" scoped>
.paracraft-field {
  min-height: 500px;
  .fade-enter-active {
    transition: opacity 2s;
  }
  .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }
  &-boxs {
    min-height: 560px;
  }
  &-pages {
    margin-top: 40px;
    text-align: center;
  }
  &-nothing {
    text-align: center;
    &-img {
      margin: 128px 0 32px;
    }
    &-tip {
      color: #606266;
      font-size: 14px;
    }
  }
}
</style>


<template>
  <div class="picked-projects" v-loading="loading">
    <el-row class="picked-projects-boxs">
      <el-col :sm="12" :md="6" :xs="12" v-for="(project,index) in pickedProjectsData" :key="index">
        <project-cell :project="project"></project-cell>
      </el-col>
    </el-row>
    <div class="picked-projects-pages" v-if="pickedProjectsCount > perPage">
      <el-pagination background @current-change="targetPage" layout="prev, pager, next" :page-size="perPage" :total="pickedProjectsCount">
      </el-pagination>
    </div>
    <transition name="fade">
      <div v-show="nothing" class="picked-projects-nothing">
        <img class="picked-projects-nothing-img" src="@/assets/pblImg/no_result.png" alt="">
        <p class="picked-projects-nothing-tip">{{$t('explore.noResults')}}</p>
      </div>
    </transition>
  </div>
</template>
<script>
import _ from 'lodash'
import { EsAPI } from '@/api'
import TabMixin from './TabMixin'

export default {
  name: 'PickedProjects',
  props: {
    searchKey: String,
    sortProjects: String
  },
  data() {
    return {
      loading: true,
      pickedProjects: []
    }
  },
  mixins: [TabMixin],
  async mounted() {
    await this.targetPage(this.page)
  },
  computed: {
    nothing() {
      return this.pickedProjectsData.length === 0 && !this.loading
    },
    pickedProjectsCount() {
      return _.get(this.pickedProjects, 'total', 0)
    },
    pickedProjectsData() {
      let hits = _.get(this.pickedProjects, 'hits', [])
      return _.map(hits, i => {
        return {
          id: i.id,
          _id: this.searchKeyResult(i, 'id'),
          name: this.searchKeyResult(i, 'name'),
          visit: i.total_view,
          star: i.total_like,
          comment: i.total_comment || 0,
          user: { username: i.username, portrait: i.user_portrait || '' },
          updatedAt: i.updated_at,
          createdAt: i.created_at,
          type: i.type === 'site' ? 0 : 1,
          privilege: i.recruiting ? 1 : 2,
          choicenessNo: i.recommended ? 1 : 0,
          rate: i.point || 0,
          extra: {
            imageUrl: i.cover,
            videoUrl: i.video,
            rate: { count: i.point ? 8 : 0 }
          }
        }
      })
    }
  },
  methods: {
    async targetPage(targetPage) {
      this.loading = true
      this.$nextTick(async () => {
        await EsAPI.projects
          .getProjects({
            page: targetPage,
            per_page: this.perPage,
            recommended: true,
            q: this.searchKey,
            sort: this.sortProjects
          })
          .then(res => {
            this.pickedProjects = res
          })
          .catch(err => console.error(err))
        this.loading = false
        this.$emit('getAmount', this.pickedProjectsCount)
      })
    }
  }
}
</script>
<style lang="scss" scoped>
.picked-projects {
  min-height: 500px;
  .fade-enter-active {
    transition: opacity 2s;
  }
  .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }
  &-boxs {
    min-height: 560px;
  }
  &-pages {
    margin-top: 40px;
    text-align: center;
  }
  &-nothing {
    text-align: center;
    &-img {
      margin: 128px 0 32px;
    }
    &-tip {
      color: #606266;
      font-size: 14px;
    }
  }
}
</style>


<template>
  <div class="recruiting-field" v-loading="loading">
    <el-row class="recruiting-field-boxs">
      <el-col :sm="12" :md="6" :xs="12" v-for="(project,index) in recruitmentData" :key="index">
        <project-cell :project="project"></project-cell>
      </el-col>
    </el-row>
    <div class="recruiting-field-pages" v-if="recruitingCount > perPage">
      <el-pagination background @current-change="targetPage" layout="prev, pager, next" :page-size="perPage" :total="recruitingCount">
      </el-pagination>
    </div>
    <transition name="fade">
      <div v-show="nothing" class="recruiting-field-nothing">
        <img class="recruiting-field-nothing-img" src="@/assets/pblImg/no_result.png" alt="">
        <p class="recruiting-field-nothing-tip">{{$t('explore.noResults')}}</p>
      </div>
    </transition>
  </div>
</template>
<script>
import _ from 'lodash'
import { EsAPI } from '@/api'
import TabMixin from './TabMixin'

export default {
  name: 'RecruitingField',
  props: {
    searchKey: String,
    sortProjects: String
  },
  data() {
    return {
      loading: true,
      recruitongProjects: []
    }
  },
  mixins: [TabMixin],
  async mounted() {
    await this.targetPage(this.page)
  },
  computed: {
    nothing() {
      return this.recruitmentData.length === 0 && !this.loading
    },
    recruitingCount() {
      return _.get(this.recruitongProjects, 'total', 0)
    },
    recruitmentData() {
      let hits = _.get(this.recruitongProjects, 'hits', [])
      return _.map(hits, i => {
        return {
          id: i.id,
          _id: this.searchKeyResult(i, 'id'),
          name: this.searchKeyResult(i, 'name'),
          visit: i.total_view,
          star: i.total_like,
          comment: i.total_comment || 0,
          user: { username: i.username, portrait: i.user_portrait || '' },
          updatedAt: i.updated_at,
          createdAt: i.created_at,
          type: i.type === 'site' ? 0 : 1,
          privilege: i.recruiting ? 1 : 2,
          choicenessNo: i.recommended ? 1 : 0,
          rate: i.point || 0,
          extra: {
            imageUrl: i.cover,
            videoUrl: i.video,
            rate: { count: i.point ? 8 : 0 }
          }
        }
      })
    }
  },
  methods: {
    async targetPage(targetPage) {
      this.loading = true
      this.$nextTick(async () => {
        await EsAPI.projects
          .getProjects({
            page: targetPage,
            per_page: this.perPage,
            recruiting: true,
            q: this.searchKey,
            sort: this.sortProjects
          })
          .then(res => {
            this.recruitongProjects = res
          })
          .catch(err => console.error(err))
        this.loading = false
        this.$emit('getAmount', this.recruitingCount)
      })
    }
  }
}
</script>
<style lang="scss" scoped>
.recruiting-field {
  min-height: 500px;
  .fade-enter-active {
    transition: opacity 2s;
  }
  .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }
  &-boxs {
    min-height: 560px;
  }
  &-pages {
    margin-top: 40px;
    text-align: center;
  }
  &-nothing {
    text-align: center;
    &-img {
      margin: 128px 0 32px;
    }
    &-tip {
      color: #606266;
      font-size: 14px;
    }
  }
}
</style>


<script>
import ProjectCell from '../ProjectCell'

export default {
  data() {
    return {
      perPage: 20,
      page: 1
    }
  },
  methods: {
    searchKeyResult(i, key) {
      if (i.highlight) {
        if (i.highlight[key]) {
          let name = _.get(i.highlight, key, i[key])
          if (key === 'id') {
            return name.join().replace(/<span>/g, `<span class="red">#`)
          }
          if (key === 'content') {
            return name.join('...').replace(/<span>/g, `<span class="red">`)
          }
          return name.join().replace(/<span>/g, `<span class="red">`)
        }
      }
      if (key === 'id') {
        return '#' + i[key]
      }
      if (key === 'content' && i[key].length > 80) {
        return i[key].substring(0, 80) + '...'
      }
      return i[key]
    }
  },
  components: {
    ProjectCell
  }
}
</script>

<template>
  <div class="user-cell">
    <div class="user-tab">
      <div class="user-tab-cover">
        <a :href="`/u/${user.username}`" target="_blank">
          <img class="user-tab-cover-img" :src="user.portrait || default_portrait" alt="">
        </a>
      </div>
      <h5 class="user-tab-name"><a :href="`/u/${user.username}`" target="_blank">{{user.username}}</a></h5>
      <p class="user-tab-brief" :title="user.description">{{user.description || $t("common.noSelfIntro")}}</p>
      <div class="user-tab-abstract">
        <div>
          <p class="title">{{$t("explore.project")}}</p>
          <p class="amount">{{user.total_projects || 0}}</p>
        </div>
        <div class="member">
          <p class="title">{{$t("explore.following")}}</p>
          <p class="amount">{{user.total_follows || 0}}</p>
        </div>
        <div>
          <p class="title">{{$t("explore.followers")}}</p>
          <p class="amount">{{user.total_fans || 0}}</p>
        </div>
      </div>
      <div class="user-tab-join">
        <el-button type="primary" :class="['user-tab-join-button',{'is-followed': user.isFollowed}]" :loading="isLoading" @click="toggleFollow(user)">{{user.isFollowed ? $t("explore.followed") : $t("explore.follow")}}</el-button>
        <a class="user-tab-join-button" :href="`/u/${user.username}`" target="_blank">{{$t("explore.profile")}}</a>
      </div>
    </div>
  </div>
</template>
<script>
import default_portrait from '@/assets/img/default_portrait.png'
import { keepwork, EsAPI } from '@/api'
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'UserCell',
  props: {
    user: {
      type: Object,
      default() {
        return {}
      }
    }
  },
  data() {
    return {
      isLoading: false,
      default_portrait
    }
  },
  computed: {
    ...mapGetters({
      isLogined: 'user/isLogined',
    })
  },
  methods: {
    ...mapActions({
      toggleLoginDialog: 'pbl/toggleLoginDialog'
    }),
    showMessage({ type = 'success', message = '操作成功' }) {
      this.$message({ type, message })
    },
    async toggleFollow(user) {
      if (!this.isLogined) {
        return this.toggleLoginDialog(true)
      }
      this.isLoading = true
      if (!this.user.isFollowed) {
        await keepwork.favorites
          .favoriteObject({ objectId: user.id, objectType: 0 })
          .then(res => {
            this.showMessage({
              message: this.$t('explore.successfullyFollowed')
            })
            this.user.isFollowed = true
            this.user.total_fans = this.user.total_fans ? this.user.total_fans + 1 : 1
            this.isLoading = false
          })
          .catch(err => {
            this.showMessage({
              message: '关注失败'
            })
            this.isLoading = false
          })
      } else {
        await keepwork.favorites
          .unFavoriteObject({ objectId: user.id, objectType: 0 })
          .then(res => {
            this.showMessage({
              message: this.$t('explore.successfullyUnfollowed')
            })
            this.user.isFollowed = false
            this.user.total_fans =
              this.user.total_fans - 1 < 0 ? 0 : this.user.total_fans - 1
            this.isLoading = false
          })
          .catch(err => {
            this.showMessage({
              message: '取消关注失败'
            })
            this.isLoading = false
          })
      }
    }
  }
}
</script>

<style lang="scss">
.user-cell {
  .user-tab {
    width: 286px;
    border: 1px solid #e8e8e8;
    background: #fff;
    padding: 30px 0;
    text-align: center;
    margin: 0 auto 10px;
    transition: all 200ms ease-in;
    &:hover {
      box-shadow: 0 12px 24px -6px rgba(0, 0, 0, 0.16);
      transition: all 200ms ease-in;
    }
    &-cover {
      width: 96px;
      height: 96px;
      cursor: pointer;
      margin: 0 auto;
      &-img {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
      }
    }
    &-name {
      font-size: 16px;
      margin: 18px 0;
      line-height: 22px;
      & > a {
        color: #333;
        text-decoration: none;
        &:hover {
          color: #2397f3;
        }
      }
    }
    &-brief {
      font-size: 12px;
      color: #999;
      margin: 9px 9px;
      line-height: 16px;
      height: 18px;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
    &-abstract {
      display: flex;
      div {
        flex: 1;
        .title {
          font-size: 13px;
          color: #666;
        }
        .amount {
          line-height: 18px;
          font-size: 18px;
          color: #333;
        }
      }
      .member {
        position: relative;
      }
      .member::before {
        content: "";
        width: 1px;
        height: 20px;
        background: rgb(202, 200, 200);
        position: absolute;
        left: 0;
        top: 32px;
      }
      .member::after {
        content: "";
        width: 1px;
        height: 20px;
        background: rgb(202, 200, 200);
        position: absolute;
        right: 0;
        top: 32px;
      }
    }
    &-join {
      padding-top: 6px;
      &-button {
        height: 32px;
        width: 108px;
        padding: 0;
      }
      & a {
        display: inline-block;
        border: 1px solid #dcdfe6;
        line-height: 32px;
        text-decoration: none;
        border-radius: 4px;
        margin-left: 10px;
        color: #606266;
        &:hover {
          color: #409eff;
          border-color: #c6e2ff;
          background-color: #ecf5ff;
        }
      }
    }
    .is-followed {
      background-color: transparent;
      color: #2397f3;
    }
  }
}
@media screen and (max-width: 768px) {
  .user-cell {
    .user-tab {
      width: 164px;
      padding: 6px;
      font-size: 12px;
      &-cover {
        width: 56px;
        height: 56px;
      }
      &-name {
        font-size: 12px;
        margin: 8px;
      }
      &-brief {
        margin: 3px;
      }
      &-abstract {
        div {
          .title,
          .amount {
            font-size: 12px;
            height: 18px;
            margin: 10px 0;
          }
        }
        .member::before,
        .member::after {
          height: 20px;
          position: absolute;
          top: 22px;
        }
      }
      &-join {
        &-button {
          width: 70px;
        }
      }
    }
  }
}
</style>

<template>
  <div class="user-field" v-loading="loading">
    <el-row class="user-field-boxs">
      <el-col :sm="12" :md="6" :xs="12" v-for="(user) in allUsersData" :key="user.id">
        <user-cell :user="user"></user-cell>
      </el-col>
    </el-row>
    <div class="user-field-pages" v-if="usersCount > perPage">
      <el-pagination background @current-change="targetPage" layout="prev, pager, next" :page-size="perPage" :total="usersCount">
      </el-pagination>
    </div>
    <transition name="fade">
      <div v-show="nothing" class="user-field-nothing">
        <img class="user-field-nothing-img" src="@/assets/pblImg/no_result.png" alt="">
        <p class="user-field-nothing-tip">{{$t('explore.noResults')}}</p>
      </div>
    </transition>
  </div>
</template>
<script>
import _ from 'lodash'
import { mapActions, mapGetters } from 'vuex'
import default_portrait from '@/assets/img/default_portrait.png'
import { keepwork, EsAPI } from '@/api'
import UserCell from './UserCell'
import TabMixin from './TabMixin'

export default {
  name: 'UsersField',
  props: {
    searchKey: String,
    sortUsers: String
  },
  data() {
    return {
      loading: true,
      default_portrait,
      userAllFollows: [],
      currentPage: 1
    }
  },
  mixins: [TabMixin],
  async mounted() {
    await this.targetPage(this.page)
  },
  components: {
    UserCell
  },
  computed: {
    ...mapGetters({
      allUsers: 'pbl/allUsers',
      userProfile: 'user/profile'
    }),
    nothing() {
      return this.allUsersData.length === 0 && !this.loading
    },
    usersCount() {
      return _.get(this.allUsers, 'total', 0)
    },
    allUsersData() {
      let hits = _.get(this.allUsers, 'hits', [])
      let users = _.map(hits, user => {
        return {
          ...user,
          isFollowed: this.userAllFollows
            .map(item => item.objectId)
            .includes(user.id)
        }
      })
      return users
    },
    userId() {
      return _.get(this.userProfile, 'id', '')
    },
    isFollow() {
      return (user, index) => {
        return this.userAllFollows.map(item => item.objectId).includes(user.id)
      }
    }
  },
  methods: {
    ...mapActions({
      getAllUsers: 'pbl/getAllUsers',
      getUserFavorite: 'pbl/getUserFavorite',
      toggleLoginDialog: 'pbl/toggleLoginDialog'
    }),
    async targetPage(targetPage) {
      this.currentPage = targetPage
      this.loading = true
      this.$nextTick(async () => {
        await this.getAllUsers({
          page: targetPage,
          per_page: this.perPage,
          q: this.searchKey,
          sort: this.sortUsers
        })
        this.loading = false
        this.$emit('getAmount', this.usersCount)
        this.getFollows()
      })
    },
    async getFollows() {
      let searchUserIsMyFavorite = []
      _.map(this.allUsersData, i => {
        searchUserIsMyFavorite.push(i.id)
      })
      await keepwork.favorites
        .getUserSearchAllFavorites({
          userId: this.userId,
          objectType: 0,
          objectId: {
            $in: searchUserIsMyFavorite
          }
        })
        .then(res => {
          this.userAllFollows = _.get(res, 'rows', [])
        })
    }
  }
}
</script>
<style lang="scss" scoped>
.user-field {
  min-height: 500px;
  .fade-enter-active {
    transition: opacity 2s;
  }
  .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }
  &-boxs {
    min-height: 560px;
  }
  &-pages {
    margin-top: 40px;
    text-align: center;
  }
  &-nothing {
    text-align: center;
    &-img {
      margin: 128px 0 32px;
    }
    &-tip {
      color: #606266;
      font-size: 14px;
    }
  }
}
</style>

<template>
  <div class="webpage-field" v-loading="loading">
    <div class="webpage-field-content" v-for="(webpage,index) in webpagesData" :key="index">
      <div class="webpage-field-content-top">
        <a :href="webpage.url" target="_blank" class="webpage-field-content-top-title" v-html="webpage.title"></a>
        <a :href="webpage.url" target="_blank" class="webpage-field-content-top-url" v-html="origin + webpage.url_html"></a>
      </div>
      <p class="webpage-field-content-text" v-html="webpage.content"></p>
    </div>
    <div class="webpage-field-pages" v-if="webpagesCount > perPage">
      <el-pagination background @current-change="targetPage" layout="prev, pager, next" :page-size="perPage" :total="webpagesCount">
      </el-pagination>
    </div>
    <transition name="fade">
      <div v-show="nothing" class="webpage-field-nothing">
        <img class="webpage-field-nothing-img" src="@/assets/pblImg/no_result.png" alt="">
        <p class="webpage-field-nothing-tip">{{$t('explore.noResults')}}</p>
      </div>
    </transition>
  </div>
</template>
<script>
import _ from 'lodash'
import { EsAPI } from '@/api'
import TabMixin from './TabMixin'

export default {
  name: 'WebpageField',
  props: {
    searchKey: String,
    sortProjects: String
  },
  data() {
    return {
      loading: true,
      webpages: [],
      perPage: 12
    }
  },
  mixins: [TabMixin],
  async mounted() {
    await this.targetPage(1)
  },
  computed: {
    origin() {
      return window.location.origin + '/'
    },
    webpagesData() {
      let hits = _.get(this.webpages, 'hits', [])
      return _.map(hits, i => {
        return {
          ...i,
          title: this.searchKeyResult(i, 'title'),
          url_html: this.searchKeyResult(i, 'url'),
          content: this.searchKeyResult(i, 'content')
        }
      })
    },
    webpagesCount() {
      return _.get(this.webpages, 'total', 0)
    },
    nothing() {
      return this.webpagesCount === 0 && !this.loading
    }
  },
  methods: {
    async targetPage(targetPage) {
      this.loading = true
      this.$nextTick(async () => {
        await EsAPI.webpages
          .getWebpages({
            page: targetPage,
            per_page: this.perPage,
            q: this.searchKey,
            sort: this.sortProjects
          })
          .then(res => {
            this.webpages = res
          })
          .catch(err => console.error(err))
        this.loading = false
        this.$emit('getAmount', this.webpagesCount)
      })
    }
  }
}
</script>
<style lang="scss">
.webpage-field {
  min-height: 500px;
  &-content {
    background: #fff;
    padding: 8px;
    margin-bottom: 16px;
    color: #212224;
    .red {
      color: red;
    }
    &-top {
      cursor: pointer;
      &:hover {
        .webpage-field-content-top-title {
          text-decoration: underline;
        }
      }
      &-title {
        color: #409efe;
        text-decoration: none;
        font-size: 18px;
        font-weight: bold;
        display: block;
        margin: 10px 0;
      }
      &-url {
        text-decoration: none;
        color: rgb(100, 218, 150);
      }
    }
    &-text {
      color: #909399;
      font-size: 14px;
      word-break: break-word;
    }
  }
  .fade-enter-active {
    transition: opacity 2s;
  }
  .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }
  &-pages {
    margin-top: 40px;
    text-align: center;
  }
  &-nothing {
    text-align: center;
    &-img {
      margin: 128px 0 32px;
    }
    &-tip {
      color: #606266;
      font-size: 14px;
    }
  }
}
</style>

<template>
  <div class="website-field" v-loading="loading">
    <el-row class="website-field-boxs">
      <el-col :sm="12" :md="6" :xs="12" v-for="(project,index) in websiteData" :key="index">
        <project-cell :project="project"></project-cell>
      </el-col>
    </el-row>
    <div class="website-field-pages" v-if="websiteCount > perPage">
      <el-pagination background @current-change="targetPage" layout="prev, pager, next" :page-size="perPage" :total="websiteCount">
      </el-pagination>
    </div>
    <transition name="fade">
      <div v-show="nothing" class="website-field-nothing">
        <img class="website-field-nothing-img" src="@/assets/pblImg/no_result.png" alt="">
        <p class="website-field-nothing-tip">{{$t('explore.noResults')}}</p>
      </div>
    </transition>
  </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
import _ from 'lodash'
import TabMixin from './TabMixin'

export default {
  name: 'WebsiteField',
  props: {
    searchKey: String,
    sortProjects: String
  },
  data() {
    return {
      loading: true
    }
  },
  mixins: [TabMixin],
  async mounted() {
    await this.targetPage(this.page)
  },
  computed: {
    ...mapGetters({
      pblWebsite: 'pbl/diffTypeProject'
    }),
    nothing() {
      return this.websiteData.length === 0 && !this.loading
    },
    website() {
      return this.pblWebsite({ type: 'site' })
    },
    websiteCount() {
      return _.get(this.website, 'total', 0)
    },
    websiteData() {
      let hits = _.get(this.website, 'hits', [])
      return _.map(hits, i => {
        return {
          id: i.id,
          _id: this.searchKeyResult(i, 'id'),
          name: this.searchKeyResult(i, 'name'),
          visit: i.total_view,
          star: i.total_like,
          comment: i.total_comment || 0,
          user: { username: i.username, portrait: i.user_portrait || '' },
          updatedAt: i.updated_at,
          createdAt: i.created_at,
          type: i.type === 'site' ? 0 : 1,
          privilege: i.recruiting ? 1 : 0,
          choicenessNo: i.recommended ? 1 : 0,
          rate: i.point || 0,
          extra: {
            imageUrl: i.cover,
            videoUrl: i.video,
            rate: { count: i.point ? 8 : 0 }
          }
        }
      })
    }
  },
  methods: {
    ...mapActions({
      getTypeProjects: 'pbl/getTypeProjects'
    }),
    async targetPage(targetPage) {
      this.loading = true
      this.$nextTick(async () => {
        await this.getTypeProjects({
          page: targetPage,
          per_page: this.perPage,
          type: 'site',
          q: this.searchKey,
          sort: this.sortProjects
        })
        this.loading = false
        this.$emit('getAmount', this.websiteCount)
      })
    }
  }
}
</script>
<style lang="scss" scoped>
.website-field {
  min-height: 500px;
  .fade-enter-active {
    transition: opacity 2s;
  }
  .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }
  &-boxs {
    min-height: 560px;
  }
  &-pages {
    margin-top: 40px;
    text-align: center;
  }
  &-nothing {
    text-align: center;
    &-img {
      margin: 128px 0 32px;
    }
    &-tip {
      color: #606266;
      font-size: 14px;
    }
  }
}
</style>

<template>
  <div class="exploration-page">
    <div class="exploration-page-theme">
      <div class="exploration-page-theme-center">
        <div class="theme">
          <el-input :placeholder="$t('explore.searchFor')" class="search-input" v-model="searchKey" @keyup.enter.native="goSearch">
            <i slot="suffix" class="el-icon-search search-input-button" @click="goSearch"> {{$t("explore.search")}}</i>
          </el-input>
        </div>
        <div class="search">
          <el-row>
            <el-col :sm="16" :xs="24">
              <div class="search-tab">
                <el-menu :default-active="activeTabIndex" class="search-tab-menu" mode="horizontal" @select="handleSelectTab">
                  <el-menu-item v-for="item in tabBar" :key='item.command' :index="item.command">{{item.tag}}</el-menu-item>
                </el-menu>
              </div>
            </el-col>
            <el-col :sm="8" :xs="24">
              <div class="search-result">
                <span class="contain-total">{{$t("explore.contain")}}<span class="contain-total-num">{{searchResultAmount}}</span>{{$t("explore.result")}}</span>
                <el-dropdown @command="handleSort" class="sort-dropdown-menu">
                  <span class="el-dropdown-link">
                    {{currSortMode}}
                    <i class="el-icon-arrow-down el-icon--right"></i>
                  </span>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item v-for="(i,index) in currSortColumn" :key="index" :command="i">{{i.mode}}</el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
    </div>
    <div class="exploration-page-cabinet">
      <div class="exploration-page-cabinet-center">
        <div class="selected-projects">
          <component :is="currentTabComp" :ref="currentTab" :searchKey="searchKey" :sortProjects="sortProjects" @getAmount="getAmount"></component>
        </div>
        <!-- <div class="selected-studio" v-if='currentTab == ""'>
          <el-row>
            <el-col :span="6">
              <div class="studio">
                <img class="studio-cover" src="http://star.rayli.com.cn/public/upload/share/000/001/658/04/bcfec7af1f18a45ddc90ec7f9d40a649OJWppZ.jpeg" alt="">
                <h5 class="studio-name">笑傲江湖</h5>
                <p class="studio-brief">你好，这里是笑傲江湖工作室</p>
                <div class="studio-abstract">
                  <div>
                    <p class="title">项目</p>
                    <p class="amount">123456</p>
                  </div>
                  <div class="member">
                    <p class="title">成员</p>
                    <p class="amount">123456</p>
                  </div>
                  <div>
                    <p class="title">粉丝</p>
                    <p class="amount">1235689</p>
                  </div>
                </div>
                <div class="studio-jion">
                  <el-button type="primary" class="studio-jion-button">申请加入</el-button>
                  <el-button class="studio-jion-button">关注</el-button>
                </div>
              </div>
            </el-col>
          </el-row>
        </div> -->
      </div>
    </div>
  </div>
</template>
<script>
import PickedProjects from './explorationPageTab/PickedProjects'
import AllProjects from './explorationPageTab/AllProjects'
import ParacraftField from './explorationPageTab/ParacraftField'
import WebsiteField from './explorationPageTab/WebsiteField'
import CourseField from './explorationPageTab/CourseField'
import RecruitingField from './explorationPageTab/RecruitingField'
import UsersField from './explorationPageTab/UsersField'
import WebpageField from './explorationPageTab/WebpageField'
import { EsAPI } from '@/api'
import _ from 'lodash'
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'ExplorationPage',
  data() {
    return {
      activeTabIndex: 'allProjects',
      currentTab: 'allProjects',
      searchKey: '',
      sortProjects: '',
      currSortMode: this.$t('explore.overall'),
      searchResultAmount: 0,
      currentTabComp: '',
      tabBar: [
        { command: 'pickedProjects', tag: this.$t('home.selectedProjects') },
        { command: 'allProjects', tag: this.$t('explore.project') },
        { command: 'paracraftField', tag: this.$t('explore.3DWorlds') },
        { command: 'websiteField', tag: this.$t('explore.websites') },
        // { command: 'courseField', tag: this.$t('explore.lessons') },
        { command: 'usersField', tag: this.$t('explore.uses') },
        { command: 'webpageField', tag: this.$t('editor.website') },
        { command: 'recruitingField', tag: this.$t('explore.recruiting') }
      ]
    }
  },
  created() {
    window.scrollTo(0, 0)
  },
  mounted() {
    this.resetUrl()
    const { query } = this.$route
    this.currentTab = query.tab
    this.activeTabIndex = query.tab
    this.currentTabComp = query.tab
    if (query && query.keyword) {
      this.searchKey = query.keyword
    }
    this.goSearch()
  },
  computed: {
    ...mapGetters({
      allProjects: 'pbl/allProjects',
      paracraft: 'pbl/paracraft',
      website: 'pbl/website'
    }),
    currSortColumn() {
      let tabs = [
        'pickedProjects',
        'allProjects',
        'paracraftField',
        'websiteField',
        'courseField',
        'recruitingField'
      ]
      if (tabs.includes(this.currentTab)) {
        return [
          { mode: this.$t('explore.overall'), command: '/综合' },
          { mode: this.$t('explore.newest'), command: 'updated_at/最新' },
          { mode: this.$t('explore.hottest'), command: 'recent_view/热门' }
        ]
      }
      if (this.currentTab === 'webpageField') {
        return [
          { mode: this.$t('explore.overall'), command: '/综合' },
          { mode: this.$t('explore.newest'), command: 'updated_at/最新' }
          // { mode: this.$t('explore.hottest'), command: 'recent_view/热门' }
        ]
      }
      if (this.currentTab === 'usersField') {
        return [
          { mode: this.$t('explore.overall'), command: '/综合' },
          {
            mode: this.$t('explore.projectSort'),
            command: 'total_projects/项目'
          },
          { mode: this.$t('explore.popularity'), command: 'total_fans/名气' }
        ]
      }
      return [{ mode: this.$t('explore.overall'), command: '/综合' }]
    }
  },
  methods: {
    resetUrl() {
      if (this.$route.query.searchType && this.$route.query.keyword) {
        let origin = window.location.origin
        history.replaceState('', '', `${origin}/exploration?tab=allProjects`)
      }
    },
    getAmount(amount) {
      this.searchResultAmount = amount
    },
    filterSuggetions(res, cb) {
      if (res.length) {
        cb(_.map(res, i => ({ value: i.keyword })))
      }
    },
    handleSort(selectSort) {
      let sortType = selectSort.command
      this.currSortMode = selectSort.mode
      this.sortProjects = sortType.split('/')[0]
      this.goSearch()
    },
    goSearch() {
      this.$nextTick(async () => {
        this.$refs[this.currentTab].targetPage(1)
      })
    },
    handleSelectTab(key, keyPath) {
      this.$router.push({
        name: 'ExplorationPage',
        query: {
          tab: key
        }
      })
      this.currentTabComp = key
      this.currentTab = key
      this.currSortMode = this.$t('explore.overall')
      this.sortProjects = ''
    }
  },
  components: {
    PickedProjects,
    AllProjects,
    ParacraftField,
    WebsiteField,
    CourseField,
    RecruitingField,
    UsersField,
    WebpageField
  }
}
</script>

<style lang='scss'>
.exploration-page {
  &-theme {
    background: #fff;
    padding-top: 24px;
    &-center {
      margin: 10px auto 0;
      max-width: 1200px;
      .theme {
        text-align: center;
        margin: 0 auto 32px;
        .explore {
          color: #409eff;
        }
      }
      .search {
        &-tab {
          &-menu {
            border: none;
            &.el-menu.el-menu--horizontal {
              border: none;
              .el-menu-item {
                padding: 0 10px;
              }
            }
          }
        }
        &-input {
          width: 480px;
          height: 40px;
          .el-input__inner {
            height: 40px;
            background: #f5f5f5;
            border: #f5f5f5 1px solid;
          }
          .el-input__inner:hover,
          .el-input__inner:focus {
            border-color: #409efe;
          }
          .el-input__suffix {
            right: 0;
            top: 0;
            -webkit-transition: all 0.3s;
            transition: all 0.3s;
            background: #409eff;
            color: #fff;
            display: inline-block;
            width: 88px;
            height: 40px;
            line-height: 40px;
            border-radius: 4px;
            font-size: 16px;
            letter-spacing: 4px;
          }
          &-button {
            font-weight: bold;
            line-height: 32px;
            cursor: pointer;
            white-space: nowrap;
            letter-spacing: normal;
          }
        }
        .search-result {
          text-align: right;
          .contain-total {
            font-size: 14px;
            padding-right: 30px;
            color: #606266;
            &-num {
              color: #409eff;
            }
          }
          .el-dropdown-link {
            display: inline-block;
            height: 60px;
            line-height: 60px;
            font-size: 14px;
            color: #606266;
            cursor: pointer;
          }
        }
      }
    }
  }
  &-cabinet {
    background: #f6f7f8;
    &-center {
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px 0 56px;
      .selected-studio {
        .el-row {
          .studio {
            width: 286px;
            border: 1px solid #e8e8e8;
            background: #fff;
            padding: 30px 0;
            text-align: center;
            &-cover {
              width: 96px;
              height: 96px;
              border-radius: 50%;
              object-fit: cover;
            }
            &-name {
              font-size: 16px;
              color: #333;
              margin: 18px 0;
            }
            &-brief {
              font-size: 12px;
              color: #999;
              margin: 9px 0;
            }
            &-abstract {
              display: flex;
              div {
                flex: 1;
                .title {
                  font-size: 13px;
                  color: #666;
                }
                .amount {
                  font-size: 18px;
                  color: #333;
                }
              }
              .member {
                position: relative;
              }
              .member::before {
                content: '';
                width: 1px;
                height: 20px;
                background: rgb(202, 200, 200);
                position: absolute;
                left: 0;
                top: 32px;
              }
              .member::after {
                content: '';
                width: 1px;
                height: 20px;
                background: rgb(202, 200, 200);
                position: absolute;
                right: 0;
                top: 32px;
              }
            }
            &-jion {
              padding-top: 6px;
              &-button {
                height: 32px;
                width: 108px;
                padding: 0;
              }
            }
          }
        }
      }
    }
  }
  .search-result-total {
    padding: 15px 0;
    font-size: 18px;
    margin: 20px 30px;
  }
}
@media screen and (max-width: 768px) {
  .exploration-page {
    &-theme {
      &-center {
        .theme {
          margin: 20px;
        }
        .search {
          &-tab {
            &-menu {
              display: flex;
              justify-content: center;
            }
          }
          &-input {
            width: 100%;
          }
          .search-result {
            text-align: left;
            padding: 0 16px;
            .contain-total {
              display: inline-block;
              height: 60px;
              line-height: 60px;
            }
            .sort-dropdown-menu {
              float: right;
            }
          }
        }
      }
    }
  }
}
</style>

<template>
  <el-input v-if="isShowSearchBar" v-model="searchText" class="search-bar-comp" :placeholder="$t('common.searchInKp')" @keyup.enter.native='goSearch'>
    <i slot="suffix" class="el-icon-search search-bar-comp-button" @click="goSearch"></i>
  </el-input>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
  name: 'SearchBar',
  data() {
    return {
      searchText: '',
      searchScope: 'all',
      isShowSearchBar: true
    }
  },
  computed: {
    ...mapGetters({
      loginUsername: 'user/username'
    }),
    isLogin() {
      return this.loginUsername
    }
  },
  watch: {
    $route({ name }) {
      this.isShowSearchBar = !['ExplorationPage'].includes(name)
    }
  },
  methods: {
    goSearch() {
      let searchParams = {
        searchType: 'pageinfo',
        keyword: this.searchText
      }
      if (this.searchScope === 'loginUser') {
        searchParams.username = this.loginUsername
      }
      let searchParamsArr = []
      _.forIn(searchParams, (value, key) => {
        searchParamsArr.push(`${key}=${value}`)
      })
      let searchUrl = encodeURI(`/explore?tab=allProjects&${searchParamsArr.join('&')}`)
      window.location.href = searchUrl
    }
  }
}
</script>
<style lang="scss">
.search-bar-comp {
  .el-input__inner {
    width: 240px;
    height: 32px;
    background: #f5f5f5;
    border: none;
  }
  &-button {
    font-weight: bold;
  }
  .el-input__inner:hover,
  .el-input__inner:focus {
    border-color: #dcdfe6;
  }
  &-select {
    .el-input__inner {
      width: 82px;
      font-size: 12px;
      padding: 0 5px 0 10px;
    }
    .el-select__caret {
      font-size: 12px;
    }
    .el-input__suffix {
      right: 0;
    }
  }
  .el-input-group__append .el-button {
    margin: 0;
    padding: 7px 4px;
  }
  .el-icon-search {
    position: relative;
    width: 24px;
    margin: 0;
    bottom: unset;
    right: unset;
    font-size: 14px;
  }
  .el-input-group__append {
    padding: 0;
    background-color: transparent;
    border-left: none;
  }
}
</style>

import createEndpoint from './common/endpoint'

const client = createEndpoint({
  baseURL: process.env.ES_GATEWAY_BASE_URL
})

const { post, get } = client

/*doc
---
title: search
name: search
category: elasticsearch gateway
---

> https://www.elastic.co/guide/en/elasticsearch/client/javascript-api/current/api-reference.html#api-search

```
@options {
  index,
  type,
  body //query body
}
```
*/
export const search = async options => {
  return post('es/search', options)
}

/*doc
---
title: submit Git Data
name: submitGitData
category: elasticsearch gateway
---
| Parameter | Type   | Description |
| --------- | ----   | ----------- |
| path      | String | page url path. eg: chenqh/demo/index.md |
| action    | String | create, edit, or delete |
| content   | String | page content |
| options   | Object | extra options for specify services |

*/
export const submitGitData = async (path, action, content, options) => {
  return post('git/commit', { path, action, content, options })
}

export const projects = {
  getProjects: async args => get('projects', { params: args })
}

export const packages = {
  getPackages: async args => get('packages', { params: args })
}

export const users = {
  getUsers: async args => get('users', { params: args })
}

export const webpages = {
  getWebpages: async args => get('pages', { params: args })
}

export const suggestions = {
  getPrefixSuggestions: async args => get('suggestions', { params: args })
}

export default {
  search,
  submitGitData,
  projects,
  packages,
  users,
  webpages,
  suggestions
}


<template>
  <el-select class="user-pages-selector" v-model="selectedUrl" :size='size' @change='updateValue' slot="append" :placeholder="placeholderText" filterable allow-create>
    <el-option v-for="(path, pathIndex) in personalAllPagePathList" :key="pathIndex" :value="getLocationUrl(path)">
      {{ path }}
    </el-option>
  </el-select>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
export default {
  name: 'UserPagesSelector',
  props: {
    size: {
      type: String,
      default: 'medium'
    },
    placeholderText: String,
    emitData: Object
  },
  async mounted() {
    await this.getAllPersonalPageList()
  },
  data() {
    return {
      selectedUrl: ''
    }
  },
  computed: {
    ...mapGetters({
      personalAllPagePathList: 'user/personalAllPagePathList'
    })
  },
  methods: {
    ...mapActions({
      getAllPersonalPageList: 'user/getAllPersonalPageList'
    }),
    updateValue(newLink) {
      this.$emit('onChangeLink', {
        link: newLink,
        emitData: this.emitData
      })
    },
    getLocationUrl(url) {
      return url ? location.origin + '/' + url : ''
    }
  }
}
</script>

<template>
  <div class="user-sites-selector">
    <p class="user-sites-selector-info">{{$t('project.pleaseSelect')}}</p>
    <el-select v-model="selectSiteId" filterable>
      <el-option v-for="siteDetail in personalSiteList" :key="siteDetail.id" :label="siteDetail.displayName || siteDetail.sitename" :value="siteDetail.id">
      </el-option>
    </el-select>
  </div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
export default {
  name: 'UserSitesSelector',
  async mounted() {
    await this.userGetAllPersonalWebsite()
    this.selectSiteId = _.get(this.personalSiteList, '0.id')
  },
  data() {
    return {
      selectSiteId: undefined
    }
  },
  computed: {
    ...mapGetters({
      personalSiteList: 'user/personalSiteList'
    }),
    selectSiteDetail() {
      return _.find(this.personalSiteList, { id: this.selectSiteId })
    }
  },
  methods: {
    ...mapActions({
      userGetAllPersonalWebsite: 'user/getAllPersonalWebsite'
    })
  }
}
</script>

<template>
  <div class="ranking-list">
    <div class="ranking-list-banner"><img src="@/assets/pblImg/ranking_banner.png" alt="banner"></div>
    <div class="ranking-list-tab">
      <div class="ranking-list-tab-center">
        <el-menu :default-active="defaultActiveIndex" mode="horizontal" @select="handleSelect">
          <el-menu-item index="总榜">总榜</el-menu-item>
          <el-submenu index="NPL">
            <template slot="title">NPL大赛</template>
            <el-menu-item v-for="i in tabGamesList" :key="i.id" :index="i.id+''">{{gameNoState(i)}}</el-menu-item>
          </el-submenu>
        </el-menu>
      </div>
    </div>
    <div class="ranking-list-cabinet" v-loading="loading">
      <div class="ranking-list-cabinet-center">
        <div class="ranking-list-cabinet-center-hint">
          <div class="ranking-list-cabinet-center-hint-left">{{currentListName}}</div>
          <div class="ranking-list-cabinet-center-hint-right" v-if="currentListName == '总榜' ? false : true"><a href="/NPL">了解大赛详情</a></div>
        </div>
        <el-row>
          <el-col :sm="12" :md="6" :xs="12" v-for="(project,index) in showProjectsByTab" :key="index">
            <project-cell :project="project" :ranking='true' :level="index" :showProjectRate="showProjectRate"></project-cell>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>
<script>
import ProjectCell from './ProjectCell'
import _ from 'lodash'
import { keepwork } from '@/api'
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'RankingList',
  data() {
    return {
      loading: true,
      ranking: {},
      defaultActiveIndex: '总榜',
      activeIndex: ['总榜']
    }
  },
  computed: {
    ...mapGetters({
      gamesList: 'pbl/gamesList',
      gameWorks: 'pbl/gameWorks'
    }),
    currentListName() {
      if (this.activeIndex[0] === '总榜') {
        return '总榜'
      }
      if (this.activeIndex[0] === 'NPL') {
        for (let i = 0; i < this.tabGamesList.length; i++) {
          if (Number(this.activeIndex[1]) === this.tabGamesList[i].id) {
            return this.gameNoState(this.tabGamesList[i])
          }
        }
      }
      return '总榜'
    },
    tabGamesList() {
      const nowTime = new Date()
      return _.filter(_.get(this.gamesList, 'rows', []), i => {
        return (
          (nowTime > new Date(i.startDate) && nowTime < new Date(i.endDate)) ||
          nowTime > new Date(i.endDate)
        ) && i.type === 0  // type: 0  NPL大赛
      })
    },
    showProjectsByTab() {
      return this.activeIndex[0] === '总榜'
        ? this.rankingList
        : this.gameStagesWorks
    },
    showProjectRate() {
      return this.showProjectsByTab === this.rankingList ? true : false
    },
    rankingList() {
      return _.get(this.ranking, 'rows', [])
    },
    gameStagesWorks() {
      let list = _.get(this.gameWorks, 'rows', [])
      return _.filter(_.map(list, item => item.projects), v => v)
    }
  },
  async mounted() {
    await this.getRankingProjects()
    await this.getGamesList()
    this.loading = false
  },
  methods: {
    ...mapActions({
      getGamesList: 'pbl/getGamesList',
      getWorksByGameId: 'pbl/getWorksByGameId'
    }),
    gameNoState(i) {
      const nowTime = new Date()
      let state =
        nowTime < new Date(i.startDate)
          ? '未开始'
          : nowTime > new Date(i.startDate) && nowTime < new Date(i.endDate)
          ? '进行中'
          : '已结束'
      return `${i.name}第${i.no}期   （${state}）`
    },
    getRankingProjects() {
      keepwork.projects
        .getProjects({
          'x-order': 'rate-desc',
          'x-per-page': 100,
          type: 1,
          visibility: 0
        })
        .then(res => {
          this.ranking = res
        })
        .catch(e => {
          console.error(e)
        })
    },
    async handleSelect(key, keyPath) {
      this.loading = true
      this.activeIndex = keyPath
      if (key === '总榜') {
        await this.getRankingProjects()
        this.loading = false
      }
      await this.getWorksByGameId({ gameId: key })
      this.loading = false
    }
  },
  components: {
    ProjectCell
  }
}
</script>
<style lang="scss">
.ranking-list {
  &-banner {
    background: linear-gradient(to right, #6400d5, #7613d5);
    text-align: center;
    img {
      width: 100%;
      max-width: 1920px;
      object-fit: cover;
    }
  }
  &-tab {
    height: 60px;
    background: #ffffff;
    &-center {
      max-width: 1200px;
      margin: 0 auto;
      .el-dropdown-link {
        .right-icon {
          font-size: 12px;
        }
      }
    }
  }
  &-cabinet {
    min-height: 500px;
    &-center {
      max-width: 1200px;
      margin: 0 auto;
      &-hint {
        display: flex;
        margin: 20px 0;
        &-left {
          flex: 1;
          text-align: left;
          font-weight: 700;
        }
        &-right {
          flex: 1;
          text-align: right;
          a {
            text-decoration: none;
          }
        }
      }
    }
  }
}
</style>


```