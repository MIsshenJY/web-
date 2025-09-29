// closureStack.js
// 堆栈 — 闭包实现 (factory + closure)
// 说明：该实现把内部数据完全封装在闭包中，外部不可直接访问。
// 学习笔记：闭包提供了最强的私有性，但每次创建实例都会分配一套方法，
// 对大量实例来说可能有内存开销。
// 复杂度：push/pop/peek/isEmpty/size 为 O(1)。toArray 为 O(n)。

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

    isEmpty() {
      return items.length === 0;
    },

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
