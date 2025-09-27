// 实现 map 函数
function myMap(array, callback) {
    const result = [];
    for (let i = 0; i < array.length; i++) {
        result.push(callback(array[i], i, array));
    }
    return result;
}

// 实现 filter 函数
function myFilter(array, callback) {
    const result = [];
    for (let i = 0; i < array.length; i++) {
        if (callback(array[i], i, array)) {
            result.push(array[i]);
        }
    }
    return result;
}

// 测试用例
const arr = [1, 2, 3, 4, 5];

// 测试 myMap
const mapResult = myMap(arr, x => x * 2);
console.log('myMap 测试结果:', mapResult); // [2, 4, 6, 8, 10]

// 测试 myFilter
const filterResult = myFilter(arr, x => x % 2 === 0);
console.log('myFilter 测试结果:', filterResult); // [2, 4]
