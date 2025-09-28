<<<<<<< HEAD
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

    static nextStep() {
      return new Promise((resolve) => {
        setTimeout(() => {
          const random = Math.random();
            if (random < 0.5) {
              // 有提示：返回方向（非 null）和要打印的信息
              resolve({ direction: '向东南方前进3公里', message: ' 线索中隐藏了一个方向...' });
            } else {
              // 无提示：direction 为 null，但仍返回要打印的信息
              resolve({ direction: null, message: '埋头继续向前走...' });
            }
        }, 1200);
      });
    }
    static traverseDesert(direction) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          if (!direction) {
            reject("没有方向，迷失在沙漠!");
          }
          resolve(`找到了方向:${direction}，成功穿越沙漠，看到了神庙的轮廓!`);
        }, 2000);
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
    .then(decodedMessage => {
      console.log(decodedMessage);
      return TreasureMap.nextStep();
    })
    .then(({ direction, message }) => {
      console.log(message);
      return TreasureMap.traverseDesert(direction);
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

=======
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

    static nextStep() {
      return new Promise((resolve) => {
        setTimeout(() => {
          const random = Math.random();
            if (random < 0.5) {
              // 有提示：返回方向（非 null）和要打印的信息
              resolve({ direction: '向东南方前进3公里', message: ' 线索中隐藏了一个方向...' });
            } else {
              // 无提示：direction 为 null，但仍返回要打印的信息
              resolve({ direction: null, message: '埋头继续向前走...' });
            }
        }, 1200);
      });
    }
    static traverseDesert(direction) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          if (!direction) {
            reject("没有方向，迷失在沙漠!");
          }
          resolve(`找到了方向:${direction}，成功穿越沙漠，看到了神庙的轮廓!`);
        }, 2000);
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
    .then(decodedMessage => {
      console.log(decodedMessage);
      return TreasureMap.nextStep();
    })
    .then(({ direction, message }) => {
      console.log(message);
      return TreasureMap.traverseDesert(direction);
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

>>>>>>> 8792f3a79d2b6128d3065c8221c5b7b57b712ad7
