// classStack.js
// 堆栈 — ES6 class 实现
// 说明：class 提供清晰语法，便于阅读与继承。当前使用约定的私有属性名 `_items`。
// 学习笔记：如果你想更严格的私有性，可以改用私有字段（例如 `#items`），
// 但那会要求运行环境支持或通过 Babel 转译。
// 复杂度：push/pop/peek/isEmpty/size 为 O(1)。toArray 为 O(n)。

class ClassStack {
  constructor() {
    this._items = [];
  }

  push(value) {
    this._items.push(value);
    return this;
  }

  pop() {
    return this._items.pop();
  }

  peek() {
    return this._items[this._items.length - 1];
  }

  isEmpty() {
    return this._items.length === 0;
  }

  size() {
    return this._items.length;
  }

  clear() {
    this._items.length = 0;
    return this;
  }

  toArray() {
    return this._items.slice();
  }
}

module.exports = ClassStack;
