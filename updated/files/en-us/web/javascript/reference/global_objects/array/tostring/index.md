````
---
title: Array.prototype.toString()
slug: Web/JavaScript/Reference/Global_Objects/Array/toString
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.toString
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`toString()`** 方法會回傳一個字串，表示指定的陣列及其元素。

{{InteractiveExample("JavaScript Demo: Array.prototype.toString()", "shorter")}}

```js interactive-example
const array1 = [1, 2, "a", "1a"];

console.log(array1.toString());
// Expected output: "1,2,a,1a"
// 預期輸出：「1,2,a,1a」
```

## 形式語法

```js-nolint
toString()
```

### 參數

無。

### 回傳值

一個字串，表示陣列的元素。

## 描述

{{jsxref("Array")}} 物件會覆寫 {{jsxref("Object")}} 的 `toString` 方法。陣列的 `toString` 方法會在內部呼叫 [`join()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/join)，這會合併陣列並回傳一個字串，其中包含每個以逗號分隔的陣列元素。如果 `join` 方法不可用或不是函式，則會改用 [`Object.prototype.toString`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Object/toString)，並回傳 `[object Array]`。

```js
const arr = [];
arr.join = 1; // re-assign `join` with a non-function
// 使用非函式重新賦值 `join`
console.log(arr.toString()); // [object Array]

console.log(Array.prototype.toString.call({ join: () => 1 })); // 1
```

當陣列要表示為文字值或在字串串接中引用陣列時，JavaScript 會自動呼叫 `toString` 方法。

`Array.prototype.toString` 會以遞迴方式將每個元素（包括其他陣列）轉換為字串。由於 `Array.prototype.toString` 回傳的字串沒有分隔符，因此巢狀陣列看起來像是被扁平化。

```js
const matrix = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9],
];

console.log(matrix.toString()); // 1,2,3,4,5,6,7,8,9
```

當陣列是循環的（包含本身就是元素的元素）時，瀏覽器會忽略循環引用，以避免無限遞迴。

```js
const arr = [];
arr.push(1, [3, arr, 4], 2);
console.log(arr.toString()); // 1,3,,4,2
```

## 範例

### 使用 toString()

```js
const array1 = [1, 2, "a", "1a"];

console.log(array1.toString()); // "1,2,a,1a"
```

### 在稀疏陣列上使用 toString()

依照 `join()` 的行為，`toString()` 會將空插槽視為與 `undefined` 相同，並產生額外的分隔符：

```js
console.log([1, , 3].toString()); // '1,,3'
```

### 在非陣列物件上呼叫 toString()

`toString()` 是[泛用的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它期望 `this` 具有 `join()` 方法；如果沒有，則改用 `Object.prototype.toString()`。

```js
console.log(Array.prototype.toString.call({ join: () => 1 }));
// 1; a number
// 1；數字
console.log(Array.prototype.toString.call({ join: () => undefined }));
// undefined
console.log(Array.prototype.toString.call({ join: "not function" }));
// "[object Object]"
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.join()")}}
- {{jsxref("Array.prototype.toLocaleString()")}}
- {{jsxref("TypedArray.prototype.toString()")}}
- {{jsxref("String.prototype.toString()")}}
````