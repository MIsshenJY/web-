// 堆栈 — 构造函数 + 原型实现

function PrototypeStack() {
  // 使用约定的私有属性名（下划线）来提示不应该被外部直接访问
  this._items = [];
}

// 添加元素并返回 this，便于链式调用
PrototypeStack.prototype.push = function(value) {
  this._items.push(value);
  return this;
};

// 弹出并返回栈顶元素；当为空时返回 undefined（与 Array.prototype.pop 行为一致）
PrototypeStack.prototype.pop = function() {
  return this._items.pop();
};

// 返回栈顶元素但不弹出；空栈返回 undefined
PrototypeStack.prototype.peek = function() {
  return this._items[this._items.length - 1];
};

// 栈是否为空
PrototypeStack.prototype.isEmpty = function() {
  return this._items.length === 0;
};

// 返回栈的元素数量
PrototypeStack.prototype.size = function() {
  return this._items.length;
};

// 清空栈并返回 this（链式）
PrototypeStack.prototype.clear = function() {
  this._items.length = 0;
  return this;
};

// 返回栈的元素数组副本（不改变原栈）
PrototypeStack.prototype.toArray = function() {
  return this._items.slice();
};

module.exports = PrototypeStack;
