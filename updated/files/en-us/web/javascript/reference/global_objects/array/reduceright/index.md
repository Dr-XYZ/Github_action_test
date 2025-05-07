````markdown
---
title: Array.prototype.reduceRight()
slug: Web/JavaScript/Reference/Global_Objects/Array/reduceRight
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.reduceRight
---

{{JSRef}}

**`reduceRight()`** 是 {{jsxref("Array")}} 實例的方法，會將一個函式套用至一個累加器，以及陣列中的每個值（從右至左），來將該陣列縮減為單一值。

另請參閱從左至右的 {{jsxref("Array.prototype.reduce()")}}。

{{InteractiveExample("JavaScript Demo: Array.prototype.reduceRight()")}}

```js interactive-example
const array1 = [
  [0, 1],
  [2, 3],
  [4, 5],
];

const result = array1.reduceRight((accumulator, currentValue) =>
  accumulator.concat(currentValue),
);

console.log(result);
// Expected output: Array [4, 5, 2, 3, 0, 1]
// 預期輸出：陣列 [4, 5, 2, 3, 0, 1]
```

## 語法

```js-nolint
reduceRight(callbackFn)
reduceRight(callbackFn, initialValue)
```

### 參數

- `callbackFn`
  - : 為陣列中每個元素所執行的函式。其回傳值會變成下一次呼叫 `callbackFn` 時 `accumulator` 參數的值。在最後一次呼叫時，回傳值會變成 `reduceRight()` 的回傳值。該函式會使用以下引數呼叫：
    - `accumulator`
      - : 前一次呼叫 `callbackFn` 所產生的值。在第一次呼叫時，如果指定了 `initialValue`，其值為 `initialValue`；否則其值為陣列的最後一個元素。
    - `currentValue`
      - : 目前元素的值。在第一次呼叫時，如果指定了 `initialValue`，其值為最後一個元素；否則其值為倒數第二個元素。
    - `currentIndex`
      - : 陣列中 `currentValue` 的索引位置。在第一次呼叫時，如果指定了 `initialValue`，其值為 `array.length - 1`，否則為 `array.length - 2`。
    - `array`
      - : 呼叫 `reduceRight()` 的陣列。
- `initialValue` {{optional_inline}}
  - : 作為第一次呼叫 `callbackFn` 時累加器的值。如果沒有提供初始值，將會使用陣列中的最後一個元素並跳過。在沒有初始值的情況下，於空陣列上呼叫 `reduceRight()` 會建立一個 `TypeError`。

### 回傳值縮減後產生的值。

## 描述

