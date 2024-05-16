<!-- BEGIN_AUTOGEN: do NOT edit in this block -->

**command: `/paralife`**

**quick ref:**
> /paralife [show|hide|buy|checkbuy|openbook] [-addbag|-askonce|setbag|setbagtype|pickbagitem|clearbag|showbag]

**description:**

```
paralife logic. 
@param show: show paralife mode [-showplayer -noedit -nobackbutton -nobookbutton]
@param hide: hide paralife mode
@param setbag [x|name],[y],[z]: set the data source of paralife bag with a movie entity's pos or live entity's name
@param addbag [x|name],[y],[z]: add a paralife bag data source with a live entity
@param clearbag: clear the paralife bag
@param buy [-askonce] product_id: buy a product by product_id. Product is bound to mac address.  
  if -askonce is not specified, we will block the user until payment is done.
@param checkbuy|buy product_id: return true if the given product(product_id) is already purchased.
@param openbook: open the default manul book. 
@param pathfinding: handles pathfinding logic. [-jumpHeightWhileHidden] set jump height while hidden
e.g.
/paralife show -showplayer -noedit -nobackbutton -nobookbutton
/paralife hide
/paralife setbagtype grid
/paralife setbagtype gridbottom  |  gridtop  [-count=8] [-size=48]
/paralife showbag
/paralife setbag 19200 11 19200
/paralife addbag myLiveModelName
/paralife pickbagitem staticTag|templates/xxx.bmx
/paralife clearbag
/paralife checkbuy project_123123
/paralife buy -askonce project_123123
/paralife openbook
/paralife pathfinding -jumpHeightWhileHidden 4
```

<!-- END_AUTOGEN-->


## 例子1
`/paralife show -noedit -nobackbutton -nobookbutton -nofacial`

- noedit: 没有编辑按钮， 只有play按钮
- nobackbutton: 没有右上角返回按钮
- nobookbutton: 没有右上角书按钮
- nofacial: 没有换脸按钮