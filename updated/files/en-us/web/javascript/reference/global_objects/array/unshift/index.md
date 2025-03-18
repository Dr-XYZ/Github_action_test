````markdown
---
title: Array.prototype.unshift()
slug: Web/JavaScript/Reference/Global_Objects/Array/unshift
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.unshift
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`unshift()`** 方法會將指定的元素新增到陣列的開頭，並回傳陣列的新長度。

{{InteractiveExample("JavaScript Demo: Array.prototype.unshift()")}}

```js interactive-example
const array1 = [1, 2, 3];

console.log(array1.unshift(4, 5));
// Expected output: 5

console.log(array1);
// Expected output: Array [4, 5, 1, 2, 3]
```

## 語法

```js-nolint
unshift()
unshift(element1)
unshift(element1, element2)
unshift(element1, element2, /* …, */ elementN)
```

### 參數

- `element1`, …, `elementN`
  - : 要加到 `arr` 最前面的元素。

### 回傳值

呼叫此方法的物件之新的 {{jsxref("Array/length", "length")}} 屬性。

## 描述

`unshift()` 方法會將給定的值插入到類陣列物件的開頭。

{{jsxref("Array.prototype.push()")}} 的行為與 `unshift()` 類似，但作用於陣列的結尾。

請注意，如果傳遞多個元素作為參數，它們會以區塊的形式插入到物件的開頭，順序與傳遞參數的順序完全相同。因此，**一次**呼叫帶有 `n` 個引數的 `unshift()`，或**用 1 個**引數呼叫 `n` 次（例如用迴圈），不會產生相同的結果。

參見範例：

```js
let arr = [4, 5, 6];

arr.unshift(1, 2, 3);
console.log(arr);
// [1, 2, 3, 4, 5, 6]

arr = [4, 5, 6]; // 重設陣列

arr.unshift(1);
arr.unshift(2);
arr.unshift(3);

console.log(arr);
// [3, 2, 1, 4, 5, 6]
```

`unshift()` 方法是[泛用的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它只要求 `this` 值具有 `length` 屬性和整數鍵屬性。雖然字串也是類陣列，但此方法不適合應用於字串，因為字串是不可變的。

## 範例

### 使用 unshift()

```js
const arr = [1, 2];

arr.unshift(0); // 呼叫的結果是 3，也就是新的陣列長度
// arr is [0, 1, 2]

arr.unshift(-2, -1); // 新的陣列長度是 5
// arr is [-2, -1, 0, 1, 2]

arr.unshift([-4, -3]); // 新的陣列長度是 6
// arr is [[-4, -3], -2, -1, 0, 1, 2]

arr.unshift([-7, -6], [-5]); // 新的陣列長度是 8
// arr is [ [-7, -6], [-5], [-4, -3], -2, -1, 0, 1, 2 ]
```

### 在非陣列物件上呼叫 unshift()

`unshift()` 方法會讀取 `this` 的 `length` 屬性。它會將 `0` 到 `length - 1` 範圍內的所有索引向右移動引數的數量（將它們的值增加此數字）。然後，它會從 `0` 開始，將每個索引設定為傳遞給 `unshift()` 的引數。最後，它會將 `length` 設定為先前的長度加上前置元素的數量。

```js
const arrayLike = {
  length: 3,
  unrelated: "foo",
  2: 4,
};
Array.prototype.unshift.call(arrayLike, 1, 2);
console.log(arrayLike);
// { '0': 1, '1': 2, '4': 4, length: 5, unrelated: 'foo' }

const plainObj = {};
// 沒有 length 屬性，所以長度為 0
Array.prototype.unshift.call(plainObj, 1, 2);
console.log(plainObj);
// { '0': 1, '1': 2, length: 2 }
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`core-js` 中 `Array.prototype.unshift` 的 Polyfill，並修正了此方法](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.prototype.unshift` 的 es-shims Polyfill](https://www.npmjs.com/package/array.prototype.unshift)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.push()")}}
- {{jsxref("Array.prototype.pop()")}}
- {{jsxref("Array.prototype.shift()")}}
- {{jsxref("Array.prototype.concat()")}}
- {{jsxref("Array.prototype.splice()")}}
````