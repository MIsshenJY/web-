// 在 Node.js 下演示并验证三种堆栈实现的用法，包含边界测试

const { createClosureStack } = require('./closureStack');
const PrototypeStack = require('./prototypeStack');
const ClassStack = require('./classStack');

function demoStack(apiName, stack) {
  console.log('===', apiName, '===');

  // 正常使用场景
  stack.push(1).push(2).push(3);
  console.log('after push 1,2,3 -> size:', stack.size());
  console.log('peek (expect 3):', stack.peek());
  console.log('pop (expect 3):', stack.pop());
  console.log('toArray (expect [1,2]):', stack.toArray());

  // 边界与链式调用验证
  console.log('isEmpty (expect false):', stack.isEmpty());
  stack.clear();
  console.log('after clear isEmpty (expect true):', stack.isEmpty());

  // 空栈操作：peek/pop 在空栈上应返回 undefined
  console.log('pop on empty (expect undefined):', stack.pop());
  console.log('peek on empty (expect undefined):', stack.peek());

  // 链式风格验证
  stack.push('a').push('b');
  console.log('after push a,b -> toArray (expect ["a","b"]):', stack.toArray());

  console.log();
}

// closure
const c = createClosureStack();
demoStack('closureStack', c);

// prototype
const p = new PrototypeStack();
demoStack('prototypeStack', p);

// class
const cl = new ClassStack();
demoStack('classStack', cl);

console.log('Demo finished');
