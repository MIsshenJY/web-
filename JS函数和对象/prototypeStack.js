// prototypeStack.js
// 堆栈 — 构造函数 + 原型实现
// 说明：方法放在原型上，节省每个实例的内存开销，适合大量实例场景。
// 学习笔记：通过原型共享方法可以避免在堆上为每个实例创建重复函数，
// 但实例属性（如 _items）仍可以被外部访问，封装性不及闭包。
// 复杂度：push/pop/peek/isEmpty/size 为 O(1)。toArray 为 O(n)。

function PrototypeStack() {
  // 使用约定的私有属性名（下划线）来提示不应该被外部直接访问
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
