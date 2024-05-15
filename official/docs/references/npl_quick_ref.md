## NPL常用语法 速查表

NPL语言的语法100%兼容lua, 并有扩充。下面仅包含本书理论部分提到的常用语法。
```lua
-- 两个横岗代表单行注释

--[[
     首尾加入两个 [ 和 ] 可以为多行注释
]]

----
-- 1. 变量与控制
----
local num = 42;  -- 所有的数字都是浮点数(double)

s = '相同的字符串在内存中只有一个Copy'  
t = "双引号也可以"; -- `;` 每行代码的结尾可以加入`;`也可不加
u = [[ 在开头和结尾
       的两个中括号
       代表多行文本字符串.]]
-- 'nil' 为空的意思. 例子中t不再指向任何存储单元.
-- 当没有任何变量指向某个存储单元时，存储单元很快会被从内存中释放。
t = nil  

-- do 和 end 之间的代码是一个代码区间
while num < 50 do
  num = num + 1
end

-- 如果:
if (num <= 40) then
  log('小于等于 40')
elseif ("string" == 40 or s) then
  log('任意类型的变量之间都可以比较');
elseif s ~= 'NPL' then
  log('if语句也可以不加前后的括号()')
else
  -- 变量默认为全局变量，代码方块中情况特殊
  thisIsGlobal = 5  -- 注意变量是区分大小写的

  -- 如何定义一个本地变量：
  local line = "这个变量只能在下个`end`或文件结束前使用"

  -- 连接2个字符串用 .. 函数:
  log("第一个字符串" .. line)
end

-- 从来没有赋值过的变量会返回nil
-- 下面代码并没有语法错误
foo = anUnknownVariable  -- 现在 foo == nil.

aBoolValue = false  -- 真true与假false

-- 对于if语句只有nil 和 false 是假的; 0 和 ''都是真！
if (not aBoolValue) then log('false') end

-- 'or' 和 'and' 函数返回最近的输入
ans = (aBoolValue and 'yes') or 'no'  --> 'no'

local nSum = 0;
for i = 1, 100 do  -- i包含1和100是本地变量
   nSum = nSum + i
end

-- 用 "100, 1, -1" 可以递减:
-- 区间的三个输入分别是 开始值, 结束值[, 递增增].
nSum = 0
for i = 100, 1, -1 do 
   nSum = nSum + i 
end

-- 另一种罕见的循环, 循环直到nSum == 0:
repeat
  nSum = nSum - 1
until nSum == 0

----
-- 2. 函数
----
function fib(n)
  if n < 2 then return 1 end
  return fib(n - 2) + fib(n - 1)
end

-- 函数的返回值, 函数调用, 和赋值语句都支持多个输入
-- 不匹配的输入，值为nil;
-- 多出来的输入会被自动忽略.

x, y, z = 1, 2, 3, 4
-- 现在 x = 1, y = 2, z = 3, 但是 4 会被忽略.

function bar(a, b, c)
  log(string.format("%s %s %s", a, b or "b", c))
  return 4, 8, 15, 16, 23, 42
end

x, y = bar("NPL")  --> 输出 "NPL b nil"
-- 现在 x = 4, y = 8, 数字 15..42 被忽略.

-- 函数也是变量，可以是全局或本地的.
-- 下面定义函数f的方式是等价的：
function f(x) 
  return x * x 
end
f = function (x) 
  return x * x 
end

-- 下面的方式也是等价的
local function g(x) return math.sin(x) end
local g; g  = function (x) return math.sin(x) end

-- 当函数只有一个输入时，也可以不加括号:
log 'hello'  -- 正确的语法.

----
-- 3. 表.
----
-- 表是NPL语言中唯一的复合数据结构;

-- 默认情况下关键字为字符串类型: "key1", "key2"
t = {key1 = 'value1', key2 = false}

-- 可以用.来引用表中的数据:
log(t.key1)  -- 输出 'value1'.
t.newKey = {}  -- 可在运行过程中可随时插入新的数据.
t.key2 = nil   -- 将key2从表中删除.

-- 任何不是nil的数据类型都可以为表的关键字
u = {['@!#'] = 'blabla', [{}] = 1982, [3.14] = 'pi'}
log(u[3.14])  -- 输出 "pi"


for key, val in pairs(u) do  -- 获取表中的每个数据.
  log(key, val)
end

-- _G 是一个特殊的表，里面有所有的全局变量.
_G.test = 1
log(test == 1)  -- 输出 "true"

-- 表可以当成列表或数组使用:

-- 默认为从1开始递增的整数为关键字:
v = {'value1', 'value2', 1.21, 'gigawatts'}
for i = 1, #v do  -- #v 代表v中整形关键字的数据的数目.
  log(v[i]) -- 注意数组从1开始，不是0
end

-- Have fun with NPL!
```