<<<<<<< HEAD
# JavaScript异步之寻宝
主要结构：TreasureMap类
主要方法：
  1. getInitialClue()：1秒后返回第一个线索（resolve）。
  2. decodeAncientScript(clue)：1.5秒后解码线索；如果没有线索则reject（解码失败）。
  3. searchTemple(location)：2秒后在神庙里搜索，有约 50% 的概率 reject（遇到守卫），否则 resolve（找到箱子）。
  4. openTreasureBox(): 1 秒后 resolve（打开箱子，得到宝藏）。

执行流程：findTreasureWithPromises() 
通过 then 方法链式调用各个步骤，把每个步骤的返回值传递给下一个步骤。
  1. 先getInitialClue()，打印线索；
  2. 再decodeAncientScript(clue)，打印位置说明；
  3. 然后searchTemple(location)，打印找到箱子的消息；
  4. 最后openTreasureBox()，打印最终宝藏消息。
如果任何一步失败（reject），则捕获错误并打印失败原因。

## 增加新的有趣的寻宝情节
增加新的步骤：寻找方向，得到方向进行下一步，否则进入下一步但是返回失败。

### 使用async/await重写寻宝过程
主要结构：TreasureMap类（同上）
主要方法：（同上）
执行流程：findTreasure()
通过async/await关键字，将异步操作转换为同步代码，使代码更加清晰和易读。
  1. 先await getInitialClue()，打印线索；
  2. 再await decodeAncientScript(clue)，打印位置说明；
  3. 然后await searchTemple(location)，打印找到箱子的消息；
  4. 最后await openTreasureBox()，打印最终宝藏消息。
如果任何一步失败（reject），则使用try/catch捕获错误并打印失败原因。

#### 设计动画页面展示寻宝过程
1. 可以使用HTML/CSS/JavaScript创建一个简单的网页，展示寻宝的每个步骤。
2. 在每个步骤完成后，更新页面内容，显示当前状态和结果。
3. 在失败时，显示错误信息，并提供重新开始的选项。
=======
# JavaScript异步之寻宝
主要结构：TreasureMap类
主要方法：
  1. getInitialClue()：1秒后返回第一个线索（resolve）。
  2. decodeAncientScript(clue)：1.5秒后解码线索；如果没有线索则reject（解码失败）。
  3. searchTemple(location)：2秒后在神庙里搜索，有约 50% 的概率 reject（遇到守卫），否则 resolve（找到箱子）。
  4. openTreasureBox(): 1 秒后 resolve（打开箱子，得到宝藏）。

执行流程：findTreasureWithPromises() 
通过 then 方法链式调用各个步骤，把每个步骤的返回值传递给下一个步骤。
  1. 先getInitialClue()，打印线索；
  2. 再decodeAncientScript(clue)，打印位置说明；
  3. 然后searchTemple(location)，打印找到箱子的消息；
  4. 最后openTreasureBox()，打印最终宝藏消息。
如果任何一步失败（reject），则捕获错误并打印失败原因。
>>>>>>> 8792f3a79d2b6128d3065c8221c5b7b57b712ad7
