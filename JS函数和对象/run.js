// example-run.js
// 在 Node.js 下演示三种堆栈实现的用法

const { createClosureStack } = require('./closureStack');
const PrototypeStack = require('./prototypeStack');
const ClassStack = require('./classStack');

function demoStack(apiName, stack) {
  console.log('---', apiName, '---');
  stack.push(1).push(2).push(3);
  console.log('size:', stack.size());
  console.log('peek:', stack.peek());
  console.log('pop:', stack.pop());
  console.log('toArray:', stack.toArray());
  console.log('isEmpty:', stack.isEmpty());
  stack.clear();
  console.log('after clear isEmpty:', stack.isEmpty());
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
