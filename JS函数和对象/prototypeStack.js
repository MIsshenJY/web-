// prototypeStack.js
// 堆栈使用构造函数 + 原型链实现 — 支持共享方法和节省内存
function PrototypeStack() {
  this._items = [];
}

PrototypeStack.prototype.push = function(value) {
  this._items.push(value);
  return this;
};

PrototypeStack.prototype.pop = function() {
  return this._items.pop();
};

PrototypeStack.prototype.peek = function() {
  return this._items[this._items.length - 1];
};

PrototypeStack.prototype.isEmpty = function() {
  return this._items.length === 0;
};

PrototypeStack.prototype.size = function() {
  return this._items.length;
};

PrototypeStack.prototype.clear = function() {
  this._items.length = 0;
  return this;
};

PrototypeStack.prototype.toArray = function() {
  return this._items.slice();
};

module.exports = PrototypeStack;
