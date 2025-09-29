// closureStack.js
// 堆栈使用闭包实现 — 提供完全封装的私有数据
function createClosureStack() {
  const items = [];

  return {
    push(value) {
      items.push(value);
      return this;
    },
    pop() {
      return items.pop();
    },
    peek() {
      return items[items.length - 1];
    },
    isEmpty() {
      return items.length === 0;
    },
    size() {
      return items.length;
    },
    clear() {
      items.length = 0;
      return this;
    },
    toArray() {
      return items.slice();
    }
  };
}

module.exports = { createClosureStack };