`reduceRight()` 方法是一種[迭代方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#iterative_methods)。它會依遞減索引順序，在陣列中的所有元素上執行「reducer」回呼函式，並將它們累加成單一值。閱讀[迭代方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#iterative_methods)章節，以取得更多關於這些方法如何運作的訊息。

`callbackFn` 只會針對有指定值的陣列索引呼叫。它不會針對[稀疏陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)中的空插槽呼叫。

與其他[迭代方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#iterative_methods)不同，`reduceRight()` 不接受 `thisArg` 引數。呼叫 `callbackFn` 時，`this` 永遠是 `undefined`，如果 `callbackFn` 不是嚴格模式，則會被替換為 `globalThis`。

`reduceRight()` 方法是[泛用](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)的。它只預期 `this` 值具有 `length` 屬性和整數鍵屬性。

所有在[何時不該使用 reduce()](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce#when_to_not_use_reduce)中討論關於 `reduce` 的注意事項，同樣適用於 `reduceRight`。由於 JavaScript 沒有惰性求值語意，因此 `reduce` 和 `reduceRight` 之間沒有效能差異。

## 範例

### 沒有初始值時 reduceRight() 的運作方式對 reduceRight `callbackFn` 的呼叫看起來會像這樣：

```js
arr.reduceRight((accumulator, currentValue, index, array) => {
  // …
});
```

第一次呼叫函式時，`accumulator` 和 `currentValue` 可以是兩個值之一。如果在呼叫 `reduceRight` 時提供了 `initialValue`，則 `accumulator` 會等於 `initialValue`，而 `currentValue` 會等於陣列中的最後一個值。如果沒有提供 `initialValue`，則 `accumulator` 會等於陣列中的最後一個值，而 `currentValue` 會等於倒數第二個值。

如果陣列是空的且沒有提供 `initialValue`，則會拋出 {{jsxref("TypeError")}}。如果陣列只有一個元素（無論位置為何）且沒有提供 `initialValue`，或者如果提供了 `initialValue` 但陣列是空的，則會傳回單獨的值，而不會呼叫 `callbackFn`。

該函式的一些範例執行如下所示：

```js
[0, 1, 2, 3, 4].reduceRight(
  (accumulator, currentValue, index, array) => accumulator + currentValue,
);
```

回呼會被呼叫四次，每次呼叫的引數和回傳值如下：

|             | `accumulator` | `currentValue` | `index` | 回傳值 |
| ----------- | ------------- | -------------- | ------- | ------------ |
| 第一次呼叫  | `4`           | `3`            | `3`     | `7`          |
| 第二次呼叫 | `7`           | `2`            | `2`     | `9`          |
| 第三次呼叫  | `9`           | `1`            | `1`     | `10`         |
| 第四次呼叫  | `10`          | `0`            | `0`     | `10`         |

`array` 參數在整個過程中永遠不會改變，它永遠是 `[0, 1, 2, 3, 4]`。`reduceRight` 傳回的值會是最後一次回呼呼叫的值（`10`）。

### 使用初始值時 reduceRight() 的運作方式在這裡，我們使用相同的演算法縮減相同的陣列，但將 `10` 的 `initialValue` 作為第二個引數傳遞給 `reduceRight()`：

```js
[0, 1, 2, 3, 4].reduceRight(
  (accumulator, currentValue, index, array) => accumulator + currentValue,
  10,
);
```

|             | `accumulator` | `currentValue` | `index` | 回傳值 |
| ----------- | ------------- | -------------- | ------- | ------------ |
| 第一次呼叫  | `10`          | `4`            | `4`     | `14`         |
| 第二次呼叫 | `14`          | `3`            | `3`     | `17`         |
| 第三次呼叫  | `17`          | `2`            | `2`     | `19`         |
| 第四次呼叫  | `19`          | `1`            | `1`     | `20`         |
| 第五次呼叫  | `20`          | `0`            | `0`     | `20`         |

這次 `reduceRight` 傳回的值當然會是 `20`。

### 加總陣列中的所有值

```js
const sum = [0, 1, 2, 3].reduceRight((a, b) => a + b);
// sum is 6
// sum 為 6
```

### 執行一系列具有序列回呼的非同步函式，每個函式將其結果傳遞給下一個函式

```js
const waterfall =
  (...functions) =>
  (callback, ...args) =>
    functions.reduceRight(
      (composition, fn) =>
        (...results) =>
          fn(composition, ...results),
      callback,
    )(...args);

const randInt = (max) => Math.floor(Math.random() * max);

const add5 = (callback, x) => {
  setTimeout(callback, randInt(1000), x + 5);
};
const mult3 = (callback, x) => {
  setTimeout(callback, randInt(1000), x * 3);
};
const sub2 = (callback, x) => {
  setTimeout(callback, randInt(1000), x - 2);
};
const split = (callback, x) => {
  setTimeout(callback, randInt(1000), x, x);
};
const add = (callback, x, y) => {
  setTimeout(callback, randInt(1000), x + y);
};
const div4 = (callback, x) => {
  setTimeout(callback, randInt(1000), x / 4);
};

const computation = waterfall(add5, mult3, sub2, split, add, div4);
computation(console.log, 5); // Logs 14
// 記錄 14

// same as:
// 等同於：

const computation2 = (input, callback) => {
  const f6 = (x) => div4(callback, x);
  const f5 = (x, y) => add(f6, x, y);
  const f4 = (x) => split(f5, x);
  const f3 = (x) => sub2(f4, x);
  const f2 = (x) => mult3(f3, x);
  add5(f2, input);
};
```

### reduce 與 reduceRight 之間的差異

```js
const a = ["1", "2", "3", "4", "5"];
const left = a.reduce((prev, cur) => prev + cur);
const right = a.reduceRight((prev, cur) => prev + cur);

console.log(left); // "12345"
console.log(right); // "54321"
```

### 定義可組合的函式函式組合是一種組合函式的機制，其中每個函式的輸出會傳遞到下一個函式，而最後一個函式的輸出是最終結果。在這個範例中，我們使用 `reduceRight()` 來實作函式組合。

另請參閱 Wikipedia 上的[函式組合](<https://en.wikipedia.org/wiki/Function_composition_(computer_science)>)。

```js
const compose =
  (...args) =>
  (value) =>
    args.reduceRight((acc, fn) => fn(acc), value);

// Increment passed number
// 遞增傳入的數字
const inc = (n) => n + 1;

// Doubles the passed value
// 將傳入的值加倍
const double = (n) => n * 2;

// using composition function
// 使用組合函式
console.log(compose(double, inc)(2)); // 6

// using composition function
// 使用組合函式
console.log(compose(inc, double)(2)); // 5
```

### 將 reduceRight() 與稀疏陣列搭配使用

`reduceRight()` 會跳過稀疏陣列中遺失的元素，但不會跳過 `undefined` 值。

```js
console.log([1, 2, , 4].reduceRight((a, b) => a + b)); // 7
console.log([1, 2, undefined, 4].reduceRight((a, b) => a + b)); // NaN
```

### 在非陣列物件上呼叫 reduceRight()

`reduceRight()` 方法會讀取 `this` 的 `length` 屬性，然後存取每個鍵為小於 `length` 的非負整數的屬性。

```js
const arrayLike = {
  length: 3,
  0: 2,
  1: 3,
  2: 4,
  3: 99, // ignored by reduceRight() since length is 3
  // 因為長度為 3，所以 reduceRight() 會忽略
};
console.log(Array.prototype.reduceRight.call(arrayLike, (x, y) => x - y));
// -1, which is 4 - 3 - 2
// -1，即 4 - 3 - 2
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`Array.prototype.reduceRight` 在 `core-js` 中的 Polyfill](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.prototype.reduceRight` 的 es-shims polyfill](https://www.npmjs.com/package/array.prototype.reduceright)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections)指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.map()")}}
- {{jsxref("Array.prototype.flat()")}}
- {{jsxref("Array.prototype.flatMap()")}}
- {{jsxref("Array.prototype.reduce()")}}
- {{jsxref("TypedArray.prototype.reduceRight()")}}
- {{jsxref("Object.groupBy()")}}
- {{jsxref("Map.groupBy()")}}
````