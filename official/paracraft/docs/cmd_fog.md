<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/fog`**

**quick ref:**
> /fog [-color|skycolor|fogstart|fogend] values

**description:**

```
Change fog color and range  e.g. 
-- if no option specified it will set fogstart
-- 若无参数指定则设置“默认雾”

/fog 100
-- only start fog after 100 meters and end by view_distance
-- 从视野消失前数100m开始设置迷雾

/fog 0.6
-- if value is smaller than 1, it means 0.6*view_distance
-- 如果参数小于1 ， 则等价于 /fog 0.6*可视距离

/fog -color 1 1 1
-- change fog color to white, and disable auto fog color according to time
-- 修改雾气颜色为白色，并且取消随着游戏地图时间而更改的自动雾气颜色

/fog
-- enable auto fog color according to time of day
-- 开启默认雾气效果

/fog -skycolor 1 1 1
-- change the sky's color to white. 
-- 修改天空颜色为白色

/fog -fogstart 80
-- fog start distance
-- 设置雾气开始的距离

/fog -fogend 100
-- fog end distance
-- 设置雾气结束的距离
```



<!-- END_AUTOGEN-->



打开场景中的雾，可以改变雾的颜色和范围大小。