````markdown
---
title: Array.prototype.toSpliced()
slug: Web/JavaScript/Reference/Global_Objects/Array/toSpliced
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.toSpliced
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`toSpliced()`** 方法是 {{jsxref("Array/splice", "splice()")}} 方法的[複製](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array#copying_methods_and_mutating_methods)版本。它會回傳一個新的陣列，其中一些元素在給定的索引處被移除和／或替換。

## 形式語法

```js-nolint
toSpliced(start)
toSpliced(start, deleteCount)
toSpliced(start, deleteCount, item1)
toSpliced(start, deleteCount, item1, item2)
toSpliced(start, deleteCount, item1, item2, /* …, */ itemN)
```

### 參數

- `start`

  - : 從 0 開始的索引，表示從此處開始變更陣列，[轉換為整數](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number#integer_conversion)。
    - 負數索引從陣列的結尾倒數——如果 `-array.length <= start < 0`，則使用 `start + array.length`。
    - 如果 `start < -array.length` 或省略 `start`，則使用 `0`。
    - 如果 `start >= array.length`，則不會刪除任何元素，但此方法將如同新增函式一樣運作，新增提供的所有元素。

- `deleteCount` {{optional_inline}}

  - : 一個整數，表示要從 `start` 移除的陣列元素數量。

    如果省略 `deleteCount`，或者其值大於或等於 `start` 指定位置之後的元素數量，則會刪除從 `start` 到陣列結尾的所有元素。但是，如果你希望傳遞任何 `itemN` 參數，則應傳遞 `Infinity` 作為 `deleteCount` 以刪除 `start` 之後的所有元素，因為明確的 `undefined` 會[轉換](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number#integer_conversion)為 `0`。

    如果 `deleteCount` 為 `0` 或負數，則不會移除任何元素。在這種情況下，你應該指定至少一個新元素（參見下方）。

- `item1`，…，`itemN` {{optional_inline}}

  - : 要新增到陣列的元素，從 `start` 開始。

    如果你未指定任何元素，則 `toSpliced()` 將僅從陣列中移除元素。

### 回傳值

一個新的陣列，包含 `start` 之前的所有元素、`item1`、`item2`、…、`itemN`，以及 `start + deleteCount` 之後的所有元素。

## 描述

`toSpliced()` 方法與 `splice()` 類似，可以一次執行多個操作：它會從陣列中移除給定數量的元素（從給定索引開始），然後在相同索引處插入給定的元素。但是，它會回傳一個新的陣列，而不是修改原始陣列。因此，刪除的元素不會由此方法回傳。

`toSpliced()` 方法永遠不會產生[稀疏陣列](/en-US/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)。如果來源陣列是稀疏的，則新的陣列中的空白插槽將被替換為 `undefined`。

`toSpliced()` 方法是[泛用的](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它僅期望 `this` 值具有 `length` 屬性和整數鍵屬性。

## 範例

### 刪除、新增和替換元素

你可以使用 `toSpliced()` 來刪除、新增和替換陣列中的元素，並建立一個新的陣列，這比使用 `slice()` 和 `concat()` 更有效率。

```js
const months = ["Jan", "Mar", "Apr", "May"];

// 在索引 1 處插入一個元素
const months2 = months.toSpliced(1, 0, "Feb");
console.log(months2); // ["Jan", "Feb", "Mar", "Apr", "May"]

// 從索引 2 開始刪除兩個元素
const months3 = months2.toSpliced(2, 2);
console.log(months3); // ["Jan", "Feb", "May"]

// 將索引 1 處的一個元素替換為兩個新元素
const months4 = months3.toSpliced(1, 1, "Feb", "Mar");
console.log(months4); // ["Jan", "Feb", "Mar", "May"]

// 原始陣列未被修改
console.log(months); // ["Jan", "Mar", "Apr", "May"]
```

### 在稀疏陣列上使用 toSpliced()

`toSpliced()` 方法總是建立一個密集陣列。

```js
const arr = [1, , 3, 4, , 6];
console.log(arr.toSpliced(1, 2)); // [1, 4, undefined, 6]
```

### 在非陣列物件上呼叫 toSpliced()

`toSpliced()` 方法會讀取 `this` 的 `length` 屬性。然後，它會讀取所需的整數鍵屬性，並將它們寫入新的陣列中。

```js
const arrayLike = {
  length: 3,
  unrelated: "foo",
  0: 5,
  2: 4,
};
console.log(Array.prototype.toSpliced.call(arrayLike, 0, 1, 2, 3));
// [2, 3, undefined, 4]
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`Array.prototype.toSpliced` 的 Polyfill，位於 `core-js`](https://github.com/zloirock/core-js#change-array-by-copy)
- [`Array.prototype.toSpliced` 的 es-shims Polyfill](https://www.npmjs.com/package/array.prototype.tospliced)
- {{jsxref("Array.prototype.splice()")}}
- {{jsxref("Array.prototype.toReversed()")}}
- {{jsxref("Array.prototype.toSorted()")}}
- {{jsxref("Array.prototype.with()")}}
````