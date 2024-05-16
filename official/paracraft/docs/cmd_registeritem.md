<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/registeritem`**

**quick ref:**
> /registeritem [-alphaTestTexture] [-blendedTexture] [-light] [block_id:2000-2999] [texture] [base_block_id] 

**description:**

```
create a new item based on an icon and block id. 
e.g.
/registeritem 2000 Texture/blocks/lapis_ore.png 234					thin plate
/registeritem 2001 Texture/blocks/items/1013_Carrot.png 115			flower
/registeritem					it will create using the inventory of fromEntity. The first slot item must be a painting, the second one is base block if any. 
/registeritem -alphaTestTexture 2002 Texture/blocks/glass_pane.png 6 				transparent block emitting light
/registeritem -blendedTexture 2003 Texture/blocks/ice.png 6 				alpha-blended block emitting light
/registeritem -light 2004 Texture/blocks/leaves_birch.png 86 				a tree leave block emitting light
```

<!-- END_AUTOGEN-->

自定义新的方块类型
- 参数`base_block_id`： 表示从哪个方块派生。 派生后将继承它的属性。

### 例子

- `/registeritem -blendedTexture 2003 Texture/blocks/ice.png 6`
  基于`灯方块id=6`, 派生一个id=2003的方块。 并使用贴图`Texture/blocks/ice.png`,并且是半透明的`-blendedTexture`
这样就创建了即会发光又透明的方块了。 

> 然后你可以用`/take 2003` 获得新的方块
