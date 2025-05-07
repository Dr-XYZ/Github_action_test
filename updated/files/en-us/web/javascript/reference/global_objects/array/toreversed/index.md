````markdown
---
title: Array.prototype.toReversed()
slug: Web/JavaScript/Reference/Global_Objects/Array/toReversed
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.toReversed
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`toReversed()`** 方法是 {{jsxref("Array/reverse", "reverse()")}} 方法的[複製](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array#copying_methods_and_mutating_methods)對應方法。它會回傳一個新的陣列，其元素為反向排序。

## 語法

```js-nolint
toReversed()
```

### 參數無。

### 回傳值一個新的陣列，其元素為反向排序。

## 描述

`toReversed()` 方法會以反向順序轉置呼叫陣列物件的元素，並回傳一個新的陣列。

當用於[稀疏陣列](/en-US/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)時，`toReversed()` 方法會迭代空插槽，如同它們具有 `undefined` 值。

`toReversed()` 方法是[泛型](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它僅期望 `this` 值具有 `length` 屬性和整數鍵屬性。

## 範例

### 反轉陣列中的元素以下範例建立一個包含三個元素的陣列 `items`，然後建立一個新的陣列，它是 `items` 的反向陣列。`items` 陣列保持不變。

```js
const items = [1, 2, 3];
console.log(items); // [1, 2, 3]

const reversedItems = items.toReversed();
console.log(reversedItems); // [3, 2, 1]
console.log(items); // [1, 2, 3]
```

### 在稀疏陣列上使用 toReversed()

`toReversed()` 的回傳值永遠不會是稀疏的。空插槽在回傳的陣列中會變成 `undefined`。

```js
console.log([1, , 3].toReversed()); // [3, undefined, 1]
console.log([1, , 3, 4].toReversed()); // [4, 3, undefined, 1]
```

### 在非陣列物件上呼叫 toReversed()

`toReversed()` 方法會讀取 `this` 的 `length` 屬性。然後，它會以降序方式走訪每個具有介於 `length - 1` 和 `0` 之間的整數鍵的屬性，並將目前屬性的值新增至要回傳的陣列末尾。

```js
const arrayLike = {
  length: 3,
  unrelated: "foo",
  2: 4,
};
console.log(Array.prototype.toReversed.call(arrayLike));
// [4, undefined, undefined]
// '0' 和 '1' 索引不存在，因此它們變成 undefined
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`Array.prototype.toReversed` 的 Polyfill 於 `core-js`](https://github.com/zloirock/core-js#change-array-by-copy)
- [`Array.prototype.toReversed` 的 es-shims polyfill](https://www.npmjs.com/package/array.prototype.toreversed)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections)指南
- {{jsxref("Array.prototype.reverse()")}}
- {{jsxref("Array.prototype.toSorted()")}}
- {{jsxref("Array.prototype.toSpliced()")}}
- {{jsxref("Array.prototype.with()")}}
- {{jsxref("TypedArray.prototype.toReversed()")}}
````