````markdown
---
title: Array.prototype.indexOf()
slug: Web/JavaScript/Reference/Global_Objects/Array/indexOf
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.indexOf
---

{{JSRef}}

**`indexOf()`** 是 {{jsxref("Array")}} 實例的方法，會回傳陣列中可以找到給定元素的**第一個**索引，如果陣列中沒有此元素，則回傳 -1。

{{InteractiveExample("JavaScript Demo: Array.prototype.indexOf()")}}

```js interactive-example
const beasts = ["ant", "bison", "camel", "duck", "bison"];

console.log(beasts.indexOf("bison"));
// Expected output: 1

// Start from index 2
console.log(beasts.indexOf("bison", 2));
// Expected output: 4

console.log(beasts.indexOf("giraffe"));
// Expected output: -1
```

## 形式語法

```js-nolint
indexOf(searchElement)
indexOf(searchElement, fromIndex)
```

### 參數

- `searchElement`
  - : 要在陣列中尋找的元素。
- `fromIndex` {{optional_inline}}
  - : 從零開始的索引，表示從此處開始搜尋，會[轉換為整數](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Number#integer_conversion)。
    - 負數索引會從陣列的結尾開始倒數——如果 `-array.length <= fromIndex < 0`，則會使用 `fromIndex + array.length`。請注意，在這種情況下，陣列仍然會從前往後搜尋。
    - 如果 `fromIndex < -array.length` 或省略 `fromIndex`，則會使用 `0`，導致搜尋整個陣列。
    - 如果 `fromIndex >= array.length`，則不會搜尋陣列，並回傳 `-1`。

### 回傳值

陣列中 `searchElement` 的第一個索引；如果找不到，則為 `-1`。

## 描述

`indexOf()` 方法使用[嚴格相等](/zh-TW/docs/Web/JavaScript/Reference/Operators/Strict_equality)（與 `===` 運算子使用的演算法相同）比較 `searchElement` 與陣列的元素。[`NaN`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/NaN) 值永遠不會被視為相等，因此當 `searchElement` 為 `NaN` 時，`indexOf()` 總是回傳 `-1`。

`indexOf()` 方法會跳過[稀疏陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)中的空插槽。

`indexOf()` 方法是[泛用的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它只要求 `this` 值具有 `length` 屬性及整數鍵屬性。

## 範例

### 使用 indexOf()

以下範例使用 `indexOf()` 來尋找陣列中的值。

```js
const array = [2, 9, 9];
array.indexOf(2); // 0
array.indexOf(7); // -1
array.indexOf(9, 2); // 2
array.indexOf(2, -1); // -1
array.indexOf(2, -3); // 0
```

你不能使用 `indexOf()` 來搜尋 `NaN`。

```js
const array = [NaN];
array.indexOf(NaN); // -1
```

### 尋找元素的所有出現位置

```js
const indices = [];
const array = ["a", "b", "a", "c", "a", "d"];
const element = "a";
let idx = array.indexOf(element);
while (idx !== -1) {
  indices.push(idx);
  idx = array.indexOf(element, idx + 1);
}
console.log(indices);
// [0, 2, 4]
```

### 尋找陣列中是否存在元素並更新陣列

```js
function updateVegetablesCollection(veggies, veggie) {
  if (veggies.indexOf(veggie) === -1) {
    veggies.push(veggie);
    console.log(`New veggies collection is: ${veggies}`);
  } else {
    console.log(`${veggie} already exists in the veggies collection.`);
  }
}

const veggies = ["potato", "tomato", "chillies", "green-pepper"];

updateVegetablesCollection(veggies, "spinach");
// New veggies collection is: potato,tomato,chillies,green-pepper,spinach
updateVegetablesCollection(veggies, "spinach");
// spinach already exists in the veggies collection.
```

### 在稀疏陣列上使用 indexOf()

你不能使用 `indexOf()` 來搜尋稀疏陣列中的空插槽。

```js
console.log([1, , 3].indexOf(undefined)); // -1
```

### 在非陣列物件上呼叫 indexOf()

`indexOf()` 方法會讀取 `this` 的 `length` 屬性，然後存取每個鍵為小於 `length` 的非負整數的屬性。

```js
const arrayLike = {
  length: 3,
  0: 2,
  1: 3,
  2: 4,
  3: 5, // ignored by indexOf() since length is 3
};
console.log(Array.prototype.indexOf.call(arrayLike, 2));
// 0
console.log(Array.prototype.indexOf.call(arrayLike, 5));
// -1
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`core-js` 中 `Array.prototype.indexOf` 的 Polyfill](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.prototype.indexOf` 的 es-shims polyfill](https://www.npmjs.com/package/array.prototype.indexof)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections)指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.findIndex()")}}
- {{jsxref("Array.prototype.findLastIndex()")}}
- {{jsxref("Array.prototype.lastIndexOf()")}}
- {{jsxref("TypedArray.prototype.indexOf()")}}
- {{jsxref("String.prototype.indexOf()")}}
````