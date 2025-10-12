// 堆栈 — ES6 class 实现

class ClassStack {
  // 私有属性：使用 # 定义，只能在类内部访问
  #stack = [];

  // 添加元素并返回 this，便于链式调用
  push(value) {
    this.#stack.push(value);
    return this;
  }

  // 删除并返回栈顶元素
  pop() {
    return this.#stack.pop();
  }

  // 返回栈顶元素（不删除）
  peek() {
    return this.#stack[this.#stack.length - 1];
  }

  // 栈是否为空
  isEmpty() {
    return this.#stack.length === 0;
  }

  // 返回栈的元素数量
  size() {
    return this.#stack.length;
  }

  // 清空栈
  clear() {
    this.#stack.length = 0;
    return this;
  }

  // 返回栈的元素数组副本（不改变原栈） 
  toArray() {
    return this.#stack.slice(); 
  }
}

module.exports = ClassStack;
