// 模拟宝藏地图API类，包含一系列异步方法模拟寻宝过程
class TreasureMap {
    // 获取初始线索
    static getInitialClue() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve("在古老的图书馆里找到了第一个线索...");
            }, 1000); // 模拟1秒延迟
        });
    }

    // 解码古文字线索
    static decodeAncientScript(clue) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (!clue) {
                    reject("没有线索可以解码!"); // 如果没有线索，抛出错误
                }
                resolve("解码成功!宝藏在一座古老的神庙中...");
            }, 1500); // 模拟1.5秒延迟
        });
    }

    // 获取下一步的方向或提示
    static nextStep() {
        return new Promise((resolve) => {
            setTimeout(() => {
                const random = Math.random(); // 随机生成方向提示
                if (random < 0.5) {
                    // 有方向提示
                    resolve({ direction: '向东南方前进3公里', message: ' 线索中隐藏了一个方向...' });
                } else {
                    // 无方向提示
                    resolve({ direction: null, message: '埋头继续向前走...' });
                }
            }, 1200); // 模拟1.2秒延迟
        });
    }

    // 穿越沙漠
    static traverseDesert(direction) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (!direction) {
                    reject("没有方向，迷失在沙漠!"); // 如果没有方向，抛出错误
                }
                resolve(`找到了方向:${direction}，成功穿越沙漠，看到了神庙的轮廓!`);
            }, 2000); // 模拟2秒延迟
        });
    }

    // 在神庙中搜索宝藏
    static searchTemple(location) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                const random = Math.random(); // 随机决定是否遇到守卫
                if (random < 0.5) {
                    reject("糟糕!遇到了神庙守卫!"); // 遇到守卫，抛出错误
                }
                resolve("找到了一个神秘的箱子...");
            }, 2000); // 模拟2秒延迟
        });
    }

    // 打开宝藏箱
    static openTreasureBox() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve("恭喜!你找到了传说中的宝藏!");
            }, 1000); // 模拟1秒延迟
        });
    }
}

// 使用async/await重写寻宝过程
async function findTreasure() {
    try {
        // 获取初始线索
        const clue = await TreasureMap.getInitialClue();
        console.log(clue);

        // 解码线索
        const decodedMessage = await TreasureMap.decodeAncientScript(clue);
        console.log(decodedMessage);

        // 获取下一步提示
        const { direction, message } = await TreasureMap.nextStep();
        console.log(message);

        // 穿越沙漠
        const location = await TreasureMap.traverseDesert(direction);
        console.log(location);

        // 搜索神庙
        const box = await TreasureMap.searchTemple(location);
        console.log(box);

        // 打开宝藏箱
        const treasure = await TreasureMap.openTreasureBox();
        console.log(treasure);
    } catch (error) {
        // 捕获并处理错误
        console.error("任务失败:", error);
    }
}

// 暴露到全局，供页面脚本调用
window.TreasureMap = TreasureMap;
window.findTreasure = findTreasure;