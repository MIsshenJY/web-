// 模拟宝藏地图API
class TreasureMap {
    static getInitialClue() {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve("在古老的图书馆里找到了第一个线索...");
        }, 1000);
      });
    }
  
    static decodeAncientScript(clue) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          if (!clue) {
            reject("没有线索可以解码!");
          }
          resolve("解码成功!宝藏在一座古老的神庙中...");
        }, 1500);
      });
    }
  
    static searchTemple(location) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          const random = Math.random();
          if (random < 0.5) {
            reject("糟糕!遇到了神庙守卫!");
          }
          resolve("找到了一个神秘的箱子...");
        }, 2000);
      });
    }
  
    static openTreasureBox() {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve("恭喜!你找到了传说中的宝藏!");
        }, 1000);
      });
    }
  }

  function findTreasureWithPromises() {
    TreasureMap.getInitialClue()
      .then(clue => {
        console.log(clue);
        return TreasureMap.decodeAncientScript(clue);
      })
      .then(location => {
        console.log(location);
        return TreasureMap.searchTemple(location);
      })
      .then(box => {
        console.log(box);
        return TreasureMap.openTreasureBox();
      })
      .then(treasure => {
        console.log(treasure);
      })
      .catch(error => {
        console.error("任务失败:", error);
      });
  }

  findTreasureWithPromises()

  // ...existing code...
// 以下为新增的有趣情节与进阶流程（异步实现）

// 商人：可能给你一个提示或一把“钥匙”
TreasureMap.meetWiseMerchant = function() {
  return new Promise((resolve) => {
    setTimeout(() => {
      const hasKey = Math.random() < 0.4; // 40% 概率得到钥匙
      const hint = hasKey ? "商人给了你一把古铜钥匙和一句低语: '月亮在祭坛之上'." : "商人只给了你一条模糊的提示: '小心陷阱.'";
      resolve({ hasKey, hint });
    }, 800);
  });
};

// 过断桥：有概率失败，但允许重试一次
TreasureMap.crossRopeBridge = function() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const success = Math.random() < 0.7;
      if (success) resolve("顺利通过断桥，来到了神庙山脚.");
      else reject("断桥断裂，你摔下去了!");
    }, 700);
  });
};

// 神庙谜题：需要线索或商人的提示
TreasureMap.solveTempleRiddle = function(hint) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (!hint) {
        reject("没有线索，无法解开神庙谜题!");
        return;
      }
      // 根据 hint 的关键词提高成功率
      const success = /月亮|祭坛|钥匙/.test(hint) ? Math.random() < 0.9 : Math.random() < 0.5;
      if (success) resolve("你解开了祭坛的谜题，发现了隐藏通道!");
      else reject("谜题未解开，祭坛陷阱触发!");
    }, 1200);
  });
};

// 解陷阱：有道具（钥匙）时更容易避免失败
TreasureMap.disarmTrap = function(hasKey) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const success = hasKey ? true : Math.random() < 0.6;
      if (success) resolve("你成功解除了陷阱，继续前进.");
      else reject("陷阱触发，你受了点伤，暂时撤退!");
    }, 900);
  });
};

// 最终守卫：可以尝试交涉（小概率成功）或战斗（随机）
TreasureMap.finalGuardian = function() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const action = Math.random();
      if (action < 0.4) resolve("守卫被你的智慧说服，允许你带走宝藏.");
      else if (action < 0.8) reject("守卫不满，发动攻击!");
      else resolve("你用勇气战胜了守卫，拿走了宝藏（受了点伤）.");
    }, 1100);
  });
};

// 用 async/await 实现的进阶寻宝流程，包含分支与重试
async function findTreasureAdvanced() {
  try {
    const clue = await TreasureMap.getInitialClue();
    console.log(clue);

    // 遇见商人，可能获得钥匙或提示
    const merchant = await TreasureMap.meetWiseMerchant();
    console.log("遇见商人:", merchant.hint);

    // 过桥，若第一次失败，重试一次
    try {
      const cross = await TreasureMap.crossRopeBridge();
      console.log(cross);
    } catch (e) {
      console.warn(e, "正在重试...");
      const retry = await TreasureMap.crossRopeBridge();
      console.log(retry);
    }

    // 解码线索（可用商人提示提高成功率）
    const location = await TreasureMap.decodeAncientScript(clue);
    console.log(location);

    // 解谜（使用商人的提示）
    const riddle = await TreasureMap.solveTempleRiddle(merchant.hint);
    console.log(riddle);

    // 搜索神庙，可能遇到箱子或陷阱
    let box;
    try {
      box = await TreasureMap.searchTemple(location);
      console.log(box);
    } catch (e) {
      console.warn("搜索受阻:", e);
      // 如果遇到守卫，尝试与守卫周旋（调用 finalGuardian）
      const guardianResult = await TreasureMap.finalGuardian();
      console.log("与守卫的交涉结果:", guardianResult);
      // 若守卫让路，继续搜索
      box = "在守卫允许后找到的箱子...";
    }

    // 如果找到箱子，可能有陷阱，尝试解除
    try {
      const disarm = await TreasureMap.disarmTrap(merchant.hasKey);
      console.log(disarm);
    } catch (e) {
      console.error("解陷阱失败:", e);
      throw e; // 终止任务
    }

    // 最后打开箱子（如果有钥匙，可能直接获得更好宝藏）
    const treasure = await TreasureMap.openTreasureBox();
    console.log(merchant.hasKey ? treasure + "（钥匙使宝藏更丰富）" : treasure);

  } catch (error) {
    console.error("进阶任务失败:", error);
  }
}

// 调用进阶流程（可以注释掉与原函数冲突）
findTreasureAdvanced();