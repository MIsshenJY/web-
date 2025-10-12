// 堆栈 — 闭包实现 (factory + closure)

function createClosureStack() {
  const items = [];

  // 返回的对象把操作函数暴露为闭包内的接口。
  return {
    // 添加元素并返回 this，便于链式调用
    push(value) {
      items.push(value);
      return this;
    },

    // 弹出并返回栈顶元素；当为空时返回 undefined（与 Array.prototype.pop 行为一致）
    pop() {
      return items.pop();
    },

    // 返回栈顶元素但不弹出；空栈返回 undefined
    peek() {
      return items[items.length - 1];
    },

    // 栈是否为空
    isEmpty() {
      return items.length === 0;
    },

    // 返回栈的元素数量
    size() {
      return items.length;
    },

    // 清空栈并返回 this（链式）
    clear() {
      items.length = 0;
      return this;
    },

    // 返回从底到顶的浅拷贝数组，不暴露内部引用
    toArray() {
      return items.slice();
    }
  };
}

module.exports = { createClosureStack };
