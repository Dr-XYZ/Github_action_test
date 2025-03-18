````markdown
---
title: Array.prototype.lastIndexOf()
slug: Web/JavaScript/Reference/Global_Objects/Array/lastIndexOf
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.lastIndexOf
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`lastIndexOf()`** 方法會回傳陣列中指定元素最後一次出現的索引，若陣列中沒有此元素則回傳 -1。此陣列會從 `fromIndex` 開始**反向**搜尋。

{{InteractiveExample("JavaScript Demo: Array.prototype.lastIndexOf()")}}

```js interactive-example
const animals = ["Dodo", "Tiger", "Penguin", "Dodo"];

console.log(animals.lastIndexOf("Dodo"));
// Expected output: 3

console.log(animals.lastIndexOf("Tiger"));
// Expected output: 1
```

## 形式語法

```js-nolint
lastIndexOf(searchElement)
lastIndexOf(searchElement, fromIndex)
```

### 參數

- `searchElement`
  - : 欲在此陣列中尋找的元素。
- `fromIndex` {{optional_inline}}
  - : 從此索引開始**反向**搜尋，從 0 開始。會[轉換成整數](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Number#integer_conversion)。
    - 負數索引會從陣列的尾端開始倒數——若 `-array.length <= fromIndex < 0`，則會使用 `fromIndex + array.length`。
    - 若 `fromIndex < -array.length`，則不會搜尋此陣列，並回傳 `-1`。你可以將它想像成從陣列開頭前不存在的位置開始，然後從那裡往後退。路徑上沒有陣列元素，因此永遠找不到 `searchElement`。
    - 若 `fromIndex >= array.length` 或省略 `fromIndex`，則會使用 `array.length - 1`，這會導致搜尋整個陣列。你可以將它想像成從陣列結尾後不存在的位置開始，然後從那裡往後退。它最終會到達陣列的真實結尾位置，此時它會開始反向搜尋實際的陣列元素。

### 回傳值

陣列中 `searchElement` 最後一次出現的索引；若找不到則回傳 `-1`。

## 描述

`lastIndexOf()` 方法使用[嚴格相等](/zh-TW/docs/Web/JavaScript/Reference/Operators/Strict_equality)比較 `searchElement` 與陣列的元素（與 `===` 運算子使用的演算法相同）。[`NaN`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/NaN) 值永遠不會被視為相等，因此當 `searchElement` 為 `NaN` 時，`lastIndexOf()` 永遠會回傳 `-1`。

`lastIndexOf()` 方法會跳過[稀疏陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)中的空插槽。

`lastIndexOf()` 方法是[泛用的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它只要求 `this` 值具有 `length` 屬性以及整數鍵屬性。

## 範例

### 使用 lastIndexOf()

以下範例使用 `lastIndexOf()` 來尋找陣列中的值。

```js
const numbers = [2, 5, 9, 2];
numbers.lastIndexOf(2); // 3
numbers.lastIndexOf(7); // -1
numbers.lastIndexOf(2, 3); // 3
numbers.lastIndexOf(2, 2); // 0
numbers.lastIndexOf(2, -2); // 0
numbers.lastIndexOf(2, -1); // 3
```

你不能使用 `lastIndexOf()` 搜尋 `NaN`。

```js
const array = [NaN];
array.lastIndexOf(NaN); // -1
```

### 找出元素的所有出現位置

以下範例使用 `lastIndexOf` 來找出指定陣列中元素的所有索引，並使用 {{jsxref("Array/push", "push()")}} 將它們加到另一個陣列中。

```js
const indices = [];
const array = ["a", "b", "a", "c", "a", "d"];
const element = "a";
let idx = array.lastIndexOf(element);
while (idx !== -1) {
  indices.push(idx);
  idx = idx > 0 ? array.lastIndexOf(element, idx - 1) : -1;
}

console.log(indices);
// [4, 2, 0]
```

請注意，我們必須在此處單獨處理 `idx === 0` 的情況，因為如果元素是陣列的第一個元素，則無論 `fromIndex` 參數為何，都會找到該元素。這與 {{jsxref("Array/indexOf", "indexOf()")}} 方法不同。

### 在稀疏陣列上使用 lastIndexOf()

你無法使用 `lastIndexOf()` 搜尋稀疏陣列中的空插槽。

```js
console.log([1, , 3].lastIndexOf(undefined)); // -1
```

### 在非陣列物件上呼叫 lastIndexOf()

`lastIndexOf()` 方法會讀取 `this` 的 `length` 屬性，然後存取每個鍵為小於 `length` 的非負整數的屬性。

```js
const arrayLike = {
  length: 3,
  0: 2,
  1: 3,
  2: 2,
  3: 5, // lastIndexOf() 會忽略，因為 length 為 3
};
console.log(Array.prototype.lastIndexOf.call(arrayLike, 2));
// 2
console.log(Array.prototype.lastIndexOf.call(arrayLike, 5));
// -1
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`core-js` 中 `Array.prototype.lastIndexOf` 的 Polyfill](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.prototype.lastIndexOf` 的 es-shims Polyfill](https://www.npmjs.com/package/array.prototype.lastindexof)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections)教學
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.findIndex()")}}
- {{jsxref("Array.prototype.findLastIndex()")}}
- {{jsxref("Array.prototype.indexOf()")}}
- {{jsxref("TypedArray.prototype.lastIndexOf()")}}
- {{jsxref("String.prototype.lastIndexOf()")}}
````