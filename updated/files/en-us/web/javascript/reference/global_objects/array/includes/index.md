````markdown
---
title: Array.prototype.includes()
slug: Web/JavaScript/Reference/Global_Objects/Array/includes
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.includes
---

{{JSRef}}

**`includes()`** 是 {{jsxref("Array")}} 實例的方法，用來判斷陣列是否在其條目中包含某個值，並據此回傳 `true` 或 `false`。

{{InteractiveExample("JavaScript Demo: Array.prototype.includes()")}}

```js interactive-example
const array1 = [1, 2, 3];

console.log(array1.includes(2));
// Expected output: true

const pets = ["cat", "dog", "bat"];

console.log(pets.includes("cat"));
// Expected output: true

console.log(pets.includes("at"));
// Expected output: false
```

## 形式語法

```js-nolint
includes(searchElement)
includes(searchElement, fromIndex)
```

### 參數

- `searchElement`
  - : 要搜尋的值。
- `fromIndex` {{optional_inline}}
  - : 從此處開始搜尋的從零開始的索引，[轉換為整數](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Number#integer_conversion)。
    - 負索引從陣列末尾開始倒數 — 如果 `-array.length <= fromIndex < 0`，則使用 `fromIndex + array.length`。 然而，在這種情況下，陣列仍然從前往後搜尋。
    - 如果 `fromIndex < -array.length` 或省略 `fromIndex`，則使用 `0`，導致搜尋整個陣列。
    - 如果 `fromIndex >= array.length`，則不會搜尋陣列，並回傳 `false`。

### 回傳值

如果值 `searchElement` 在陣列中（或在索引 `fromIndex` 指示的陣列部分中，如果已指定）找到，則布林值為 `true`。

## 描述

`includes()` 方法使用 [SameValueZero](/zh-TW/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness#same-value-zero_equality) 演算法比較 `searchElement` 與陣列的元素。數值 0 都被認為是相等的，無論符號如何（也就是說，`-0` 等於 `0`），但 `false` _不_ 被認為與 `0` 相同。 可以正確地搜尋 [`NaN`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/NaN)。

當用於[稀疏陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)時，`includes()` 方法會將空插槽視為具有值 `undefined` 來進行迭代。

`includes()` 方法是[泛型的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。 它只需要 `this` 值具有 `length` 屬性和整數鍵屬性。

## 範例

### 使用 includes()

```js
[1, 2, 3].includes(2); // true
[1, 2, 3].includes(4); // false
[1, 2, 3].includes(3, 3); // false
[1, 2, 3].includes(3, -1); // true
[1, 2, NaN].includes(NaN); // true
["1", "2", "3"].includes(3); // false
```

### fromIndex 大於或等於陣列長度

如果 `fromIndex` 大於或等於陣列的長度，則會回傳 `false`。將不會搜尋陣列。

```js
const arr = ["a", "b", "c"];

arr.includes("c", 3); // false
arr.includes("c", 100); // false
```

### 計算索引小於 0

如果 `fromIndex` 是負數，則計算索引以用作陣列中的位置，從該位置開始搜尋 `searchElement`。如果計算索引小於或等於 `0`，則會搜尋整個陣列。

```js
// array length is 3
// fromIndex is -100
// computed index is 3 + (-100) = -97

const arr = ["a", "b", "c"];

arr.includes("a", -100); // true
arr.includes("b", -100); // true
arr.includes("c", -100); // true
arr.includes("a", -2); // false
```

### 在稀疏陣列上使用 includes()

你可以在稀疏陣列中搜尋 `undefined` 並取得 `true`。

```js
console.log([1, , 3].includes(undefined)); // true
```

### 在非陣列物件上呼叫 includes()

`includes()` 方法會讀取 `this` 的 `length` 屬性，然後存取每個鍵是非負整數且小於 `length` 的屬性。

```js
const arrayLike = {
  length: 3,
  0: 2,
  1: 3,
  2: 4,
  3: 1, // ignored by includes() since length is 3
};
console.log(Array.prototype.includes.call(arrayLike, 2));
// true
console.log(Array.prototype.includes.call(arrayLike, 1));
// false
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`core-js` 中 `Array.prototype.includes` 的 Polyfill](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.prototype.includes` 的 es-shims polyfill](https://www.npmjs.com/package/array-includes)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.indexOf()")}}
- {{jsxref("Array.prototype.find()")}}
- {{jsxref("Array.prototype.findIndex()")}}
- {{jsxref("TypedArray.prototype.includes()")}}
- {{jsxref("String.prototype.includes()")}}
````