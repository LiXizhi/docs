```javascript



  /**
  * @api {post} /projects/:encoded_project_path/files/:encoded_path create
  * @apiName CreateFile
  * @apiGroup File
  * @apiDescription To create a file
  * @apiPermission authorized user
  *
  * @apiParam {String} encoded_project_path Urlencoded encoded_project_path such as 'username%2Fsitename'
  * @apiParam {String} encoded_path Urlencoded tree path such as 'folder%2Ffolder'
  * @apiParam {String} [content] Content of the file
  */
  async create() {
    const { ctx } = this;
    ctx.validate(create_rule);
    const { path } = ctx.params;
    const project = await this.get_writable_project();
    await this.ensure_node_not_exist(project._id, path);
    const nodes_to_create = await ctx.model.Node
      .get_parents_not_exist(project.account_id, project._id, path);
    let file = {
      name: this.get_file_name(path),
      content: ctx.params.content,
      path,
      project_id: project._id,
      account_id: project.account_id,
    };

    nodes_to_create.push(file);
    const files = await ctx.model.Node
      .create(nodes_to_create);
    file = files[files.length - 1];

    const message_options = this.get_message_options(project);
    const message = await ctx.model.Message
      .create_file(file, project._id, message_options);

    await this.send_message(message);
    this.created();
  }


'use strict';

const Controller = require('../core/base_controller');

const create_rule = {
  id: 'int',
  username: { type: 'string', format: /^[a-zA-Z]/ },
  password: {
    type: 'password',
    min: 6,
  },
};

class AccountController extends Controller {
  /**
  * @api {get} /accounts get account
  * @apiName ShowAccount
  * @apiGroup Account
  * @apiDescription To get the information of an account
  * @apiPermission authorized user
  *
  * @apiParam {Number} id keepwork user id
  * @apiParam {String} username Username of the user
  * @apiParam {String{ > 6 }} password Password of the gitlab account
  */
  async show() {
    const { ctx, service } = this;
    ctx.verify();
    const kw_username = ctx.state.user.username;
    const account = await this.get_existing_account({ kw_username });
    if (!account.token) {
      account.token = await service.gitlab.get_token(account._id);
      await account.save().catch(err => {
        const errMsg = 'Failed to get token';
        ctx.logger.error(err);
        ctx.throw(err.response.status, errMsg);
      });
    }
    ctx.body = {
      git_id: account._id,
      git_username: account.name,
      token: account.token,
    };
  }

  /**
  * @api {post} /accounts create
  * @apiName CreateAccount
  * @apiGroup Account
  * @apiDescription To create a git account for a new keepwork user
  * @apiPermission admin
  *
  * @apiParam {Number} id keepwork user id
  * @apiParam {String} username Username of the user
  * @apiParam {String{ > 6 }} password Password of the gitlab account
  */
  async create() {
    const { ctx, service, config } = this;
    ctx.ensureAdmin();
    ctx.validate(create_rule);
    const kw_username = ctx.params.username;
    await this.ensure_account_not_exist({ kw_username });
    const account_prifix = config.gitlab.account_prifix;
    const email_postfix = config.gitlab.email_postfix;
    const account = await service.gitlab
      .create_account({
        username: `${account_prifix}${kw_username}`,
        name: kw_username,
        password: `kw${ctx.params.password}`,
        email: `${kw_username}${email_postfix}`,
      }).catch(err => {
        ctx.logger.error(err);
        ctx.throw(err.response.status);
      });
    await ctx.model.Account.create({
      _id: account._id,
      kw_id: ctx.params.id,
      name: account.username,
      kw_username,
    }).catch(err => {
      ctx.logger.error(err);
      throw err;
    });
    this.created();
  }

  /**
  * @api {delete} /accounts/:username remove
  * @apiName RemoveAccount
  * @apiGroup Account
  * @apiDescription To remove an account
  * @apiPermission admin
  *
  * @apiParam {String} username Username of the user
  */
  async remove() {
    const { ctx, service } = this;
    ctx.ensureAdmin();
    const account = await this.get_existing_account({
      kw_username: ctx.params.kw_username,
    });

    await ctx.model.Node
      .delete_account(account._id)
      .catch(err => {
        ctx.logger.error(err);
        ctx.throw(500);
      });

    await ctx.model.Project
      .delete_account(account._id)
      .catch(err => {
        ctx.logger.error(err);
        ctx.throw(500);
      });

    await service.gitlab
      .delete_account(account._id)
      .catch(err => {
        ctx.logger.error(err);
        ctx.throw(err.response.status);
      });
    await ctx.model.Account
      .remove_by_query({ _id: account._id })
      .catch(err => {
        ctx.logger.error(err);
        ctx.throw(500);
      });
    this.deleted();
  }

  async ensure_account_not_exist(query) {
    const account = await this.get_account(query);
    this.throw_if_exists(account, 'Account already exists');
  }
}

module.exports = AccountController;


'use strict';

const Controller = require('./node');
const _ = require('lodash/object');

const DEFAULT_BRANCH = 'master';
const PENDING_TIP = 'pending';
const ERROR_COMMIT_PENDING = 'Commit is pending';
const CODE_NOT_FOUND = 404;
const LATEST_FIELDS_TO_SHOW = [ 'version', 'source_version', 'createdAt' ];

const create_rule = {
  branch: { type: 'string', default: 'master', required: false },
  content: { type: 'string', required: false, allowEmpty: true },
  commit_message: { type: 'string', required: false },
  encoding: {
    type: 'enum',
    values: [ 'text', 'base64' ],
    default: 'text',
    required: false,
  },
};

const create_many_rule = {
  branch: { type: 'string', default: 'master', required: false },
  files: {
    type: 'array',
    itemType: 'object',
    rule: {
      path: 'string',
      content: { type: 'string', required: false, allowEmpty: true },
    },
  },
  commit_message: { type: 'string', required: false },
  encoding: {
    type: 'enum',
    values: [ 'text', 'base64' ],
    default: 'text',
    required: false,
  },
};

const update_rule = {
  branch: { type: 'string', default: 'master', required: false },
  content: { type: 'string', allowEmpty: true },
  commit_message: { type: 'string', required: false },
  encoding: {
    type: 'enum',
    values: [ 'text', 'base64' ],
    default: 'text',
    required: false,
  },
};

const move_rule = {
  new_path: 'string',
  branch: { type: 'string', default: 'master', required: false },
  content: { type: 'string', required: false, allowEmpty: true },
  commit_message: { type: 'string', required: false },
  encoding: {
    type: 'enum',
    values: [ 'text', 'base64' ],
    default: 'text',
    required: false,
  },
};

class FileController extends Controller {
  /**
  * @api {get} /projects/:encoded_project_path/files/:encoded_path get
  * @apiName GetFile
  * @apiGroup File
  * @apiDescription To get a file
  * @apiPermission authorized user
  *
  * @apiParam {String} encoded_project_path Urlencoded encoded_project_path such as 'username%2Fsitename'
  * @apiParam {String} encoded_path Urlencoded tree path such as 'folder%2Ffolder'
  * @apiParam {Boolean} [refresh_cache=false]  Whether refresh the cache of this file
  */
  async show() {
    const { ctx, service } = this;
    const { path, refresh_cache, ref = DEFAULT_BRANCH, commit } = ctx.params;

    let project;
    if (commit) {
      project = await this.get_writable_project();
    } else {
      project = await this.get_readable_project();
    }

    const from_cache = !refresh_cache;
    let file;
    if (ref !== DEFAULT_BRANCH) {
      if (ref === PENDING_TIP) ctx.throw(CODE_NOT_FOUND, ERROR_COMMIT_PENDING);
      file = await service.gitlab.load_file(project._id, path, ref)
        .catch(err => {
          if (err.response.status === CODE_NOT_FOUND) {
            ctx.throw(err.response.status, err.response.data.message);
          }
        });
    } else {
      file = await this.get_node(project._id, path, from_cache);
      file = file || await this.load_from_gitlab(project);
    }

    if (commit && !file.latest_commit) {
      file = await service.node.getFileWithCommits(file);
    }

    ctx.body = {
      _id: file._id,
      content: file.content || '',
    };

    if (commit) {
      ctx.body.commit = _.pick(file.latest_commit, LATEST_FIELDS_TO_SHOW);
    }
  }

  /**
  * @api {post} /projects/:encoded_project_path/files/:encoded_path create
  * @apiName CreateFile
  * @apiGroup File
  * @apiDescription To create a file
  * @apiPermission authorized user
  *
  * @apiParam {String} encoded_project_path Urlencoded encoded_project_path such as 'username%2Fsitename'
  * @apiParam {String} encoded_path Urlencoded tree path such as 'folder%2Ffolder'
  * @apiParam {String} [content] Content of the file
  */
  async create() {
    const { ctx } = this;
    ctx.validate(create_rule);
    const { path } = ctx.params;
    const project = await this.get_writable_project();
    await this.ensure_node_not_exist(project._id, path);
    const nodes_to_create = await ctx.model.Node
      .get_parents_not_exist(project.account_id, project._id, path);
    let file = {
      name: this.get_file_name(path),
      content: ctx.params.content,
      path,
      project_id: project._id,
      account_id: project.account_id,
    };

    nodes_to_create.push(file);
    const files = await ctx.model.Node
      .create(nodes_to_create);
    file = files[files.length - 1];

    const message_options = this.get_message_options(project);
    const message = await ctx.model.Message
      .create_file(file, project._id, message_options);

    await this.send_message(message);
    this.created();
  }

  async create_many() {
    const { ctx } = this;
    ctx.validate(create_many_rule);
    const project = await this.get_writable_project();
    let { files } = ctx.params;
    this.ensure_unique(files);
    await this.ensure_nodes_not_exist(project._id, files);
    const ancestors_to_create = await ctx.model.Node
      .get_parents_not_exist(project.account_id, project._id, files);
    for (const file of files) {
      file.name = this.get_file_name(file.path);
      file.project_id = project._id;
      file.account_id = project.account_id;
    }

    const nodes_to_create = files.concat(ancestors_to_create);
    files = await ctx.model.Node
      .create(nodes_to_create);

    const message_options = this.get_message_options(project);
    const message = await ctx.model.Message
      .create_file(files, project._id, message_options);

    await this.send_message(message);
    this.created();
  }

  /**
  * @api {put} /projects/:encoded_project_path/files/:encoded_path update
  * @apiName UpdateFile
  * @apiGroup File
  * @apiDescription To update a file
  * @apiPermission authorized user
  *
  * @apiParam {String} encoded_project_path Urlencoded encoded_project_path such as 'username%2Fsitename'
  * @apiParam {String} encoded_path Urlencoded tree path such as 'folder%2Ffolder'
  * @apiParam {String} content Content of the file
  */
  async update() {
    const { ctx, service } = this;
    ctx.validate(update_rule);
    const { path, source_version } = ctx.params;
    const project = await this.get_readable_project();
    let file = await this.get_existing_node(project._id, path, false);
    file = await service.node.getFileWithCommits(file);

    file.set({ content: ctx.params.content });
    file.createCommit({ author_name: ctx.state.user.username, source_version });
    await file.save();

    const message_options = this.get_message_options(project);
    const message = await ctx.model.Message
      .update_file(file, project._id, message_options);

    await this.send_message(message);
    this.updated({ commit: _.pick(file.latest_commit, LATEST_FIELDS_TO_SHOW) });
  }

  /**
  * @api {delete} /projects/:encoded_project_path/files/:encoded_path remove
  * @apiName RemoveFile
  * @apiGroup File
  * @apiDescription To remove a file
  * @apiPermission authorized
  *
  * @apiParam {String} encoded_project_path Urlencoded encoded_project_path such as 'username%2Fsitename'
  * @apiParam {String} encoded_path Urlencoded tree path such as 'folder%2Ffolder'
  */
  async remove() {
    const { ctx } = this;
    const { path } = ctx.params;
    const project = await this.get_writable_project();
    const file = await this.get_existing_node(project._id, path, false);

    await ctx.model.Node
      .delete_and_release_cache(file);

    const message_options = this.get_message_options(project);
    const message = await ctx.model.Message
      .delete_file(file, project._id, message_options);

    await this.send_message(message);
    this.deleted();
  }

  /**
  * @api {put} /projects/:encoded_project_path/files/:encoded_path/move move
  * @apiName MoveFile
  * @apiGroup File
  * @apiDescription To move a file
  * @apiPermission authorized user
  *
  * @apiParam {String} encoded_project_path Urlencoded encoded_project_path such as 'username%2Fsitename'
  * @apiParam {String} encoded_path Urlencoded tree path such as 'username%2Fsitename%2Fprevious%2Findex.md'
  * @apiParam {String} new_path New path of the file such as 'username/sitename/new/index.md'
  * @apiParam {String} [content] Content of the file
  */
  async move() {
    const { ctx, service } = this;
    ctx.validate(move_rule);
    const previous_path = ctx.params.path;
    const new_path = ctx.params.path = ctx.params.new_path;
    const project = await this.get_writable_project();
    let file = await this.get_existing_node(project._id, previous_path, false);
    file = await service.node.getFileWithCommits(file);
    await this.ensure_node_not_exist(project._id, new_path);
    await this.ensure_parent_exist(project.account_id, project._id, new_path);
    file = await service.node.getFileWithCommits(file);

    const { content } = ctx.params;
    if (content) { file.content = content; }
    file.previous_path = previous_path;
    file.path = new_path;
    file.previous_name = file.name;
    file.name = this.get_file_name();

    file.createCommit({ author_name: ctx.state.user.username });
    await ctx.model.Node.move(file);

    const message_options = this.get_message_options(project);
    const message = await ctx.model.Message
      .move_file(file, project._id, message_options);

    await this.send_message(message);
    this.moved();
  }

  async load_from_gitlab(project) {
    const { ctx, service } = this;
    if (!project) { project = await this.get_existing_project(); }
    const file = await service.gitlab
      .load_raw_file(project.git_path, ctx.params.path)
      .catch(err => {
        ctx.logger.error(err);
        if (err.response.status === CODE_NOT_FOUND) {
          this.throw_if_node_not_exist();
        }
        ctx.throw(500);
      });
    file.path = ctx.params.path;
    file.name = this.get_file_name(file.path);
    file.project_id = project._id;
    file.account_id = project.account_id;
    await ctx.model.Node.create(file);
    return file;
  }
}

module.exports = FileController;


'use strict';

const Controller = require('./node');

const create_rule = {
  branch: { type: 'string', default: 'master', required: false },
  commit_message: { type: 'string', required: false },
  encoding: {
    type: 'enum',
    values: [ 'text', 'base64' ],
    default: 'text',
    required: false,
  },
};

const move_rule = {
  new_path: 'string',
  branch: { type: 'string', default: 'master', required: false },
  content: { type: 'string', required: false },
  commit_message: { type: 'string', required: false },
  encoding: {
    type: 'enum',
    values: [ 'text', 'base64' ],
    default: 'text',
    required: false,
  },
};

class FolderController extends Controller {
  /**
  * @api {post} /projects/:encoded_project_path/folders/:encoded_path create
  * @apiName CreateFolder
  * @apiGroup Folder
  * @apiDescription To create a folder
  * @apiPermission authorized user
  *
  * @apiParam {String} encoded_project_path Urlencoded encoded_project_path such as 'username%2Fsitename'
  * @apiParam {String} encoded_path Urlencoded tree path such as 'folder%2Ffolder'
  */
  async create() {
    const { ctx } = this;
    ctx.validate(create_rule);
    const path = ctx.params.path;
    const project = await this.get_writable_project();
    await this.ensure_node_not_exist(project._id, path);
    await this.ensure_parent_exist(project.account_id, project._id, path);
    const folder = new ctx.model.Node({
      name: this.get_file_name(path),
      type: 'tree',
      path,
      project_id: project._id,
      account_id: project.account_id,
    });

    await folder.save();
    this.created();
  }

  /**
  * @api {delete} /projects/:encoded_project_path/folders/:encoded_path remove
  * @apiName RemoveFolder
  * @apiGroup Folder
  * @apiDescription To remove a folder and all of its sub files
  * @apiPermission authorized user
  *
  * @apiParam {String} encoded_project_path Urlencoded encoded_project_path such as 'username%2Fsitename'
  * @apiParam {String} encoded_path Urlencoded tree path such as 'folder%2Ffolder'
  */
  async remove() {
    const { ctx } = this;
    const path = ctx.params.path;
    const project = await this.get_writable_project();
    const folder = await this.get_existing_node(project._id, path, false);
    const subfiles = await ctx.model.Node
      .get_tree_by_path_from_db(
        project._id,
        ctx.params.path,
        true,
        { skip: 0, limit: 9999999 }
      );
    subfiles.push(folder);

    const message_options = {
      commit_message: ctx.params.commit_message ||
        `${ctx.state.user.username} delete folder ${folder.path}`,
      author: ctx.state.user.username,
      visibility: project.visibility,
    };

    const message = await ctx.model.Message
      .delete_file(subfiles, project._id, message_options);

    await ctx.model.Node
      .delete_subfiles_and_release_cache(project._id, folder.path, subfiles);

    await this.send_message(message);
    this.deleted();
  }

  /**
  * @api {put} /projects/:encoded_project_path/folders/:encoded_path/move move
  * @apiName MoveFolder
  * @apiGroup Folder
  * @apiDescription To move a folder
  * @apiPermission authorized user
  *
  * @apiParam {String} encoded_project_path Urlencoded encoded_project_path such as 'username%2Fsitename'
  * @apiParam {String} encoded_path Urlencoded folder path such as 'username%2Fsitename%2Fprevious'
  * @apiParam {String} new_path New path of the folder such as 'username/sitename/new'
  */
  async move() {
    const { ctx, service } = this;
    ctx.validate(move_rule);
    const previous_path = ctx.params.path;
    const new_path = ctx.params.path = ctx.params.new_path;
    const project = await this.get_writable_project();
    const folder = await this.get_existing_node(project._id, previous_path, false);
    await this.ensure_node_not_exist(project._id, new_path);
    await this.ensure_parent_exist(project.account_id, project._id, new_path);

    folder.path = new_path;
    folder.previous_path = previous_path;
    folder.previous_name = folder.name;
    folder.name = this.get_file_name();

    let subfiles = await ctx.model.Node
      .get_subfiles_by_path(project._id, previous_path, null, false);

    subfiles = Promise.all(subfiles.map(file => {
      return service.node.getFileWithCommits(file);
    }));

    const pattern = new RegExp(`^${previous_path}`, 'u');
    for (const file of subfiles) {
      file.previous_path = file.path;
      file.path = file.path.replace(pattern, new_path);
    }
    subfiles.push(folder);

    const tasks = subfiles.map(file => {
      file.createCommit({ author: ctx.state.user.username });
      return file.save();
    });
    await Promise.all(tasks);

    const message_options = this.get_message_options(project);
    const message = await ctx.model.Message
      .move_file(subfiles, project._id, message_options);

    await this.send_message(message);
    this.moved();
  }
}

module.exports = FolderController;


'use strict';

const Controller = require('../core/base_controller');

class HomeController extends Controller {
  async index() {
    this.ctx.body = 'Hello, git-gateway';
  }
}

module.exports = HomeController;


'use strict';

const Controller = require('../core/base_controller');

class NodeController extends Controller {
  async clear_project() {
    const { ctx } = this;
    ctx.ensureAdmin();
    const project = await this.get_project();
    await ctx.model.Node
      .delete_project(project._id)
      .catch(err => {
        ctx.logger.error(err);
        ctx.throw(500);
      });
    this.deleted();
  }

  wrap_message(message) {
    const { ctx } = this;
    const { helper } = ctx;
    const key = message.project_id;
    const topics = this.config.kafka.topics;
    const git_message = {
      messages: message._id,
      topic: topics.commit,
      key,
    };
    const es_message = {
      messages: helper.commit_to_message(message),
      topic: topics.elasticsearch,
      key,
    };
    return [ git_message, es_message ];
  }

  async send_message(message) {
    const { ctx, service } = this;
    const payloads = this.wrap_message(message);
    await service.kafka.send(payloads)
      .catch(err => {
        ctx.logger.error(err);
      });
  }

  get_file_name(path) {
    const { ctx } = this;
    path = path || ctx.params.path;
    return ctx.model.Node.get_file_name(path);
  }

  validate_file_path(path) {
    const { ctx } = this;
    path = path || ctx.params.path;
    const pattern = /\.[^\.]+$/;
    if (!pattern.test(path)) { ctx.throw(400, 'Path of the file must end with .xxx'); }
  }

  async get_node(project_id, path, from_cache) {
    const { ctx } = this;
    path = path || ctx.params.path;
    const node = await ctx.model.Node
      .get_by_path(project_id, path, from_cache)
      .catch(err => {
        ctx.logger.error(err);
        ctx.throw(500);
      });
    return node;
  }

  async get_existing_node(project_id, path, from_cache) {
    const node = await this.get_node(project_id, path, from_cache);
    this.throw_if_node_not_exist(node);
    return node;
  }

  throw_if_node_not_exist(node) {
    this.throw_if_not_exist(node, 'File or folder not found');
  }

  throw_if_node_exists(node) {
    this.throw_if_exists(node, 'File or folder already exists');
  }

  async ensure_node_not_exist(project_id, path, from_cache) {
    const node = await this.get_node(project_id, path, from_cache);
    this.throw_if_node_exists(node);
    return node;
  }

  async ensure_nodes_not_exist(project_id, files, from_cache) {
    for (const file of files) {
      await this.ensure_node_not_exist(project_id, file.path, from_cache);
    }
  }

  ensure_unique(files) {
    const { ctx } = this;
    const exist_paths = {};
    const errMsg = 'Reduplicative files exist in your request';
    for (const file of files) {
      if (exist_paths[file.path]) { ctx.throw(409, errMsg); }
      exist_paths[file.path] = true;
    }
  }

  async ensure_parent_exist(account_id, project_id, path) {
    const { ctx } = this;
    path = path || ctx.params.path;
    await ctx.model.Node
      .ensure_parent_exist(account_id, project_id, path)
      .catch(err => {
        ctx.logger.error(err);
        ctx.throw(500);
      });
  }

  async ensure_parents_exist(account_id, project_id, files) {
    const { ctx } = this;
    for (const file of files) {
      await ctx.model.Node.ensure_parent_exist(
        account_id, project_id, file.path
      );
    }
  }

  get_message_options(project) {
    const { ctx } = this;
    const { commit_message, source_version, encoding } = ctx.params;
    return {
      source_version,
      commit_message,
      encoding,
      author: ctx.state.user.username,
      visibility: project.visibility,
    };
  }
}

module.exports = NodeController;


'use strict';

const Controller = require('../core/base_controller');

const create_rule = {
  sitename: 'string',
  site_id: { type: 'int', required: false },
  visibility: [ 'public', 'private' ],
};

const update_visibility_rule = {
  visibility: [ 'public', 'private' ],
};

class ProjectController extends Controller {
  /**
 * @api {get} /projects/:encoded_path/exist check existence
 * @apiName exist
 * @apiGroup Project
 * @apiDescription To check the existence of a project
 * @apiPermission admin
 *
 * @apiParam {String} encoded_path Urlencoded path of a project.Like 'username%2Fproject_name'
 */
  async exist() {
    const { ctx } = this;
    ctx.ensureAdmin();
    const project = await this.get_project(ctx.params.path);
    if (ctx.helper.empty(project)) {
      ctx.body = 0;
    } else {
      ctx.body = 1;
    }
  }

  /**
 * @api {post} /projects/user/:username create
 * @apiName CreateProject
 * @apiGroup Project
 * @apiDescription To create a git project
 * @apiPermission admin
 *
 * @apiParam {String} username Username of the project owner
 * @apiParam {String} sitename Name of the website
 * @apiParam {String{public, private}} visibility Visibility of the project
 * @apiParam {Number} [site_id] Id of the website in keepwork.When the
 * project is bound to a website,it is required.
 */
  async create() {
    const { ctx, service } = this;
    ctx.ensureAdmin();
    ctx.validate(create_rule);
    const kw_username = ctx.params.kw_username;
    const sitename = ctx.params.sitename;
    const project_path = `${kw_username}/${sitename}`;
    const account = await this.get_existing_account({ kw_username });
    await this.ensure_project_not_exist(project_path);
    const project = await service.gitlab
      .create_project({
        name: sitename,
        visibility: ctx.params.visibility,
        account_id: account._id,
      }).catch(err => {
        ctx.logger.error(err);
        ctx.throw(err.response.status, err.response.data);
      });
    project.sitename = sitename;
    project.path = project_path;
    project.site_id = ctx.params.site_id;
    await ctx.model.Project
      .create(project)
      .catch(err => {
        ctx.logger.error(err);
        ctx.throw(500);
      });
    this.created();
  }

  /**
 * @api {put} /projects/:encoded_path/visibility update visibility
 * @apiName UpdateVisibility
 * @apiGroup Project
 * @apiDescription To update the visibility of a project
 * @apiPermission admin
 *
 * @apiParam {String} encoded_path Urlencoded path of a project.Like 'username%2Fproject_name'
 * @apiParam {String="public", "private"} visibility Visibility of the website
 */
  async update_visibility() {
    const { ctx, service } = this;
    ctx.ensureAdmin();
    ctx.validate(update_visibility_rule);
    const project = await this.get_existing_project(ctx.params.path, false);
    project.visibility = ctx.params.visibility;
    await service.gitlab
      .update_project_visibility(project._id, project.visibility)
      .catch(err => {
        ctx.logger.error(err);
        ctx.throw(500);
      });

    await project.save().catch(err => {
      ctx.logger.error(err);
      ctx.throw(500);
    });

    if (project.site_id) {
      const method_to_call = 'updateSiteVisibility';
      await this.send_message(project, method_to_call);
    }

    ctx.body = {
      site_id: project.site_id,
      visibility: project.visibility,
    };
  }

  /**
 * @api {delete} /projects/:encoded_path remove
 * @apiName RemoveProject
 * @apiGroup Project
 * @apiDescription To remove a project
 * @apiPermission admin
 *
 * @apiParam {String} encoded_path Urlencoded path of a project.Like 'username%2Fproject_name'
 */
  async remove() {
    const { ctx, service } = this;
    ctx.ensureAdmin();
    const project = await this.get_existing_project(ctx.params.path, false);
    await ctx.model.Node
      .delete_project(project._id)
      .catch(err => {
        ctx.logger.error(err);
        ctx.throw(500);
      });

    await service.gitlab
      .delete_project(project._id)
      .catch(err => {
        ctx.logger.error(err);
        ctx.throw(500);
      });

    await ctx.model.Project
      .delete_and_release_cache(project.path)
      .catch(err => {
        ctx.logger.error(err);
        ctx.throw(500);
      });

    if (project.site_id) {
      const method_to_call = 'deleteSite';
      await this.send_message(project, method_to_call);
    }

    this.deleted();
  }

  async getCommits() {
    const { ctx, service } = this;
    const { path, file_path } = ctx.params;
    const { skip, limit } = ctx.helper.paginate(ctx.params);
    const project = await this.get_readable_project(path, false);
    ctx.body = await service.node.getCommits(project._id, file_path, skip, limit);
  }

  async ensure_project_not_exist(project_path) {
    const project = await this.get_project(project_path);
    this.throw_if_exists(project, 'Project already exists');
  }

  wrap_message(project, method) {
    const { ctx } = this;
    const { helper } = ctx;
    return {
      topic: this.config.kafka.topics.elasticsearch,
      messages: helper.project_to_message(project, method),
      key: project._id,
    };
  }

  async send_message(project, method) {
    const { ctx, service } = this;
    const payload = this.wrap_message(project, method);
    await service.kafka.send(payload)
      .catch(err => {
        ctx.logger.error(err);
      });
  }
}

module.exports = ProjectController;


'use strict';

const Controller = require('./node');
const { paginate } = require('../lib/helper');

class TreeController extends Controller {
  /**
  * @api {get} /projects/:encoded_project_path/tree/:encoded_path get
  * @apiName GetTree
  * @apiGroup Tree
  * @apiDescription To get a tree
  * @apiPermission anyone
  *
  * @apiParam {String} encoded_project_path Urlencoded encoded_project_path such as 'username%2Fsitename'
  * @apiParam {String} encoded_path Urlencoded tree path such as 'folder%2Ffolder'
  * @apiParam {Boolean} [recursive=false] Whether get all sub tree
  * @apiParam {Number} [page=1] Page number, only works if recursive = true
  * @apiParam {Number} [per_page=20] Items amount for a page, only works if recursive = true
  * @apiParam {Boolean} [refresh_cache=false]  Whether refresh the cache of this tree
  */
  async show() {
    const { ctx } = this;
    const from_cache = !ctx.params.refresh_cache;
    const recursive = ctx.params.recursive;
    const project = await this.get_existing_project(ctx.params.project_path);
    const tree = await ctx.model.Node
      .get_tree_by_path(
        project._id,
        ctx.params.path,
        from_cache,
        recursive,
        paginate(ctx.params)
      );
    ctx.body = tree;
  }

  async root() {
    const { ctx } = this;
    const project = await this.get_existing_project(ctx.params.project_path);
    const tree = await ctx.model.Node
      .get_tree_by_path(
        project._id,
        null,
        false,
        true,
        paginate(ctx.params)
      );
    ctx.body = tree;
  }
}

module.exports = TreeController;


'use strict';

const Controller = require('egg').Controller;

class Base_controllerController extends Controller {
  async get_account(query) {
    const { ctx } = this;
    const account = await ctx.model.Account
      .get_by_query(query)
      .catch(err => {
        ctx.logger.error(err);
        ctx.throw(500);
      });
    return account;
  }

  async get_existing_account(query) {
    const account = await this.get_account(query);
    this.throw_if_not_exist(account, 'Account not found');
    return account;
  }

  async get_project(project_path, from_cache) {
    const { ctx } = this;
    project_path = project_path || ctx.params.project_path;
    const project = await ctx.model.Project
      .get_by_path(project_path, from_cache)
      .catch(err => {
        ctx.logger.error(err);
        ctx.throw(500);
      });
    return project;
  }

  async get_existing_project(project_path, from_cache) {
    const project = await this.get_project(project_path, from_cache);
    this.throw_if_not_exist(project, 'Project not found');
    return project;
  }

  async get_readable_project(project_path, from_cache) {
    const { ctx, config } = this;
    project_path = project_path || ctx.params.project_path;
    const project = await this.get_existing_project(project_path, from_cache);
    const white_list = config.file.white_list;
    const must_ensure = (!(white_list.includes(project.sitename)))
      && (project.visibility === 'private');
    if (must_ensure) {
      await ctx.ensurePermission(project.site_id, 'r');
    }
    return project;
  }

  async get_writable_project(project_path, from_cache) {
    const { ctx } = this;
    project_path = project_path || ctx.params.project_path;
    const project = await this.get_existing_project(project_path, from_cache);
    const username = ctx.state.user.username;
    if (this.own_this_project(username, project_path)) {
      await ctx.validateToken();
    } else {
      await ctx.ensurePermission(project.site_id, 'rw');
    }
    return project;
  }

  own_this_project(username, project_path) {
    return project_path.startsWith(`${username}/`);
  }

  throw_if_exists(object, errMsg) {
    const { ctx } = this;
    if (!ctx.helper.empty(object)) { ctx.throw(409, errMsg); }
  }

  throw_if_not_exist(object, errMsg) {
    const { ctx } = this;
    if (ctx.helper.empty(object)) { ctx.throw(404, errMsg); }
  }

  success(action = 'success', extraMsg = {}) {
    const { ctx } = this;
    extraMsg[action] = true;
    ctx.body = extraMsg;
  }

  created(extraMsg) {
    this.ctx.status = 201;
    this.success('created', extraMsg);
  }

  updated(extraMsg) {
    this.success('updated', extraMsg);
  }

  deleted(extraMsg) {
    this.success('deleted', extraMsg);
  }

  moved(extraMsg) {
    this.success('moved', extraMsg);
  }
}

module.exports = Base_controllerController;


'use strict';

const { empty } = require('../lib/helper');

const isAdmin = user => {
  return user.roleId === 10;
};

module.exports = {
  verify() {
    let errMsg;
    this.state = this.state || {};
    if (empty(this.state.user)) {
      errMsg = 'Valid authorization token was required';
    } else if (!this.state.user.userId || !this.state.user.username) {
      errMsg = 'Invalid token';
    }
    if (errMsg) { this.throw(401, errMsg); }
  },
  async ensurePermission(site_id, type) {
    this.verify();
    if (isAdmin(this.state.user)) { return; }
    const token = this.headers.authorization;
    const permitted = await this.service.keepwork
      .ensurePermission(token, site_id, type);
    if (!permitted) {
      const errMsg = 'Not allowed to access this protected resource';
      this.throw(403, errMsg);
    }
  },
  ensureAdmin() {
    const errMsg = 'Not allowed to access this protected resource';
    this.state = this.state || {};
    this.state.user = this.state.user || {};
    const not_permitted = empty(this.state.user) || !isAdmin(this.state.user);
    if (not_permitted) { this.throw(403, errMsg); }
  },
  async validateToken() {
    this.verify();
    const token = this.headers.authorization;
    await this.service.keepwork
      .getUserProfile(token)
      .catch(err => {
        this.ctx.logger.error(err);
        const errMsg = 'Invalid token';
        this.throw(401, errMsg);
      });
    return true;
  },
};


'use strict';

const Helper = require('../lib/helper');

module.exports = Helper;


'use strict';

const Stringifier = require('./stringifier');

class Helper {
  static generate_file_key(project_id, path) {
    return `project:${project_id}:file:${path}`;
  }

  static generate_tree_key(project_id, path) {
    return `project:${project_id}:tree:${path}`;
  }

  static generate_project_key(path) {
    return `project:${path}`;
  }

  static generate_account_key(kw_username) {
    return `account:${kw_username}`;
  }

  static project_to_message(project, method) {
    return Stringifier.stringify_project({
      _id: project._id,
      visibility: project.visibility,
      path: project.path,
      method,
    });
  }

  static getCommitsRecordKey(project_id, path) {
    let key = `project:${project_id}`;
    if (path) key += `:file:${path}`;
    key += ':commits';
    return key;
  }

  static commit_to_message(message) {
    return Stringifier.stringify_commit(message);
  }

  static serilize_file(file) {
    return Stringifier.stringify_file(file);
  }

  static serilize_tree(tree) {
    return Stringifier.stringify_tree(tree);
  }

  static serilizeCommitRecord(message) {
    return Stringifier.stringifyCommitRecord(message);
  }

  static empty(obj) {
    if (!obj) { return true; }
    if (Object.keys(obj).length === 0) {
      return true;
    }
    return false;
  }

  static paginate(query) {
    const limit = Number(query.per_page) || 10000;
    const page = Number(query.page) || 1;
    const skip = (page - 1) * limit;
    return { skip, limit };
  }
}

module.exports = Helper;


'use strict';

class MessageFormatter {
  static output(actions, project_id, options) {
    return {
      branch: options.branch || 'master',
      visibility: options.visibility,
      project_id,
      author_name: options.author || null,
      commit_message: options.commit_message,
      source_version: options.source_version,
      actions,
    };
  }

  static format_create_action(file, options) {
    return {
      _id: file._id,
      action: 'create',
      file_path: file.path,
      content: file.content,
      encoding: options.encoding || 'text',
    };
  }

  static format_update_action(file, options) {
    file.latest_commit = file.latest_commit || {};
    const { version } = file.latest_commit;
    return {
      _id: file._id,
      action: 'update',
      file_path: file.path,
      content: file.content,
      encoding: options.encoding || 'text',
      version,
    };
  }

  static format_delete_action(file) {
    const file_path = file.path;
    return {
      _id: file._id,
      action: 'delete',
      file_path,
    };
  }

  static format_move_action(file, options) {
    file.latest_commit = file.latest_commit || {};
    const { version } = file.latest_commit;
    return {
      _id: file._id,
      action: 'move',
      file_path: file.path,
      previous_path: file.previous_path,
      encoding: options.encoding || 'text',
      content: file.content,
      version,
    };
  }

  static format_actions(files, action_formatter, options) {
    let actions;
    if (files instanceof Array) {
      actions = [];
      for (const file of files) {
        if (file.type === 'tree') { continue; }
        actions.push(action_formatter(file, options));
      }
    } else {
      actions = [ action_formatter(files, options) ];
    }
    return actions;
  }

  static create_file(files, project_id, options) {
    const actions = this.format_actions(files, this.format_create_action, options);
    let default_message = `${options.author} create file ${files.path}`;
    if (files instanceof Array) { default_message = `${options.author} create files`; }
    options.commit_message = options.commit_message || default_message;
    return this.output(actions, project_id, options);
  }

  static update_file(files, project_id, options) {
    const actions = this.format_actions(files, this.format_update_action, options);
    let default_message = `${options.author} update file ${files.path}`;
    if (files instanceof Array) { default_message = `${options.author} update files`; }
    options.commit_message = options.commit_message || default_message;
    return this.output(actions, project_id, options);
  }

  static delete_file(files, project_id, options) {
    const actions = this.format_actions(files, this.format_delete_action, options);
    let default_message = `${options.author} delete file ${files.path}`;
    if (files instanceof Array) { default_message = `${options.author} delete files`; }
    options.commit_message = options.commit_message || default_message;
    return this.output(actions, project_id, options);
  }

  static move_file(files, project_id, options) {
    const actions = this.format_actions(files, this.format_move_action, options);
    let default_message =
      `${options.author} move file from ${files.previous_path} to ${files.path}`;
    if (files instanceof Array) { default_message = `${options.author} move files`; }
    options.commit_message = options.commit_message || default_message;
    return this.output(actions, project_id, options);
  }
}

module.exports = MessageFormatter;


'use strict';

const fast_JSON = require('fast-json-stringify');

const stringify_commit = fast_JSON({
  title: 'stringify commit message',
  type: 'object',
  properties: {
    project_id: { type: 'string' },
    createdAt: { type: 'string' },
    visibility: { type: 'string' },
    actions: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          _id: { type: 'string' },
          action: { type: 'string' },
          file_path: { type: 'string' },
          previous_path: { type: 'string' },
          content: { type: 'string' },
        },
      },
    },
  },
});

const stringifyCommitRecord = fast_JSON({
  title: 'stringify commit record',
  type: 'object',
  properties: {
    short_id: { type: 'string' },
    author_name: { type: 'string' },
    authored_date: { type: 'string' },
    created_at: { type: 'string' },
    message: { type: 'string' },
    version: { type: 'number' },
  },
});

const stringify_project = fast_JSON({
  title: 'stringify project',
  type: 'object',
  properties: {
    _id: { type: 'string' },
    visibility: { type: 'string' },
    path: { type: 'string' },
    method: { type: 'string' },
  },
});

const stringify_file = fast_JSON({
  title: 'stringify file',
  type: 'object',
  properties: {
    _id: { type: 'string' },
    path: { type: 'string' },
    type: { type: 'string' },
    content: { type: 'string' },
    latest_commit: {
      type: 'object',
      properties: {
        _id: { type: 'string' },
        commit_id: { type: 'string' },
        short_id: { type: 'string' },
        version: { type: 'number' },
        author_name: { type: 'string' },
        source_version: { type: 'number' },
        message: { type: 'string' },
        createdAt: { type: 'string' },
      } },
  },
});

const stringify_tree = fast_JSON({
  title: 'stringify tree',
  type: 'array',
  items: {
    type: 'object',
    properties: {
      _id: { type: 'string' },
      name: { type: 'string' },
      type: { type: 'string' },
      path: { type: 'string' },
    },
  },
});

module.exports = {
  stringify_commit,
  stringifyCommitRecord,
  stringify_project,
  stringify_file,
  stringify_tree,
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

const { empty } = require('../lib/helper');

module.exports = app => {
  const mongoose = app.mongoose;
  const Schema = mongoose.Schema;
  const logger = app.logger;

  const AccountSchema = new Schema({
    _id: Number,
    name: String,
    kw_id: Number,
    kw_username: { type: String, unique: true },
    token: String,
  }, { timestamps: true });

  const statics = AccountSchema.statics;

  statics.get_by_query = async function(query) {
    const account = await this.findOne(query)
      .catch(err => {
        logger.error(err);
        throw err;
      });
    if (!empty(account)) { return account; }
  };

  statics.remove_by_query = async function(query) {
    await this.deleteOne(query)
      .catch(err => {
        logger.error(err);
        throw err;
      });
  };

  return mongoose.model('Account', AccountSchema);
};


'use strict';

const MessageFormatter = require('../lib/message_formatter');

module.exports = app => {
  const { mongoose } = app;
  const Schema = mongoose.Schema;
  const logger = app.logger;

  const ActionSchema = new Schema({
    _id: String,
    action: String,
    file_path: String,
    previous_path: String,
    content: String,
    version: Number,
    encoding: { type: String, default: 'text' },
  });

  const MessageSchema = new Schema({
    branch: { type: String, default: 'master' },
    visibility: { type: String, default: 'public' },
    project_id: String,
    actions: [ ActionSchema ],
    commit_message: String,
    author_name: String,
    source_version: Number,
  }, { timestamps: true });

  const statics = MessageSchema.statics;

  statics.create_file = function(files, project_id, options) {
    const message = MessageFormatter.create_file(files, project_id, options);
    return this.create(message)
      .catch(err => {
        logger.error(`failed to create message ${message}`);
        throw err;
      });
  };

  statics.update_file = function(files, project_id, options) {
    const message = MessageFormatter.update_file(files, project_id, options);
    return this.create(message)
      .catch(err => {
        logger.error(`failed to create message ${message}`);
        throw err;
      });
  };

  statics.delete_file = function(files, project_id, options) {
    const message = MessageFormatter.delete_file(files, project_id, options);
    return this.create(message)
      .catch(err => {
        logger.error(`failed to create message ${message}`);
        throw err;
      });
  };

  statics.move_file = function(files, project_id, options) {
    const message = MessageFormatter.move_file(files, project_id, options);
    return this.create(message)
      .catch(err => {
        logger.error(`failed to create message ${message}`);
        throw err;
      });
  };

  return mongoose.model('Message', MessageSchema);
};


'use strict';

const assert = require('assert');
const Helper = require('../lib/helper');

const PENDING_TIP = 'pending';
const FOLDER_TYPE = 'tree';

const deserialize_tree = serilized_tree => {
  return JSON.parse(serilized_tree);
};

module.exports = app => {
  const redis = app.redis;
  const mongoose = app.mongoose;
  const Schema = mongoose.Schema;
  const logger = app.logger;
  const cache_expire = app.config.cache_expire;

  const CommitSchema = new Schema({
    commit_id: String,
    short_id: String,
    version: Number,
    author_name: String,
    source_version: Number,
    message: String,
  }, { timestamps: true });

  const LastCommitSchema = new Schema({
    version: Number,
    source_version: Number,
    message: String,
  }, { timestamps: true });

  const NodeSchema = new Schema({
    name: String,
    path: String,
    content: String,
    type: { type: String, default: 'blob' },
    project_id: Number,
    account_id: Number,
    commits: [ CommitSchema ],
    latest_commit: LastCommitSchema,
  }, { timestamps: true });

  NodeSchema.index({ project_id: 1, path: 1 });
  const CommitModel = mongoose.model('Commit', CommitSchema);

  const methods = NodeSchema.methods;

  methods.createCommit = function(info) {
    if (this.type === FOLDER_TYPE) return;
    const lastCommit = this.latest_commit;
    if (!lastCommit) return;
    let baseInfo = {
      version: (lastCommit.version || 0) + 1,
      commit_id: PENDING_TIP,
      short_id: PENDING_TIP,
    };
    baseInfo = Object.assign(baseInfo, info);
    const commit = new CommitModel(baseInfo);
    this.latest_commit = commit;
    this.commits.push(commit);
    return this;
  };

  const statics = NodeSchema.statics;

  NodeSchema.virtual('tree_path').get(function() {
    const path = this.previous_path || this.path;
    const name = this.previous_name || this.name;
    return statics.get_tree_path(path, name);
  });

  statics.get_file_name = function(path) {
    const file_name_pattern = /[^\/]+$/;
    const file_name = path.match(file_name_pattern)[0];
    return file_name;
  };

  statics.get_tree_path = function(path, file_name) {
    if (!file_name) { file_name = this.get_file_name(path); }
    const file_name_pattern = new RegExp(`/${file_name}$`, 'u');
    const tree_path = path.replace(file_name_pattern, '');
    return tree_path;
  };

  statics.cache = function(file, pipeline = redis.pipeline()) {
    assert(file.project_id);
    assert(file.path);
    this.cache_content(file, pipeline);
    return pipeline;
  };

  statics.release_cache = function(file, pipeline = redis.pipeline()) {
    assert(file.project_id);
    assert(file.path);
    this.release_content_cache(file, pipeline);
    this.release_tree_cache(file, pipeline);
    return pipeline;
  };

  statics.cache_content = function(file, pipeline = redis.pipeline()) {
    const key = Helper.generate_file_key(file.project_id, file.path);
    pipeline.setex(key, cache_expire, Helper.serilize_file(file));
  };

  statics.release_content_cache = function(file, pipeline = redis.pipeline()) {
    const path = file.previous_path || file.path;
    const key = Helper.generate_file_key(file.project_id, path);
    pipeline.del(key);
  };

  statics.load_content_cache_by_path = async function(project_id, path) {
    const key = Helper.generate_file_key(project_id, path);
    const project = await redis.get(key)
      .catch(err => {
        logger.error(err);
      });
    return JSON.parse(project);
  };

  statics.cache_tree = function(project_id, path, tree, pipeline = redis.pipeline()) {
    const key = Helper.generate_tree_key(project_id, path);
    pipeline.setex(key, cache_expire, Helper.serilize_tree(tree));
    return pipeline;
  };

  statics.load_tree_cache_by_path = async function(project_id, path) {
    const key = Helper.generate_tree_key(project_id, path);
    const serilized_tree = await redis.get(key)
      .catch(err => {
        logger.error(err);
      });
    return deserialize_tree(serilized_tree);
  };

  statics.release_tree_cache = function(file, pipeline = redis.pipeline()) {
    const key = Helper.generate_tree_key(file.project_id, file.tree_path);
    pipeline.del(key);
    return pipeline;
  };

  statics.release_multi_files_cache = function(files, project_id, pipeline = redis.pipeline()) {
    const keys_to_release = [];
    for (const file of files) {
      file.project_id = file.project_id || project_id;
      const file_key = Helper.generate_file_key(
        file.project_id || project_id,
        file.previous_path || file.path
      );
      keys_to_release.push(file_key);

      if (file.type === FOLDER_TYPE) {
        const tree_key = Helper.generate_tree_key(
          file.project_id || project_id,
          file.previous_path || file.path
        );
        keys_to_release.push(tree_key);
      }
    }
    pipeline.del(keys_to_release);
    return pipeline;
  };

  statics.get_by_path_from_db = async function(project_id, path) {
    const file = await this.findOne({ project_id, path });
    if (file) {
      const pipeline = this.cache(file);
      await pipeline.exec()
        .catch(err => {
          logger.error(err);
          throw err;
        });
      return file;
    }
  };

  statics.get_by_path = async function(project_id, path, from_cache = true) {
    let file;
    if (from_cache) {
      file = await this.load_content_cache_by_path(project_id, path);
      if (!Helper.empty(file)) { return file; }
    }
    file = await this.get_by_path_from_db(project_id, path);
    return file;
  };

  statics.getCommits = async function(project_id, path, skip = 0, limit = 20) {
    const node = await this.findOne({ project_id, path });
    node.commits = node.commits.reverse().slice(skip, skip + limit);
    return node;
  };

  statics.move = async function(file) {
    const pipeline = this.release_cache(file);
    await pipeline.exec()
      .catch(err => {
        logger.error(err);
        throw err;
      });
    await file.save()
      .catch(err => {
        logger.error(err);
        throw err;
      });
  };

  statics.delete_and_release_cache = async function(file) {
    const pipeline = this.release_cache(file);
    await pipeline.exec()
      .catch(err => {
        logger.error(err);
        throw err;
      });

    const path = file.path;
    await this.deleteOne({ path })
      .catch(err => {
        logger.error(`failed to hard delete file ${path}`);
        throw err;
      });
  };

  statics.get_tree_by_path_from_db = async function(
    project_id, path, recursive = false, pagination) {
    let query_condition;
    if (path) {
      const path_pattern = recursive ? `^${path}\/` : `^${path}\/[^\/]+$`;
      query_condition = { project_id, path: new RegExp(path_pattern, 'u') };
    } else {
      query_condition = { project_id };
    }

    const selected_fields = '_id name path type';
    const tree = await this.find(query_condition, selected_fields)
      .skip(pagination.skip)
      .limit(pagination.limit)
      .catch(err => { logger.error(err); });
    if (tree.length > 0 && !recursive) {
      const pipeline = this.cache_tree(project_id, path, tree);
      await pipeline.exec()
        .catch(err => {
          logger.error(`failed cache tree ${path}`);
          throw err;
        });
    }
    return tree;
  };

  statics.get_tree_by_path = async function(
    project_id, path, from_cache = true, recursive = false, pagination) {
    let tree;
    if (!recursive) {
      pagination = { skip: 0, limit: 9999999 };
      if (from_cache) {
        tree = await this.load_tree_cache_by_path(project_id, path);
      }
    }
    if (Helper.empty(tree)) {
      tree = await this.get_tree_by_path_from_db(project_id, path, recursive, pagination);
    }
    return tree;
  };

  statics.get_ancestors_of_node = async function(
    account_id, project_id, ancestors_to_create = {},
    ancestors_already_exist = {}, node) {
    let path = node.path;
    const ancestor_names = path.split('/');
    let node_name = ancestor_names[ancestor_names.length - 1];
    for (let i = ancestor_names.length - 2; i >= 0; i--) {
      path = this.get_tree_path(path, node_name);
      node_name = ancestor_names[i];
      if (ancestors_to_create[path] || ancestors_already_exist[path]) { continue; }
      const parent = await this.get_by_path_from_db(project_id, path);
      if (Helper.empty(parent)) {
        ancestors_to_create[path] = {
          name: node_name,
          type: FOLDER_TYPE,
          path,
          project_id,
          account_id,
        };
      } else {
        ancestors_already_exist[path] = true;
      }
    }
  };

  statics.get_parents_not_exist = async function(account_id, project_id, nodes) {
    const ancestors_to_create = {};
    const ancestors_already_exist = {};
    if (!(nodes instanceof Array)) { nodes = [{ path: nodes }]; }
    for (const node of nodes) {
      await this.get_ancestors_of_node(
        account_id,
        project_id,
        ancestors_to_create,
        ancestors_already_exist,
        node
      );
    }
    return Object.values(ancestors_to_create);
  };

  statics.ensure_parent_exist = async function(account_id, project_id, path) {
    const ancestors_to_create = await this
      .get_parents_not_exist(account_id, project_id, path);
    if (ancestors_to_create.length > 0) {
      await this.create(ancestors_to_create)
        .catch(err => {
          logger.error(err);
          throw err;
        });
    }
  };

  statics.get_subfiles_by_path = async function(project_id, tree_path, pattern, get_self = true) {
    if (!pattern) { pattern = new RegExp(`^${tree_path}/.*`, 'u'); }
    const subfiles = await this.find({ project_id, path: pattern })
      .limit(999999);

    if (get_self) {
      const folder = await this.findOne({ project_id, path: tree_path });
      subfiles.push(folder);
    }
    return subfiles;
  };

  statics.delete_subfiles_and_release_cache =
  async function(project_id, tree_path, subfiles, remove_self = true) {
    const pattern = new RegExp(`^${tree_path}/.*`, 'u');
    if (!subfiles) {
      subfiles = await this.get_subfiles_by_path(project_id, tree_path, pattern, remove_self);
    }
    if (Helper.empty(subfiles)) { return; }

    const pipeline = this.release_multi_files_cache(subfiles, project_id);
    await pipeline.exec()
      .catch(err => {
        logger.error(err);
        throw err;
      });

    await this.deleteMany({ project_id, path: pattern })
      .catch(err => {
        logger.error(err);
        throw err;
      });

    if (remove_self) {
      const folder = subfiles[subfiles.length - 1];
      if (!Helper.empty(folder)) {
        await folder.remove()
          .catch(err => {
            logger.error(err);
            throw err;
          });
      }
    }
  };

  statics.delete_and_release_by_query = async function(query) {
    const files = await this.find(query).limit(99999999);
    if (Helper.empty(files)) { return; }
    const pipeline = await this.release_multi_files_cache(files);
    await pipeline.exec();
    await this.deleteMany(query);
  };

  statics.delete_project = async function(project_id) {
    assert(project_id);
    await this.delete_and_release_by_query({ project_id })
      .catch(err => {
        logger.error(err);
        throw err;
      });
  };

  statics.delete_account = async function(account_id) {
    assert(account_id);
    await this.delete_and_release_by_query({ account_id })
      .catch(err => {
        logger.error(err);
        throw err;
      });
  };

  NodeSchema.post('save', async function(file) {
    const pipeline = statics.release_cache(file);
    await pipeline.exec()
      .catch(err => {
        logger.error(err);
        throw err;
      });
  });

  return mongoose.model('Node', NodeSchema);
};


'use strict';

const assert = require('assert');
const fast_JSON = require('fast-json-stringify');
const { empty, generate_project_key, generate_tree_key } = require('../lib/helper');

module.exports = app => {
  const redis = app.redis;
  const mongoose = app.mongoose;
  const Schema = mongoose.Schema;
  const logger = app.logger;
  const cache_expire = app.config.cache_expire;

  const ProjectSchema = new Schema({
    _id: Number,
    visibility: { type: String, default: 'public' },
    name: String,
    site_id: Number,
    sitename: String,
    path: { type: String, unique: true },
    git_path: String,
    account_id: Number,
  }, { timestamps: true });

  const stringify = fast_JSON({
    title: 'stringify project',
    type: 'object',
    properties: {
      _id: { type: 'number' },
      visibility: { type: 'string' },
      name: { type: 'string' },
      site_id: { type: 'number' },
      sitename: { type: 'string' },
      path: { type: 'string' },
      git_path: { type: 'string' },
      account_id: { type: 'number' },
    },
  });

  const statics = ProjectSchema.statics;

  statics.cache = async function(project) {
    const key = generate_project_key(project.path);
    const serilized_project = stringify(project);
    await redis.setex(key, cache_expire, serilized_project)
      .catch(err => {
        logger.error(`fail to cache project ${key}`);
        logger.error(err);
      });
  };

  statics.release_cache = async function(path, pipeline = redis.pipeline()) {
    this.release_content_cache(path, pipeline);
    this.release_tree_cache(path, pipeline);
    await pipeline.exec()
      .catch(err => {
        logger.error(`fail to release cache of project ${path}`);
        logger.error(err);
      });
  };

  statics.release_content_cache = async function(path, pipeline = redis.pipeline()) {
    const key = generate_project_key(path);
    pipeline.del(key);
  };

  statics.release_tree_cache = function(path, pipeline = redis.pipeline()) {
    const key = generate_tree_key(path);
    pipeline.del(key);
  };

  statics.load_cache_by_path = async function(path) {
    const key = generate_project_key(path);
    const project = await redis.get(key)
      .catch(err => {
        logger.error(err);
      });
    return JSON.parse(project);
  };

  statics.get_by_path = async function(path, from_cache = true) {
    let project;

    // load from cache
    if (from_cache) {
      project = await this.load_cache_by_path(path);
      if (!empty(project)) { return project; }
    }
    // load from db
    project = await this.get_by_path_from_db(path);
    return project;
  };

  statics.get_by_path_from_db = async function(path) {
    const project = await this.findOne({ path })
      .catch(err => { logger.error(err); });
    if (!empty(project)) {
      await this.cache(project);
      return project;
    }
  };

  statics.delete_and_release_cache = async function(path) {
    await this.release_cache(path);
    await this.deleteOne({ path })
      .catch(err => {
        throw err;
      });
  };

  statics.release_multi_projects_cache = async function(projects, pipeline = redis.pipeline()) {
    const keys_to_release = [];
    for (const project of projects) {
      keys_to_release.push(generate_project_key(project.path));
      keys_to_release.push(generate_tree_key(project.path));
    }
    pipeline.del(keys_to_release);
    return pipeline;
  };

  statics.delete_and_release_by_query = async function(query) {
    const projects = await this.find(query).limit(99999999);
    if (empty(projects)) { return; }
    const pipeline = await this.release_multi_projects_cache(projects);
    await pipeline.exec();
    await this.deleteMany(query);
  };

  statics.delete_account = async function(account_id) {
    assert(account_id);
    await this.delete_and_release_by_query({ account_id })
      .catch(err => {
        logger.error(err);
        throw err;
      });
  };

  ProjectSchema.post('save', async function(project) {
    await statics.release_cache(project.path);
  });

  return mongoose.model('Project', ProjectSchema);
};


'use strict';

const Service = require('egg').Service;
const Axios = require('axios');
const assert = require('assert');
const _ = require('lodash/object');

let Client;
let Raw_Client;

const COMMIT_PROPERTIES_TO_PICK = [
  'id', 'short_id', 'author_name', 'authored_date',
  'created_at', 'message',
];
const SOURCE_VERSION_FLAG = '|FROM';

const serializeCommits = commits => {
  let version = commits.length;
  return commits.map(commit => {
    const serilized = _.pick(commit, COMMIT_PROPERTIES_TO_PICK);
    serilized.version = version;
    serilized.commit_id = serilized.id;
    serilized.createdAt = serilized.created_at;
    serilized.updateAt = serilized.createdAt;
    serilized.source_version = serilized.message.split(SOURCE_VERSION_FLAG)[1];
    version--;
    return serilized;
  });
};

class GitlabService extends Service {
  get client() {
    if (!Client) {
      const GITLAB_CONFIG = this.config.gitlab;
      Client = Axios.create({
        baseURL: GITLAB_CONFIG.url,
        headers: { 'private-token': GITLAB_CONFIG.admin_token },
        timeout: 30 * 1000,
      });
    }
    return Client;
  }

  get raw_client() {
    if (!Raw_Client) {
      const GITLAB_CONFIG = this.config.gitlab;
      Raw_Client = Axios.create({
        baseURL: GITLAB_CONFIG.raw_url,
        headers: { 'private-token': GITLAB_CONFIG.admin_token },
        timeout: 30 * 1000,
      });
    }
    return Raw_Client;
  }

  // account
  serialize_new_account(user) {
    return {
      username: user.username,
      name: user.name,
      email: user.email,
      password: user.password,
      skip_confirmation: true,
    };
  }

  serialize_loaded_account(res_data) {
    return {
      username: res_data.username,
      name: res_data.name,
      _id: res_data.id,
    };
  }

  async get_account(username) {
    const res = await this.client
      .get(`/users?username=${username}`)
      .catch(err => {
        this.app.logger.error(`failed to get git account ${username}`);
        this.app.logger.error(err);
        throw err;
      });
    if (res.data.length > 0) { return res.data[0]; }
  }

  async create_account(user) {
    assert(user.username);
    assert(user.password);
    let registered_account;
    const account = this.serialize_new_account(user);
    await this.client
      .post('/users', account)
      .then(res => {
        registered_account = res.data;
      })
      .catch(async err => {
        if (err.response.status === 409) {
          registered_account = await this.get_account(user.username);
          return;
        }
        this.app.logger.error(`failed to create git account for ${user.username}`);
        this.app.logger.error(err);
        throw err;
      });
    return this.serialize_loaded_account(registered_account);
  }

  async delete_account(account_id) {
    assert(account_id);
    await this.client
      .delete(`/users/${account_id}?hard_delete=true`, { hard_delete: true })
      .catch(err => {
        this.app.logger.error(`failed to delete git account ${account_id}`);
        this.app.logger.error(err);
        throw err;
      });
  }

  async get_token(account_id) {
    let token = await this.get_active_token(account_id);
    if (!token) { token = await this.create_token(account_id); }
    return token;
  }

  async get_active_token(account_id) {
    assert(account_id);
    const res = await this.client
      .get(`/users/${account_id}/impersonation_tokens?state=active`)
      .catch(err => {
        this.app.logger.error(`failed to get token of git account ${account_id}`);
        this.app.logger.error(err);
        throw err;
      });
    for (const item of res.data) {
      if (item.name === 'keepwork') { return item.token; }
    }
  }

  async create_token(account_id) {
    assert(account_id);
    const res = await this.client
      .post(`/users/${account_id}/impersonation_tokens`, {
        name: 'keepwork',
        expires_at: '2222-12-12',
        scopes: [ 'api', 'read_user' ],
      }).catch(err => {
        this.app.logger.error(`failed to create token of git account ${account_id}`);
        this.app.logger.error(err);
        throw err;
      });
    return res.data.token;
  }

  // project
  serialize_new_project(project) {
    return {
      name: project.name,
      user_id: project.account_id,
      visibility: project.visibility || 'public',
      request_access_enabled: true,
    };
  }

  serialize_loaded_project(res_data) {
    return {
      _id: res_data.id,
      visibility: res_data.visibility,
      name: res_data.name,
      git_path: res_data.path_with_namespace,
      account_id: res_data.owner.id,
    };
  }

  serialize_hook_setting(project) {
    return {
      url: project.hook_url,
      push_events: project.push_events || true,
      enable_ssl_verification: project.enable_ssl_verification || false,
    };
  }

  async set_project_hooks(project_id, hook_setting) {
    assert(hook_setting.url);
    hook_setting._id = project_id;
    await this.client
      .post(`/projects/${project_id}/hooks`, hook_setting)
      .catch(err => {
        this.app.logger.error(`failed to set hook of project ${project_id}`);
        this.app.logger.error(err);
        throw err;
      });
  }

  async set_admin(project_id) {
    const options = {
      user_id: 1,
      access_level: 40,
    };
    await this.client.post(`/projects/${project_id}/members`, options)
      .catch(err => {
        this.app.logger.error(err);
        throw err;
      });
  }

  async create_project(project) {
    assert(project.name);
    assert(project.account_id);

    let serialized_project = this.serialize_new_project(project);
    const res = await this.client
      .post(`/projects/user/${serialized_project.user_id}`, serialized_project)
      .catch(err => {
        this.app.logger.error(`failed to create git project ${serialized_project.name}`);
        this.app.logger.error(err);
        throw err;
      });
    serialized_project = this.serialize_loaded_project(res.data);
    await this.set_admin(serialized_project._id);
    return serialized_project;
  }

  async update_project_visibility(project_id, visibility) {
    assert(project_id);
    assert(visibility);
    const res = await this.client
      .put(`projects/${project_id}`, { visibility })
      .catch(err => {
        this.app.logger.error(`failed to update visibility of project ${project_id}`);
        this.app.logger.error(err);
        throw err;
      });
    return this.serialize_loaded_project(res.data);
  }

  async delete_project(project_id) {
    assert(project_id);
    await this.client
      .delete(`/projects/${project_id}`)
      .catch(err => {
        this.app.logger.error(`failed to delete project ${project_id}`);
        this.app.logger.error(err);
        throw err;
      });
  }

  // file
  serialized_loaded_file(res_data) {
    return {
      name: res_data.file_name,
      content: Buffer.from(res_data.content, res_data.encoding).toString(),
      blob_id: res_data.blob_id,
      commit_id: res_data.commit_id,
      last_commit_id: res_data.last_commit_id,
    };
  }

  async load_file(project_id, file_path, ref = 'master') {
    assert(project_id);
    assert(file_path);
    file_path = encodeURIComponent(file_path);
    const res = await this.client
      .get(`/projects/${project_id}/repository/files/${file_path}?ref=${ref}`)
      .catch(err => {
        this.app.logger.error(`failed to get file ${file_path} of project ${project_id}`);
        this.app.logger.error(err);
        throw err;
      });
    return this.serialized_loaded_file(res.data);
  }

  async load_raw_file(git_path, file_path) {
    assert(git_path);
    assert(file_path);
    const res = await this.raw_client
      .get(`/${git_path}/raw/master/${file_path}`)
      .catch(err => {
        this.app.logger.error(`failed to get file ${file_path} of project ${git_path}`);
        this.app.logger.error(err);
        throw err;
      });
    if (file_path.endsWith('.json')) { res.data = JSON.stringify(res.data); }
    if (res.data.startsWith('<!DOCTYPE html>')) { throw { response: { status: 404 } }; }
    return { content: res.data };
  }

  async loadCommits(project_id, path, page = 1, per_page = 100) {
    const res = await this.client
      .get(`/projects/${project_id}/repository/commits`, {
        params: { path, page, per_page },
      });
    const commits = res.data;
    return commits;
  }

  async loadAllCommits(project_id, path) {
    let page = 1;
    const per_page = 100;
    let commits = await this.loadCommits(project_id, path, page, per_page);
    const all = commits;
    while (commits.length >= 100) {
      page++;
      commits = await this.loadCommits(project_id, path, page, per_page);
      all.push(...commits);
    }
    return serializeCommits(all);
  }
}

module.exports = GitlabService;


'use strict';

const Service = require('egg').Service;
const { KafkaClient, HighLevelProducer } = require('kafka-node');
const { promisify, inspect } = require('util');

let Client;
let Producer;
let promisified_send;
let initialized = false;

class KafkaService extends Service {
  constructor(ctx) {
    super(ctx);
    this.init_client();
    this.init_producer();
  }

  async send(payloads) {
    if (!initialized) {
      await this.refresh_metadata();
      initialized = true;
    }
    if (!promisified_send) {
      promisified_send = promisify(Producer.send.bind(Producer));
    }
    if (!(payloads instanceof Array)) { payloads = [ payloads ]; }
    return promisified_send(payloads).then(result => {
      this.app.logger.info(`Successfully sent messages to ${inspect(result)}`);
      return result;
    });
  }

  init_client() {
    if (!Client) {
      Client = new KafkaClient(this.config.kafka.client);
    }

    this.client = Client;
  }

  init_producer() {
    if (!Producer) {
      const options = this.config.kafka.producer;
      Producer = new HighLevelProducer(Client, options);
      this.on_error();
      this.on_ready();
    }
    this.producer = Producer;
  }

  async refresh_metadata() {
    const topics = Object.values(this.config.kafka.topics);
    await promisify(Client.refreshMetadata.bind(Client))(topics)
      .catch(err => {
        this.app.logger.error(err);
      });
  }

  on_ready() {
    Producer.on('ready', () => {
      this.app.logger.info('Successfully connect to kafka');
    });
  }

  on_error() {
    Producer.on('error', err => {
      this.app.logger.error('Fail to connect to kafka');
      this.app.logger.error(err);
    });
  }
}

module.exports = KafkaService;


'use strict';

const Service = require('egg').Service;
const Axios = require('axios');

let Client;

class KeepworkService extends Service {
  get client() {
    if (!Client) {
      const KEEPWORK_CONFIG = this.config.keepwork;
      Client = Axios.create({
        baseURL: KEEPWORK_CONFIG.url,
        timeout: 3 * 1000,
      });
    }
    return Client;
  }

  async ensurePermission(token, site_id, type) {
    try {
      const permission = this.config.permission[type];
      const refuse_code = this.config.permission.reject;
      const res = await this.client.get(
        `/sites/${site_id}/privilege`,
        { headers: { Authorization: token } }
      );
      if (res.data === refuse_code) { return false; }
      if (res.data >= permission) { return true; }
      return false;
    } catch (err) {
      this.app.logger.error(err);
      throw err;
    }
  }

  async getUserProfile(token) {
    return this.client.get(
      'users/profile',
      { headers: { Authorization: token } }
    );
  }
}

module.exports = KeepworkService;


'use strict';

const Service = require('egg').Service;

const FILE_TYPE = 'blob';

class NodeService extends Service {
  async getCommits(project_id, path, skip = 0, limit = 20) {
    const { ctx } = this;
    const file = await ctx.model.Node.getCommits(project_id, path, skip, limit);
    if (!file) ctx.throw(404, 'File not found');
    if (file.type !== FILE_TYPE) return { commits: [], total: 0, file };
    if (file.latest_commit) {
      return { commits: file.commits, total: file.latest_commit.version, file };
    }
    return await this.getCommitsFromGitlab(file, skip, limit);
  }

  async getCommitsFromGitlab(file, skip, limit) {
    const { service } = this;
    file.commits = await service.gitlab.loadAllCommits(file.project_id, file.path);
    const latestCommit = file.commits[0];
    file.latest_commit = latestCommit;
    file.commits.reverse();
    await file.save();
    return {
      commits: file.commits.reverse().slice(skip, skip + limit),
      total: file.latest_commit.version,
      file,
    };
  }

  async getFileWithCommits(file) {
    if (!file.latest_commit) {
      const result = await this.getCommits(file.project_id, file.path, 0, 10000);
      file = result.file;
    }
    return file;
  }
}

module.exports = NodeService;


'use strict';

class ErrorHandler {
  static handle(err, ctx) {
    ctx.logger.error(err);
    const handler = ErrorHandler[err.name] || ErrorHandler.InternalServerError;
    const errMsg = handler(err, ctx);
    ctx.body = { error: errMsg };
  }

  static UnprocessableEntityError(err, ctx) {
    ctx.status = 400;
    return ErrorHandler.BadRequestError(err, ctx);
  }

  static BadRequestError(err) {
    return err.errors || err.message;
  }

  static ForbiddenError(err) {
    return err.message || 'Forbidden';
  }

  static ConflictError(err) {
    return err.message || 'Already exists';
  }

  static UnauthorizedError(err) {
    return err.message;
  }

  static NotFoundError(err) {
    return err.message || 'Not found';
  }

  static InternalServerError(err, ctx) {
    ctx.status = 500;
    return 'An unknown error happened';
  }

  static PayloadTooLargeError() {
    return 'This request is too large';
  }
}

module.exports = {
  accepts() {
    return 'json';
  },
  json(err, ctx) {
    ErrorHandler.handle(err, ctx);
  },
};


'use strict';

// had enabled by egg
// exports.static = true;

exports.mongoose = {
  enable: true,
  package: 'egg-mongoose',
};

exports.redis = {
  enable: true,
  package: 'egg-redis',
};

exports.validate = {
  enable: true,
  package: 'egg-validate',
};


exports.cors = {
  enable: true,
  package: 'egg-cors',
};

exports.parameters = {
  enable: true,
  package: 'egg-parameters',
};

// exports.jwt = {
//   enable: true,
//   package: 'egg-jwt',
// };


'use strict';

const { app } = require('egg-mock/bootstrap');
const jwt = require('keepwork-jwt-simple');

const user = {
  id: 123,
  username: 'gitgateway123',
  password: '12345678',
};

let token;

before(() => {
  const admin = {
    username: 'unittest',
    userId: 15,
    roleId: 10,
  };

  const secret = app.config.jwt.secret;
  token = jwt.encode(admin, secret, 'HS1');
});

describe('test/app/controller/account.test.js', () => {
  it('should post /accounts to create an account', () => {
    return app.httpRequest()
      .post('/accounts')
      .send(user)
      .set('Authorization', `Bearer ${token}`)
      .expect(201);
  });

  it('should delete /accounts/:id to delete an account', () => {
    return app.httpRequest()
      .del('/accounts/gitgateway123')
      .set('Authorization', `Bearer ${token}`)
      .expect(200);
  });
});


'use strict';

const { app } = require('egg-mock/bootstrap');
const jwt = require('keepwork-jwt-simple');

let token;

before(async () => {
  const admin = {
    username: 'unittest',
    userId: 15,
    roleId: 10,
  };
  const secret = app.config.jwt.secret;
  token = jwt.encode(admin, secret, 'HS1');

  const user = {
    id: 123,
    username: 'test_file',
    password: '12345678',
  };

  const project = {
    sitename: 'test_file',
    site_id: 123,
    visibility: 'public',
  };

  await app.httpRequest()
    .post('/accounts')
    .send(user)
    .set('Authorization', `Bearer ${token}`);

  await app.httpRequest()
    .post('/projects/user/test_file')
    .set('Authorization', `Bearer ${token}`)
    .send(project);
});

after(async () => {
  await app.httpRequest()
    .del(`/projects/${encodeURIComponent('test_file/test_file')}`)
    .set('Authorization', `Bearer ${token}`);

  await app.httpRequest()
    .del('/accounts/test_file')
    .set('Authorization', `Bearer ${token}`);
});

describe('test/app/controller/file.test.js', () => {
  const project_path = encodeURIComponent('test_file/test_file');
  const path = encodeURIComponent('test_file/test_file/test.md');
  it('should post /projects/:project_path/files/:path to create a file', () => {
    const file = { content: '123' };
    return app.httpRequest()
      .post(`/projects/${project_path}/files/${path}`)
      .send(file)
      .set('Authorization', `Bearer ${token}`)
      .expect(201);
  });

  it('should get /projects/:project_path/files/:path to get a file', () => {
    return app.httpRequest()
      .get(`/projects/${project_path}/files/${path}`)
      .set('Authorization', `Bearer ${token}`)
      .expect(200)
      .expect({ content: '123' });
  });

  it('should put /projects/:project_path/files/:path to update a file', () => {
    return app.httpRequest()
      .put(`/projects/${project_path}/files/${path}`)
      .send({ content: '456' })
      .set('Authorization', `Bearer ${token}`)
      .expect(200);
  });

  const new_path = 'test_file/test_file/test_new.md';
  it('should put /projects/:project_path/files/:path/move to move a file', () => {
    return app.httpRequest()
      .put(`/projects/${project_path}/files/${path}/move`)
      .send({ new_path })
      .set('Authorization', `Bearer ${token}`)
      .expect(200);
  });

  it('should delete /projects/:project_path/files/:path to remove a file', () => {
    return app.httpRequest()
      .del(`/projects/${project_path}/files/${encodeURIComponent(new_path)}`)
      .set('Authorization', `Bearer ${token}`)
      .expect(200);
  });
});


'use strict';

const { app } = require('egg-mock/bootstrap');
const jwt = require('keepwork-jwt-simple');

let token;
const project_path = encodeURIComponent('test_folder/test_folder');

before(async () => {
  const admin = {
    username: 'unittest',
    userId: 15,
    roleId: 10,
  };
  const secret = app.config.jwt.secret;
  token = jwt.encode(admin, secret, 'HS1');

  const user = {
    id: 123,
    username: 'test_folder',
    password: '12345678',
  };

  const project = {
    sitename: 'test_folder',
    site_id: 123,
    visibility: 'public',
  };

  await app.httpRequest()
    .post('/accounts')
    .send(user)
    .set('Authorization', `Bearer ${token}`);

  await app.httpRequest()
    .post('/projects/user/test_folder')
    .set('Authorization', `Bearer ${token}`)
    .send(project);
});

after(async () => {
  await app.httpRequest()
    .del(`/projects/${encodeURIComponent('test_folder/test_folder')}`)
    .set('Authorization', `Bearer ${token}`);

  await app.httpRequest()
    .del('/accounts/test_folder')
    .set('Authorization', `Bearer ${token}`);
});

const path = encodeURIComponent('test_folder/test_folder/new_folder');
describe('test/app/controller/folder.test.js', () => {
  it('should post /projects/:project_path/folders/:path to create a folder', () => {
    return app.httpRequest()
      .post(`/projects/${project_path}/folders/${path}`)
      .set('Authorization', `Bearer ${token}`)
      .expect(201);
  });

  it('should delete /projects/:project_path/folders/:path to remove a folder', () => {
    return app.httpRequest()
      .del(`/projects/${project_path}/folders/${path}`)
      .set('Authorization', `Bearer ${token}`)
      .expect(200);
  });
});


'use strict';

const { app, assert } = require('egg-mock/bootstrap');

describe('test/app/controller/home.test.js', () => {

  it('should assert', async () => {
    const pkg = require('../../../package.json');
    assert(app.config.keys.startsWith(pkg.name));

    // const ctx = app.mockContext({});
    // await ctx.service.xx();
  });

  it('should GET /', () => {
    return app.httpRequest()
      .get('/')
      .expect('Hello, git-gateway')
      .expect(200);
  });
});


'use strict';

const { app, assert } = require('egg-mock/bootstrap');
const jwt = require('keepwork-jwt-simple');

const project = {
  sitename: 'test',
  site_id: 456,
  visibility: 'public',
};

let token;

before(async () => {
  const admin = {
    username: 'unittest',
    userId: 15,
    roleId: 10,
  };

  const secret = app.config.jwt.secret;
  token = jwt.encode(admin, secret, 'HS1');

  const user = {
    id: 123,
    username: 'unittest',
    password: '12345678',
  };

  await app.httpRequest()
    .post('/accounts')
    .set('Authorization', `Bearer ${token}`)
    .send(user);
});

after(async () => {
  await app.httpRequest()
    .del('/accounts/unittest')
    .set('Authorization', `Bearer ${token}`);
});

describe('test/app/controller/project.test.js', () => {
  it('should post /projects/user/:kw_username to create a project', () => {
    return app.httpRequest()
      .post('/projects/user/unittest')
      .set('Authorization', `Bearer ${token}`)
      .send(project)
      .expect(201);
  });

  it('should put /projects/:path/visibility to update the visibility of a project', () => {
    const path = encodeURIComponent('unittest/test');
    return app.httpRequest()
      .put(`/projects/${path}/visibility`)
      .send({ visibility: 'private' })
      .set('Authorization', `Bearer ${token}`)
      .expect(200)
      .expect(res => {
        assert(res.body.visibility === 'private');
      });
  });

  it('should delete /projects/:path to delete an project', () => {
    const path = encodeURIComponent('unittest/test');
    return app.httpRequest()
      .del(`/projects/${path}`)
      .set('Authorization', `Bearer ${token}`)
      .expect(200);
  });
});


'use strict';

const { app, assert } = require('egg-mock/bootstrap');
const jwt = require('keepwork-jwt-simple');

let token;
const project_path = encodeURIComponent('test_tree/test_tree');

before(async () => {
  const admin = {
    username: 'unittest',
    userId: 15,
    roleId: 10,
  };
  const secret = app.config.jwt.secret;
  token = jwt.encode(admin, secret, 'HS1');

  const user = {
    id: 789,
    username: 'test_tree',
    password: '12345678',
  };

  const project = {
    sitename: 'test_tree',
    site_id: 123,
    visibility: 'public',
  };

  await app.httpRequest()
    .post('/accounts')
    .send(user)
    .set('Authorization', `Bearer ${token}`);

  await app.httpRequest()
    .post('/projects/user/test_tree')
    .set('Authorization', `Bearer ${token}`)
    .send(project);

  const file = { content: 'hello' };
  const file_path = 'test_tree/test_tree/test.md';
  await app.httpRequest()
    .post(`/projects/${project_path}/files/${encodeURIComponent(file_path)}`, file)
    .set('Authorization', `Bearer ${token}`)
    .send(project);

  const folder_path = 'test_tree/test_tree/new_folder';
  await app.httpRequest()
    .post(`/projects/${project_path}/folders/${encodeURIComponent(folder_path)}`)
    .set('Authorization', `Bearer ${token}`)
    .send(project);
});

describe('test/app/controller/tree.test.js', () => {
  it('should get a tree', () => {
    const tree_path = encodeURIComponent('test_tree/test_tree');
    return app.httpRequest()
      .get(`/projects/${project_path}/tree/${tree_path}`)
      .expect(200)
      .expect(response => {
        const tree = response.body;
        assert(tree instanceof Array);
        assert(tree.length === 2);
      });
  });
});

after(async () => {
  await app.httpRequest()
    .del(`/projects/${encodeURIComponent('test_tree/test_tree')}`)
    .set('Authorization', `Bearer ${token}`);

  await app.httpRequest()
    .del('/accounts/test_tree')
    .set('Authorization', `Bearer ${token}`);
});


'use strict';

const { app, assert } = require('egg-mock/bootstrap');

describe('test/app/extend/context.test.js', () => {
  describe('ensurePermission', () => {
    it('should throw 401', async () => {
      const ctx = app.mockContext();
      try {
        await ctx.ensurePermission(1, 2);
      } catch (err) {
        assert(err.name === 'UnauthorizedError');
      }
    });

    it('should not throw 401', async () => {
      const ctx = app.mockContext();
      ctx.state = { user: { userId: 15, username: 'test' } };
      await ctx.ensurePermission(1, 'rw');
    });
  });
});


'use strict';

const { assert } = require('egg-mock/bootstrap');
const { empty } = require('../../../app/lib/helper');

describe('test/app/lib/helper.test.js', () => {
  it('should return true', () => {
    assert(empty());
  });

  it('should return true', () => {
    assert(empty({}));
  });

  it('should return false', () => {
    assert(!empty({ test: true }));
  });
});


'use strict';

const { app, assert } = require('egg-mock/bootstrap');

const account = {
  _id: 123,
  kw_id: 132,
  name: 'test123',
  kw_username: 'test123',
};

let AccountModel;

before(() => {
  const ctx = app.mockContext();
  AccountModel = ctx.model.Account;
});

describe('test/app/model/account.test.js', () => {
  it('should get account model', async () => {
    assert(AccountModel);
  });

  it('should get an account', async () => {
    const loaded_account = await AccountModel.get_by_query({ _id: account._id });
    assert(loaded_account.kw_usename === account.kw_usename);
    assert(loaded_account.name === account.name);
    assert(loaded_account.kw_id === account.kw_id);
    assert(loaded_account._id === account._id);
  });

  it('should release the cache after deleted', async () => {
    await AccountModel.delete_and_release_cache_by_kw_username(account.kw_username);
    const cached_data = await AccountModel.load_cache_by_kw_username(account.kw_username);
    assert(!cached_data);
  });
});


'use strict';

const { app, assert } = require('egg-mock/bootstrap');

const file = {
  name: 'test.md',
  path: 'test_account/test_project/test.md',
  content: 'just a test',
  type: 'blob',
  project_id: 789,
  account_id: 789,
};

let NodeModel;

before(() => {
  const ctx = app.mockContext();
  NodeModel = ctx.model.Node;
});

describe('test/app/model/node.test.js', () => {
  it('should get file model', async () => {
    assert(NodeModel);
  });

  it('should cache after created', async () => {
    await NodeModel.create(file);
  });

  it('should get an file from database', async () => {
    const loaded_from_db = await NodeModel.get_by_path_from_db(file.project_id, file.path);
    assert(loaded_from_db.name = file.name);
    assert(loaded_from_db.path = file.path);
    assert(loaded_from_db.content = file.content);
    assert(loaded_from_db.type = file.type);
    assert(loaded_from_db.project_id = file.project_id);
    assert(loaded_from_db.account_id = file.account_id);
  });

  it('should get an file from cache', async () => {
    const loaded_from_cache = await NodeModel.load_content_cache_by_path(file.project_id, file.path);
    assert(loaded_from_cache.type = file.type);
    assert(loaded_from_cache.path = file.path);
    assert(loaded_from_cache.content = file.content);
  });

  it('should release the cache after deleted', async () => {
    await NodeModel.delete_and_release_cache(file);
    const cached_data = await NodeModel.load_content_cache_by_path(file.project_id, file.path);
    assert(!cached_data);
  });
});


'use strict';

const { app, assert } = require('egg-mock/bootstrap');

const project = {
  _id: 12345,
  site_id: 456,
  sitename: 'test1',
  visibility: 'private',
  name: 'keepworktest1',
  path: 'testuser/test1',
  git_path: 'gitlab_www_testuser/keepworktest1',
  account_id: 123,
};

let ProjectModel;

before(() => {
  const ctx = app.mockContext();
  ProjectModel = ctx.model.Project;
});

describe('test/app/model/project.test.js', () => {
  it('should get project model', async () => {
    assert(ProjectModel);
  });

  it('should create the project', async () => {
    await ProjectModel.create(project);
  });

  it('should get project from db', async () => {
    const loaded_project = await ProjectModel.get_by_path_from_db(project.path);
    assert(loaded_project._id === project._id);
    assert(loaded_project.visibility === project.visibility);
    assert(loaded_project.name === project.name);
    assert(loaded_project.site_id === project.site_id);
    assert(loaded_project.sitename === project.sitename);
    assert(loaded_project.path === project.path);
    assert(loaded_project.git_path === project.git_path);
    assert(loaded_project.account_id === project.account_id);
  });

  it('should get the cache', async () => {
    const cached_data = await ProjectModel.load_cache_by_path(project.path);
    assert(cached_data._id === project._id);
    assert(cached_data.visibility === project.visibility);
    assert(cached_data.name === project.name);
    assert(cached_data.site_id === project.site_id);
    assert(cached_data.sitename === project.sitename);
    assert(cached_data.path === project.path);
    assert(cached_data.git_path === project.git_path);
    assert(cached_data.account_id === project.account_id);
  });

  it('should release cache after updated', async () => {
    const loaded_project = await ProjectModel.get_by_path_from_db(project.path);
    loaded_project.visibility = 'public';
    await loaded_project.save();
    const cached_data = await ProjectModel.load_cache_by_path(project.path);
    assert(!cached_data);
  });

  it('should release the cache after deleted', async () => {
    await ProjectModel.delete_and_release_cache(project.path);
    const cached_data = await ProjectModel.load_cache_by_path(project.path);
    assert(!cached_data);
  });
});


'use strict';

const { app, assert } = require('egg-mock/bootstrap');

let result;
let GitlabService;

before(() => {
  const ctx = app.mockContext();
  GitlabService = ctx.service.gitlab;
});

describe('test/app/service/gitlab.test.js', () => {
  it('should get gitlab client', () => {
    assert(GitlabService.client);
  });

  describe('about account', () => {
    it('should create a gitlab account for the given user, and then delete the account', async () => {
      const user = {
        username: 'gitlab_www_testbackend1',
        name: 'testbackend1',
        password: '12345678',
        email: 'testbackend1@paracraft.cn',
      };
      const account = await GitlabService.create_account(user);
      assert(account.username === user.username);
      assert(account._id);
      assert(account.name === user.name);
      await GitlabService.delete_account(account._id);
    });
  });

  describe('about project', () => {
    it('should create a project', async () => {
      const project_to_create = {
        name: 'test0001',
        account_id: 11549,
        hook_url: 'http://localhost:8099/api/wiki/models/data_source/gitlabWebhook',
        visibility: 'public',
      };
      result = await GitlabService.create_project(project_to_create);
      assert(result._id);
      assert(result.visibility === 'public');
      assert(result.name);
      assert(result.git_path);
    });

    it('should update the visibility of a project', async () => {
      result = await GitlabService.update_project_visibility(result._id, 'private');
      assert(result.visibility === 'private');
    });

    it('should delete a project', async () => {
      await GitlabService.delete_project(result._id);
    });
  });
});


// 'use strict';

// const { app, assert } = require('egg-mock/bootstrap');

// let KeepworkService;

// before(() => {
//   const ctx = app.mockContext();
//   KeepworkService = ctx.service.keepwork;
// });

// describe('test/app/service/keepwork.test.js', () => {
//   describe('ensurePermission', () => {
//     it('should return false', async () => {
//       const permitted = await KeepworkService.ensurePermission(
//         1, 2, 'r');
//       assert(!permitted);
//     });

//     it('should return false', async () => {
//       const permitted = await KeepworkService.ensurePermission(
//         1, 2, 'rw');
//       assert(!permitted);
//     });

//     it('should return true', async () => {
//       const permitted = await KeepworkService.ensurePermission(
//         6, 5, 'r');
//       assert(permitted);
//     });

//     it('should return false', async () => {
//       const permitted = await KeepworkService.ensurePermission(
//         6, 5, 'rw');
//       assert(!permitted);
//     });

//     it('should return true', async () => {
//       const permitted = await KeepworkService.ensurePermission(
//         11, 4, 'rw');
//       assert(permitted);
//     });
//   });
// });



'use strict';


module.exports = {
  sleep(time) {
    return new Promise(resolve => {
      setTimeout(resolve, time);
    });
  },

  // decorator
  attempt(worker, number = 3, delay = 3000, debug = false) {
    return async (...params) => {
      for (let i = number; i > 0; i--) {
        try {
          const result = await worker(...params);
          return result;
        } catch (err) {
          if (i <= 1) throw err;
          await this.sleep(delay);
          if (debug) console.log('retry');
        }
      }
    };
  },

  endsWithAny(str, list) {
    for (const item of list) {
      if (str.endsWith(item)) return true;
    }
    return false;
  },
};


'use strict';

const BaseMessageConsumer = require('../base_consumer');

class CommitMessageConsumer extends BaseMessageConsumer {
  get service_name() {
    return 'gitlab';
  }
}

module.exports = CommitMessageConsumer;


'use strict';

const BaseMessageConsumer = require('../base_consumer');

class ESMessageConsumer extends BaseMessageConsumer {
  get service_name() {
    return 'gitlab';
  }
}

module.exports = ESMessageConsumer;


'use strict';

const BaseMessageConsumer = require('../base_consumer');

class ESMessageConsumer extends BaseMessageConsumer {
  get service_name() {
    return 'elasticsearch';
  }

  formatMsg(message) {
    message.value = JSON.parse(message.value.toString());
  }
}

module.exports = ESMessageConsumer;


'use strict';

const Subscription = require('egg').Subscription;

const paused_status_pool = {};

class BaseMessageConsumer extends Subscription {
  // Override this method.The property service_name is
  // the name when you call the service with
  // this.ctx.service[service_name].If your consumer
  // extends this base consumer, paraHandle method
  // and continue method must be implemented in you
  // service class.
  get service_name() {
    return 'service';
  }

  get class_name() {
    return this.constructor.name;
  }

  get paused() {
    const { class_name } = this;
    return paused_status_pool[class_name];
  }

  formatMsg(message) {
    message.value = message.value.toString();
  }

  pause() {
    const { ctx, class_name } = this;
    ctx.logger.info('paused');
    ctx.consumer.pause();
    paused_status_pool[class_name] = true;
  }

  resume() {
    const { ctx, class_name } = this;
    ctx.consumer.resume();
    paused_status_pool[class_name] = false;
    ctx.logger.info('resumed');
  }

  async pauseIfBusy(highWaterLevel) {
    if (highWaterLevel && !this.paused) {
      const { service, service_name } = this;
      this.pause();
      await service[service_name].continue();
      this.resume();
    }
  }

  async subscribe(message) {
    const { service, service_name, ctx } = this;
    try {
      this.formatMsg(message);
      const highWaterLevel = service[service_name]
        .paraHandle(message);
      await this.pauseIfBusy(highWaterLevel);
    } catch (err) {
      ctx.logger.error(err);
    }
  }
}

module.exports = BaseMessageConsumer;





'use strict';

const assert = require('assert');
const emitter = require('events');
const awaitEvent = require('await-event');
const Queue = require('./queue');

const _working_pool = Symbol('working_pool');
const _free_pool = Symbol('free_pool');
const _worker = Symbol('worker');
const _cache = Symbol('_cache');
const _emitter = Symbol('_emitter');

class QueuePool {
  constructor(worker, options) {
    let { concurrency, queue_limit, cache_limit } = options;
    concurrency = concurrency || 10;
    cache_limit = cache_limit || 5;
    queue_limit = queue_limit || 5;
    this[_working_pool] = {};
    this[_free_pool] = new Queue(concurrency);
    this[_cache] = new Queue(cache_limit * 2);
    this[_worker] = this.wrap(worker);
    this[_emitter] = new emitter();
    this[_emitter].await = awaitEvent;
    for (let i = 0; i < concurrency; i++) {
      const queue = new Queue(queue_limit);
      this[_free_pool].push(queue);
    }
  }

  wrap(worker) {
    return async key => {
      const queue = this[_working_pool][key];
      for (let params = queue.shift(); params; params = queue.shift()) {
        await worker(params);
      }
      this.unbindKeyFromQueue(key, queue);
      this.consumeCache();
    };
  }



  consumeCache() {
    const cache = this[_cache];
    const total_keys = cache.length / 2;
    for (let i = 0; i < total_keys; i++) {
      const key = cache.shift();
      const params = cache.shift();
      this.push(key, params);
    }
    !this.highWaterLevel() && this[_emitter].emit('continue');
  }

  bindKeyToQueue(key, free_queue) {
    this[_working_pool][key] = free_queue;
  }

  unbindKeyFromQueue(key, queue) {
    this[_free_pool].push(queue);
    this[_working_pool][key] = undefined;
  }

  pushIntoWorkingQueue(key, params) {
    const pushed = this[_working_pool][key].push(params);
    !pushed && this.pushIntoCache(key, params);
  }

  pushIntoFreeQueue(key, params) {
    const free_queue = this[_free_pool].shift();
    free_queue.push(params);
    this.bindKeyToQueue(key, free_queue);
    this[_worker](key);
  }

  pushIntoCache(key, params) {
    this[_cache].push(key, params);
  }

  push(key, params) {
    assert(key, 'key required');
    assert(params, 'params required');
    if (this.keyBindingQueue(key)) {
      this.pushIntoWorkingQueue(key, params);
    } else if (this.hasFreeQueue()) {
      this.pushIntoFreeQueue(key, params);
    } else {
      this.pushIntoCache(key, params);
    }
    return this.highWaterLevel();
  }

  hasFreeQueue() {
    return this[_free_pool].length > 0;
  }

  keyBindingQueue(key) {
    return this[_working_pool][key];
  }

  highWaterLevel() {
    return this[_cache].full;
  }

  continue() {
    return this[_emitter].await('continue');
  }
}

module.exports = QueuePool;





'use strict';

const assert = require('assert');

const inner = Symbol('_inner');
const limit = Symbol('_limit');
const first_pos = Symbol('_first');
const last_pos = Symbol('_last');

const isNumber = num => Object(num) instanceof Number;

class Queue {
  constructor(max_length) {
    assert(isNumber(max_length), 'Max length must be a number');
    this[inner] = [];
    this[limit] = max_length;
    this.reset();
  }

  reset() {
    this[inner] = [];
    this[first_pos] = 0;
    this[last_pos] = 0;
  }

  getNextPos(current_pos) {
    return (current_pos + 1) % this[limit];
  }

  shift() {
    const current_pos = this[first_pos];
    const first_value = this[inner][current_pos];
    if (first_value === undefined) return;
    this[inner][current_pos] = undefined;
    const next = this.getNextPos(current_pos);
    this[first_pos] = next;
    return first_value;
  }

  static validate(...values) {
    for (const value of values) {
      assert(value !== undefined, 'Cannot push undefined');
    }
  }

  pushOne(value) {
    this[inner][this[last_pos]] = value;
    const next = this.getNextPos(this[last_pos]);
    this[last_pos] = next;
  }

  push(...values) {
    if (values.length > this.available) return false;
    Queue.validate(...values);
    for (const value of values) {
      this.pushOne(value);
    }
    return true;
  }

  get available() {
    return this[limit] - this.length;
  }

  get full() {
    const last_value = this[inner][this[last_pos]];
    if (last_value !== undefined) return true;
    return false;
  }

  get length() {
    if (this.full) return this[limit];
    return (this[limit] + this[last_pos] - this[first_pos]) % this[limit];
  }
}

module.exports = Queue;





'use strict';

// const _ = require('lodash/object');
// const fast_JSON = require('fast-json-stringify');

const id2Key = id => `projects:${id}:locks`;

module.exports = app => {
  const { mongoose, redis } = app;
  const Schema = mongoose.Schema;

  const ActionSchema = new Schema({
    action: String,
    file_path: String,
    previous_path: String,
    content: String,
    encoding: { type: String, default: 'text' },
    version: Number,
  });

  const MessageSchema = new Schema({
    branch: { type: String, default: 'master' },
    project_id: String,
    actions: [ ActionSchema ],
    commit_message: String,
    author_name: String,
    source_version: Number,
  }, { timestamps: true });

  const statics = MessageSchema.statics;

  statics.lock = ids => {
    if (!ids) {
      return;
    } else if (Number(ids)) {
      const key = id2Key(ids);
      return redis.incr(key);
    }
    const pipeline = redis.pipeline();
    for (const id of ids) {
      pipeline.incr(id2Key(id));
    }
    return pipeline.exec();
  };

  statics.unLock = ids => {
    let keys;
    if (!ids) {
      return;
    } else if (Number(ids)) {
      keys = id2Key(ids);
    } else {
      const keys = [];
      for (const id of ids) {
        keys.push(id2Key(id));
      }
    }
    return redis.del(keys);
  };

  statics.resetLock = id => {
    const key = id2Key(id);
    return redis.set(key, 1);
  };

  statics.isLocked = project_id => {
    const key = id2Key(project_id);
    return redis.get(key);
  };

  MessageSchema.methods.lock = function() {
    return statics.lock(this.project_id);
  };

  MessageSchema.methods.unLock = function() {
    return statics.unLock(this.project_id);
  };

  MessageSchema.methods.resetLock = function() {
    return statics.resetLock(this.project_id);
  };

  MessageSchema.virtual('isLocked').get(function() {
    return statics.isLocked(this.project_id);
  });

  return mongoose.model('Message', MessageSchema);
};





'use strict';

const _ = require('lodash/lang');

module.exports = app => {
  const mongoose = app.mongoose;
  const Schema = mongoose.Schema;

  const CommitSchema = new Schema({
    commit_id: String,
    short_id: String,
    version: Number,
    author_name: String,
    source_version: Number,
    message: String,
  }, { timestamps: true });

  const LastCommitSchema = new Schema({
    version: Number,
    source_version: Number,
    message: String,
  }, { timestamps: true });

  const NodeSchema = new Schema({
    name: String,
    path: String,
    content: String,
    type: { type: String, default: 'blob' },
    project_id: Number,
    account_id: Number,
    commits: [ CommitSchema ],
    latest_commit: LastCommitSchema,
  }, { timestamps: true });

  const methods = NodeSchema.methods;

  methods.getCommitByVersion = function(version) {
    let index;
    let commit;
    if (!_.isEmpty(this.commits)) {
      index = version;
      commit = this.commits[version] || {};
      if (commit.version !== version) {
        for (let i = 0; i < this.commits.length; i++) {
          const item = this.commits[i];
          if (item.version === version) {
            commit = item;
            index = i;
            break;
          }
        }
      }
    }
    return { commit, index };
  };

  return mongoose.model('Node', NodeSchema);
};






'use strict';

const Service = require('egg').Service;
const QueuePool = require('../lib/queue_pool');

const queue_pools = {};

class BaseParaService extends Service {
  // Override this method.The config name
  // must be the same with you service_name
  get service_name() {
    return 'service';
  }

  get highWaterLevel() {
    return this.pool.highWaterLevel();
  }

  continue() {
    return this.pool.continue();
  }

  get pool() {
    const { service_name } = this;
    if (!queue_pools[service_name]) {
      const options = this.config[service_name].queue_pool;
      queue_pools[service_name] = new QueuePool(
        this.handleMessage.bind(this),
        options
      );
    }
    return queue_pools[service_name];
  }

  // Override this method.It's the handler
  // with every message.
  async handleMessage(message) {
    try {
      await this.ctx.helper.sleep(100);
      console.log(message);
    } catch (err) {
      const { logger } = this.ctx;
      logger.error(err);
    }
  }

  paraHandle(message) {
    return this.pool.push(message.key, message);
  }
}

module.exports = BaseParaService;






'use strict';

const BaseParaService = require('./base_para_service');
const Axios = require('axios');
const assert = require('assert');

class OperationParser {
  static parse(operation, datetime, visibility) {
    const { action } = operation;
    const meta = OperationParser.getMeta(operation);
    const bulk = [ meta ];
    if (action !== 'delete') {
      const data = OperationParser[action](operation, datetime, visibility);
      bulk.push(data);
    }
    return bulk;
  }

  static getPageInfoFromPath(operation) {
    const { file_path } = operation;
    const url = file_path.slice(0, -3);
    const splited_path = file_path.split('/');
    const [ username, site ] = splited_path;
    const title = (splited_path[ splited_path.length - 1]).slice(0, -3);
    return [ url, title, site, username ];
  }

  static getMeta(operation) {
    let { action, _id } = operation;
    if (action === 'move') action = 'update';
    return { [action]: { _id } };
  }

  static create(operation, datetime, visibility) {
    const [
      url, title, site, username,
    ] = OperationParser.getPageInfoFromPath(operation);
    const { content } = operation;
    const create_at = datetime;
    const update_at = datetime;
    const id = operation._id;
    const data = {
      url, title, site, username, id, content,
      visibility, create_at, update_at,
    };
    return data;
  }

  static update(operation, datetime) {
    const { content } = operation;
    const update_at = datetime;
    const data = { doc: { content, update_at } };
    return data;
  }

  static move(operation, datetime) {
    const [ url, title ] = OperationParser.getPageInfoFromPath(operation);
    const update_at = datetime;
    const data = { doc: { url, title, update_at } };
    return data;
  }
}



module.exports = app => {
  const config = app.config.elasticsearch;
  const Client = Axios.create({
    baseURL: `${config.url}`,
    headers: { Authorization: config.token },
    timeout: 30 * 1000,
  });

  class ElasticsearchService extends BaseParaService {
    get service_name() {
      return 'elasticsearch';
    }

    get client() {
      return Client;
    }

    async handleMessage(message) {
      try {
        const handler_name = this.route(message);
        await this[handler_name](message);
      } catch (err) {
        const { logger } = this.ctx;
        logger.error(err);
      }
    }

    route(message) {
      const handler_name = message.value.method || 'syncPage';
      return handler_name;
    }

    async syncPage(message) {
      const body = await this.getBulkBody(message);
      const { index, type } = this.config.elasticsearch.meta.page;
      if (body.length > 0) await this.bulk(body, index, type);
    }

    updateSiteVisibility(message) {
      const { path, visibility } = message.value;
      assert(path);
      assert(visibility);
      return this.client.put(`/sites/${path}/visibility`, { visibility });
    }

    deleteSite(message) {
      const { path } = message.value;
      assert(path);
      return this.client.delete(`/sites/${path}`);
    }

    bulk(body, index, type) {
      return this.client.post('/bulk', { body, index, type });
    }

    isPage(operation) {
      const { file_path } = operation;
      const { helper } = this.ctx;
      const { whilt_list } = this.config.elasticsearch;
      if (!(file_path.endsWith('.md'))) return false;
      if (helper.endsWithAny(file_path, whilt_list)) return false;
      return true;
    }

    async parseMarkdown(data) {
      const { service } = this;
      const content = data.doc ? data.doc.content : data.content;
      if (!content) return data;
      const res = await service.keepwork.parseMarkdown(content);
      if (data.content) {
        data.content = res.data.content;
      } else {
        data.doc.content = res.data.content;
      }
      return data;
    }

    async operation2Bulk(operation, datetime, visibility) {
      const bulk = OperationParser.parse(operation, datetime, visibility);
      const data = bulk[1];
      if (data) bulk[1] = await this.parseMarkdown(data);
      return bulk;
    }

    async getBulkBody(message) {
      const operations = message.value.actions;
      const { visibility } = message.value;
      const datetime = message.value.createdAt;
      const body = [];
      for (const operation of operations) {
        try {
          if (!this.isPage(operation)) continue;
          const [ meta, data ] = await this
            .operation2Bulk(operation, datetime, visibility);
          body.push(meta);
          if (data) body.push(data);
        } catch (err) {
          this.ctx.logger.error(err);
        }
      }
      return body;
    }

    async upsertPackage(pkg) {
      return this.client.post(`/packages/${pkg.id}/upsert`, pkg);
    }
  }

  return ElasticsearchService;
};





'use strict';

const BaseParaService = require('./base_para_service');
const assert = require('assert');
const Axios = require('axios');
const _ = require('lodash/object');

const default_branch = 'master';

const serialize_commit = commitDetailMsg => {
  assert(commitDetailMsg.actions, 'action required');
  let {
    branch, commit_message, actions,
    author_name, source_version,
  } = commitDetailMsg;

  if (source_version) {
    commit_message += `|FROM${source_version}`;
  }

  return {
    branch: branch || default_branch,
    commit_message, actions, author_name,
  };
};

const COMMIT_PROPERTIES_TO_PICK = [
  'id', 'short_id', 'author_name', 'authored_date',
  'created_at', 'message',
];
const serializeCommitRecord = commit => {
  const commit_id = commit.id;
  const serialized = _.pick(commit, COMMIT_PROPERTIES_TO_PICK);
  serialized.commit_id = commit_id;
  return serialized;
};

module.exports = app => {
  let attemptToSubmit;
  const config = app.config.gitlab;
  const Client = Axios.create({
    baseURL: `${config.url}`,
    headers: { 'private-token': config.token },
    timeout: 30 * 1000,
  });

  class GitlabService extends BaseParaService {
    get service_name() {
      return 'gitlab';
    }

    get client() {
      return Client;
    }

    get attemptToSubmit() {
      if (!attemptToSubmit) {
        attemptToSubmit = this.ctx.helper
          .attempt(this.submit.bind(this), 3, 3000, true);
      }
      return attemptToSubmit;
    }

    async submit(project_id, commitDetail) {
      const { service } = this;
      const serialized_commit = serialize_commit(commitDetail);
      try {
        const res = await this.client
          .post(`/projects/${project_id}/repository/commits`, serialized_commit);
        const record = serializeCommitRecord(res.data);
        await service.node.commitMany(commitDetail, record);
      } catch (err) {
        const ignorable = this.ignorable_error(err);
        if (!ignorable) throw err;
        this.ctx.logger.info('ignorable error');
      }
    }

    async handleMessage(message) {
      const { ctx } = this;
      try {
        const commitDetailMsg = await ctx.model.Message
          .findOne({ _id: message.value });
        if (!commitDetailMsg || await commitDetailMsg.isLocked) return;
        const { project_id } = commitDetailMsg;
        await this.attemptToSubmit(project_id, commitDetailMsg)
          .catch(async err => { await this.handleError(err, commitDetailMsg); });
        await commitDetailMsg.remove();
      } catch (err) {
        const { logger } = this.ctx;
        logger.error(err);
      }
    }

    ignorable_error(err) {
      err.response = err.response || {};
      err.response.data = err.response.data || {};
      const err_message = err.response.data.message;
      const ignorable = this.config.ignorable_error_messages;
      return err_message && ignorable.includes(err_message);
    }

    async handleError(err, commitDetailMsg) {
      const { logger } = this.ctx;
      logger.error(err);
      commitDetailMsg && await commitDetailMsg.lock();
      throw err;
    }
  }

  return GitlabService;
};











'use strict';

const Service = require('egg').Service;
const Axios = require('axios');

module.exports = app => {
  const config = app.config.keepwork;
  const Client = Axios.create({
    baseURL: `${config.url}/`,
    timeout: 30 * 1000,
  });

  class KeepworkService extends Service {
    get client() {
      return Client;
    }

    parseMarkdown(content) {
      return this.client.post('/es/parser', { content });
    }
  }

  return KeepworkService;
};





'use strict';

const Service = require('egg').Service;
const Axios = require('axios');

module.exports = app => {
  const config = app.config.lesson;
  const Client = Axios.create({
    baseURL: `${config.url}/`,
    headers: { Authorization: config.token },
    timeout: 30 * 1000,
  });

  class LessonService extends Service {
    get client() {
      return Client;
    }

    addPagination(page = 1, per_page = 20, options = {}) {
      options.params = options.params || {};
      options.params['x-page'] = page;
      options.params['x-per-page'] = per_page;
      return options;
    }

    async getLessonsPackages(page = 1, per_page = 20) {
      const options = this.addPagination(page, per_page);
      const res = await Client.get('/admins/packages', options);
      return res.data;
    }

    async getLessonsPackage(pkg) {
      const res = await this.getLessons(pkg.id, 1, 1000);
      const lessons = res.data;
      return {
        id: pkg.id,
        title: pkg.packageName,
        cover: pkg.extra.coverUrl,
        total_lessons: lessons.length,
        description: pkg.intro || '',
        prize: pkg.rmb,
        age_min: pkg.minAge,
        age_max: pkg.maxAge,
        recent_view: pkg.lastClassroomCount,
        created_at: pkg.createdAt,
        updated_at: pkg.updatedAt,
      };
    }

    getLessons(package_id, page = 1, per_page = 20) {
      const options = this.addPagination(page, per_page);
      return Client.get(`/packages/${package_id}/lessons`, options);
    }
  }

  return LessonService;
};





'use strict';

const Service = require('egg').Service;
const _ = require('lodash');

class NodeService extends Service {
  async commitMany(commitDetail, record) {
    const { actions } = commitDetail;
    await Promise.all(actions.map(action => {
      return this.commit(action, record);
    }));
  }

  async commit(action, record) {
    const { ctx } = this;
    const { _id, version } = action;
    const node = await ctx.model.Node.findOne({ _id });
    if (_.isEmpty(node)) return;
    if (_.isEmpty(node.latest_commit)) return;
    const { commit, index } = node.getCommitByVersion(version);
    if (_.isEmpty(commit)) return;
    _.assign(commit, record);
    await ctx.model.Node.updateOne(
      { _id: node._id },
      { $set: { [`commits.${index}`]: commit } }
    );
  }
}

module.exports = NodeService;



'use strict';

const { assert } = require('egg-mock/bootstrap');
const Queue = require('../../../app/lib/queue');

describe('app/lib/queue', () => {
  describe('initialize', () => {
    describe('max length should be a number', () => {
      it('should initialize successfully', () => {
        assert(new Queue(10));
      });
      it('should fail to initialize', () => {
        assert.throws(() => {
          new Queue('string');
        });
      });
    });
  });
  
  
  
  describe('getNextPos method', () => {
    it('should get current next', () => {
      const max = 5;
      const q = new Queue(max);
      const next1 = q.getNextPos(3);
      assert(next1 === 4);

      const next2 = q.getNextPos(4);
      assert(next2 === 0);
    });
  });
  
  
  
  describe('push method and full property', () => {
    const max = 5;
    const q = new Queue(max);

    it('should not be full', () => {
      assert(!q.full);
    });

    it('should fail to push undefined', () => {
      assert.throws(() => {
        q.push(undefined);
      });
    });

    it('should return true', () => {
      for (let i = 0; i < max; i++) assert(q.push(i));
    });

    it('should be full', () => {
      assert(q.full);
    });

    it('should return false when the queue is full', () => {
      assert(!q.push(max + 1));
    });
    it('should not be full', () => {
      q.reset();
      for (let i = 0; i < max; i++) {
        q.push(i);
        if (i === (max - 1)) {
          assert(q.full);
        } else {
          assert(!q.full);
        }
      }
    });
  });

  describe('shift method', () => {
    it('should return correct value', () => {
      const max = 5;
      const q = new Queue(max);
      for (let i = 0; i < max; i++) q.push(i);
      for (let i = 0; i < max; i++) {
        assert(q.shift() === i);
      }

      q.push(1);
      q.push(2);
      q.shift();
      q.push(3);
      assert(q.shift() === 2);
    });
  });





  describe('length property', () => {
    const max = 10;
    const q = new Queue(max);
    it('return 0 when the queue is empty', () => {
      assert(q.length === 0);
    });
    it('return correct length after values pushed', () => {
      for (let i = 0; i < max; i++) {
        q.push(i);
        assert(q.length === (i + 1));
      }
    });
    it('return correct length after values shifted', () => {
      for (let i = 0; i < max; i++) {
        q.shift();
        assert(q.length === (10 - (i + 1)));
      }
    });
  });





  describe('available property', () => {
    it('should return correct available space', () => {
      const max = 10;
      const q = new Queue(max);
      assert(q.available === 10);

      for (let i = 0; i < max; i++) {
        q.push(i);
        assert(q.available === (max - q.length));
      }

      assert(q.full);
      assert(q.available === 0);

      for (let i = 0; i < max; i++) {
        q.shift();
        assert(q.available === (max - q.length));
      }
    });
  });
});



```