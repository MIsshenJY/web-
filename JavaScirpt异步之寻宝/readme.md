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
