<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/sky`**

**quick ref:**
> /sky [-tex filename] [-add filename] [-clear] [-none] [-sim] [-sun sun_size sun_glow] [-moon moon_size moon_glow] [-cloud thickness]  [sim|white|green|filename]

**description:**

```
change sky model or its textures
-- changing to simulated sky
/sky sim
-- changing to a given model
/sky model/skybox/skybox6/skybox6.x  
-- setting sky's replaceable texture, file can be relative to world dir.
/sky -tex Texture/blocks/cake_top.png
-- use empty white texture
/sky -tex
-- sun size and glow size defaults to 500, 12
/sky -sun sun_size[10-1000] sun_glow
/sky -sun 500 12
-- moon size and glow size defaults to 500, 12
/sky -moon moon_size[10-1000] moon_glow
/sky -moon 500 12
-- cloud density
/sky -cloud density[0-1]
/sky -cloud 0.1
-- add a sub animated mesh to the sky entity. Mesh center should be 0,0,0. radius is 0.5.
/sky -add animated_sun.fbx
-- clear all child meshes
/sky -clear
-- do not show primary sky box. use submeshes only. 
/sky -none
```

<!-- END_AUTOGEN-->
/sky -tex 000.jpg 此命令为引用地图文件中的天空素材图片。