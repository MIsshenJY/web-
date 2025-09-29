// classStack.js
// 堆栈使用 ES6 class 实现 — 语法清晰，适合现代代码风格
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
