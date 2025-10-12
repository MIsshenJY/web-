# JavaScript 中实现堆栈的三种方式：闭包、原型（prototype）与类（class）

本文档展示并对比三种常见的堆栈（Stack）实现方法：使用函数闭包、原型(prototype) 和类 (class)三种方式。每种实现都包含示例 API（push, pop, peek, isEmpty, size, clear, toArray）。在 Node.js 环境下进行了功能验证和边界测试。



## 源代码文件

- `closureStack.js` — 使用闭包实现，数据私有且封装性强。
- `prototypeStack.js` — 使用构造函数和原型链实现，方法在原型上共享，节省内存。
- `classStack.js` — 使用 ES6 class 语法实现，语法清晰，易于阅读与扩展。
- `run.js` — 在 Node.js 下演示三种实现的行为。

## API 约定
堆栈是一种遵循 "后进先出 (LIFO)" 原则的数据结构，即最后添加的元素最先被移除。
因此在所有实现都遵循同样的简化 API：

- push(value): 添加元素并返回 this（允许链式调用）
- pop(): 弹出并返回栈顶元素
- peek(): 返回栈顶元素但不弹出
- isEmpty(): 返回是否为空（布尔）
- size(): 返回当前元素数量
- clear(): 清空栈并返回 this
- toArray(): 返回元素浅拷贝（从底到顶）

## 实现对比（优缺点）

1. 闭包（`closureStack.js`）：使用闭包将堆栈数据封装在函数作用域内，外部无法直接访问堆栈数据。
  - 优点：数据私有且安全，不会被外部误操作。
  - 缺点：每次创建实例都会分配一套方法，对大量实例来说可能有内存开销。
  - 复杂度：push/pop/peek/isEmpty/size 为 O(1)。toArray 为 O(n)。
  - 边界行为：pop/peek 对空栈返回 undefined。
  - 适用场景：需要强封装、限制外部访问时，或做小型模块时使用。

2. 原型（`prototypeStack.js`）：使用构造函数和原型链实现堆栈，所有方法共享同一个原型对象。
  - 优点：通过原型共享方法可以避免在堆上为每个实例创建重复函数，节省内存；兼容老式 JS 环境。
  - 缺点：内部数组是实例属性，仍然能被外部通过属性名访问（例如 `inst._items`），因此封装不如闭包。
  - 复杂度：push/pop/peek/isEmpty/size 为 O(1)。toArray 为 O(n)。
  - 边界行为：pop/peek 对空栈返回 undefined。
  - 适用场景：需要创建大量实例且关注内存占用时使用。

3. 类（`classStack.js`）：使用 ES6 class 语法实现堆栈，语法清晰、易读、支持继承。
  - 优点：语法现代、可读性好、支持继承（extends）、更契合现代项目风格。
  - 缺点：私有性仍依赖约定（下划线）或需要使用私有字段（#），老环境需转译。
  - 复杂度：push/pop/peek/isEmpty/size 为 O(1)。toArray 为 O(n)。
  - 边界行为：pop/peek 对空栈返回 undefined。
  - 适用场景：现代代码库、需要继承或与其他类互操作时使用。

## 运行示例

在包含这些文件的目录下，用 Node.js 运行 `run.js`：

```bash
node run.js
```

- 输出将展示三种实现的行为（size、peek、pop 等）。
== closureStack ===
 after push 1,2,3 -> size: 3
 after peek (expect 3): 3
 after pop (expect 3): 3
 after toArray (expect [1,2]): (2) [1, 2]
 after isEmpty (expect false): false
 after clear isEmpty (expect true): true
 after pop on empty (expect undefined): undefined
 after peek on empty (expect undefined): undefined
 after push a,b -> toArray (expect ["a","b"]): (2) ['a', 'b']
 ```(prototype / class 同上)

 - 验证结果：
  - 所有操作（push, pop, peek, isEmpty, size, clear, toArray）在三种实现中行为一致。
  - 空栈操作（pop, peek）返回预期值（undefined）。
  - 非空栈操作（push, pop, peek, size, isEmpty）返回预期值。
  - toArray 返回元素浅拷贝（从底到顶）。
三种实现的外部行为一致，均满足设计的 API 与边界约定。

## 学习总结
通过这次练习，我对闭包与原型链的区别、类语法的便利以及设计 API 时的取舍（封装 vs 性能 vs 可扩展性）有了更深刻的理解。
1. 封装与私有性
  - 闭包方式：提供最强的封装性，栈数据作为函数内部变量存在，完全私有，外部无法直接访问或修改，从语言层面保障了数据安全性。
  - 原型方式：依赖命名约定（如下划线_stack）模拟私有性，本质上属性仍可被外部访问和修改，私有性较弱。
  - 类方式：通过 ES6 私有字段语法（#前缀）实现真正私有性，或使用命名约定兼容旧环境，私有性可控性较强。

2. 操作性能与内存
  - 操作性能：在单个实例的常见操作（push/pop 等）中，三种方式性能差异可忽略不计。
  - 内存占用：
    - 闭包方式：每次创建实例都会重新分配一套方法，当需要创建大量实例时，可能产生较高内存开销。
    - 原型与类实现：通过原型链共享方法，所有实例复用同一套方法定义，内存占用更低，尤其适合大量实例场景。

3. 语法与扩展性
  - 语法特性：
    - 类语法（class）属于 ES6 + 现代语法，结构清晰、可读性好，符合主流面向对象编程习惯。
    - 原型方式需手动操作原型链，语法相对繁琐，维护成本较高。
    - 闭包方式基于函数工厂模式，语法简洁但结构相对松散。
  - 继承与扩展：
    - 原型和类支持自然的继承机制（原型链继承 /extends关键字），便于方法复用和层级扩展。
    - 闭包实现不适合直接继承，扩展需通过工厂函数组合或返回额外方法，灵活性较低。

4. 场景选择建议
  - 优先闭包：当需要严格的数据封装性、接口稳定且无需继承扩展时（如工具类组件）。
  - 优先类方式：现代项目中推荐使用，兼顾可读性、可维护性和扩展性，适合需要继承或团队协作场景。
  - 优先原型方式：需兼容旧环境，或对内存占用有极致要求且创建大量实例时（类的底层本质仍是原型，类语法是更优选择）。