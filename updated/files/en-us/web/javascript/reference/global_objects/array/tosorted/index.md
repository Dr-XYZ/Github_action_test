````markdown
---
title: Array.prototype.toSorted()
slug: Web/JavaScript/Reference/Global_Objects/Array/toSorted
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.toSorted
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`toSorted()`** 方法是 {{jsxref("Array/sort", "sort()")}} 方法的[複製](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array#copying_methods_and_mutating_methods)版本。它會回傳一個新的陣列，其元素會以遞增排序。

## 語法

```js-nolint
toSorted()
toSorted(compareFn)
```

### 參數

- `compareFn` {{optional_inline}}
  - : 一個決定元素順序的函式。如果省略，陣列元素會被轉換為字串，然後根據每個字元的 Unicode 碼位值進行排序。參見 {{jsxref("Array/sort", "sort()")}} 以取得更多訊息。

### 回傳值

一個新的陣列，其元素會以遞增排序。

## 描述

參見 {{jsxref("Array/sort", "sort()")}} 以取得更多關於 `compareFn` 參數的訊息。

當用於[稀疏陣列](/en-US/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)時，`toSorted()` 方法會迭代空插槽，如同它們具有 `undefined` 值一樣。

`toSorted()` 方法是[泛用](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)的。它只期望 `this` 值具有 `length` 屬性和整數鍵屬性。

## 範例

### 排序陣列

```js
const months = ["Mar", "Jan", "Feb", "Dec"];
const sortedMonths = months.toSorted();
console.log(sortedMonths); // ['Dec', 'Feb', 'Jan', 'Mar']
console.log(months); // ['Mar', 'Jan', 'Feb', 'Dec']

const values = [1, 10, 21, 2];
const sortedValues = values.toSorted((a, b) => a - b);
console.log(sortedValues); // [1, 2, 10, 21]
console.log(values); // [1, 10, 21, 2]
```

如需更多使用範例，參見 {{jsxref("Array/sort", "sort()")}}。

### 在稀疏陣列上使用 toSorted()

空插槽會被排序，如同它們具有 `undefined` 值一樣。它們總是會被排序到陣列的末尾，並且不會為它們呼叫 `compareFn`。

```js
console.log(["a", "c", , "b"].toSorted()); // ['a', 'b', 'c', undefined]
console.log([, undefined, "a", "b"].toSorted()); // ["a", "b", undefined, undefined]
```

### 在非陣列物件上呼叫 toSorted()

`toSorted()` 方法會讀取 `this` 的 `length` 屬性。然後，它會收集 `0` 到 `length - 1` 範圍內的所有現有整數鍵屬性，對它們進行排序，並將它們寫入一個新的陣列。

```js
const arrayLike = {
  length: 3,
  unrelated: "foo",
  0: 5,
  2: 4,
  3: 3, // toSorted() 忽略，因為 length 為 3
};
console.log(Array.prototype.toSorted.call(arrayLike));
// [4, 5, undefined]
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`core-js` 中 `Array.prototype.toSorted` 的 Polyfill](https://github.com/zloirock/core-js#change-array-by-copy)
- [`Array.prototype.toSorted` 的 es-shims Polyfill](https://www.npmjs.com/package/array.prototype.tosorted)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array.prototype.sort()")}}
- {{jsxref("Array.prototype.toReversed()")}}
- {{jsxref("Array.prototype.toSpliced()")}}
- {{jsxref("Array.prototype.with()")}}
- {{jsxref("TypedArray.prototype.toSorted()")}}
````