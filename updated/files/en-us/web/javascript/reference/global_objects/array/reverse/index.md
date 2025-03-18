````markdown
---
title: Array.prototype.reverse()
slug: Web/JavaScript/Reference/Global_Objects/Array/reverse
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.reverse
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`reverse()`** 方法會將陣列原地反轉（_[in place](https://en.wikipedia.org/wiki/In-place_algorithm)_），並回傳對同個陣列的參照。陣列的第一個元素會變成最後一個，而最後一個陣列元素則會變成第一個。換句話說，陣列中的元素順序將會變成與先前指定的方向相反。

若要反轉陣列中的元素，但不更動原始陣列，請使用 {{jsxref("Array/toReversed", "toReversed()")}}。

{{InteractiveExample("JavaScript Demo: Array.prototype.reverse()")}}

```js interactive-example
const array1 = ["one", "two", "three"];
console.log("array1:", array1);
// Expected output: "array1:" Array ["one", "two", "three"]

const reversed = array1.reverse();
console.log("reversed:", reversed);
// Expected output: "reversed:" Array ["three", "two", "one"]

// Careful: reverse is destructive -- it changes the original array.
console.log("array1:", array1);
// Expected output: "array1:" Array ["three", "two", "one"]
```

## 形式語法

```js-nolint
reverse()
```

### 參數

無。

### 回傳值

回傳已反轉的原始陣列的參照。請注意，陣列是原地（_[in place](https://en.wikipedia.org/wiki/In-place_algorithm)_）反轉的，而且不會建立副本。

## 描述

`reverse()` 方法會將呼叫陣列物件的元素原地轉置，更動陣列，並回傳對該陣列的參照。

`reverse()` 方法會保留空插槽。如果來源陣列是[稀疏陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)，則空插槽對應的新索引會[被刪除](/zh-TW/docs/Web/JavaScript/Reference/Operators/delete)，並且也會變成空插槽。

`reverse()` 方法是[泛用的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它只預期 `this` 值具有 `length` 屬性和整數鍵屬性。雖然字串也類似陣列，但此方法不適合應用於字串，因為字串是不可變的。

## 範例

### 反轉陣列中的元素

以下範例會建立一個包含三個元素的陣列 `items`，然後反轉該陣列。呼叫 `reverse()` 會回傳對已反轉陣列 `items` 的參照。

```js
const items = [1, 2, 3];
console.log(items); // [1, 2, 3]

items.reverse();
console.log(items); // [3, 2, 1]
```

### `reverse()` 方法會回傳對同個陣列的參照

`reverse()` 方法會回傳對原始陣列的參照，因此更動回傳的陣列也會更動原始陣列。

```js
const numbers = [3, 2, 4, 1, 5];
const reversed = numbers.reverse();
// numbers 和 reversed 現在都以反轉的順序排列 [5, 1, 4, 2, 3]
reversed[0] = 5;
console.log(numbers[0]); // 5
```

如果你希望 `reverse()` 不要更動原始陣列，而是像其他陣列方法（例如 [`map()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/map)）一樣回傳一個[淺複製](/zh-TW/docs/Glossary/Shallow_copy)的陣列，請使用 {{jsxref("Array/toReversed", "toReversed()")}} 方法。或者，你可以在呼叫 `reverse()` 之前進行淺複製，使用[展開語法](/zh-TW/docs/Web/JavaScript/Reference/Operators/Spread_syntax)或 [`Array.from()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/from)。

```js
const numbers = [3, 2, 4, 1, 5];
// [...numbers] 會建立一個淺複製，因此 reverse() 不會更動原始陣列
const reverted = [...numbers].reverse();
reverted[0] = 5;
console.log(numbers[0]); // 3
```

### 在稀疏陣列上使用 `reverse()`

在呼叫 `reverse()` 之後，稀疏陣列仍然是稀疏的。空插槽會複製到它們各自的新索引作為空插槽。

```js
console.log([1, , 3].reverse()); // [3, empty, 1]
console.log([1, , 3, 4].reverse()); // [4, 3, empty, 1]
```

### 在非陣列物件上呼叫 `reverse()`

`reverse()` 方法會讀取 `this` 的 `length` 屬性。然後，它會走訪每個介於 `0` 和 `length / 2` 之間的整數鍵屬性，並交換兩端的對應索引，[刪除](/zh-TW/docs/Web/JavaScript/Reference/Operators/delete)來源屬性不存在的任何目標屬性。

```js
const arrayLike = {
  length: 3,
  unrelated: "foo",
  2: 4,
  3: 33, // reverse() 會忽略，因為 length 為 3
};
console.log(Array.prototype.reverse.call(arrayLike));
// { 0: 4, 3: 33, length: 3, unrelated: 'foo' }
// 索引 2 會被刪除，因為原本沒有索引 0
// 索引 3 不會變更，因為長度為 3
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`core-js` 中 `Array.prototype.reverse` 的 Polyfill](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.prototype.reverse` 的 es-shims Polyfill](https://www.npmjs.com/package/array.prototype.reverse)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections)指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.join()")}}
- {{jsxref("Array.prototype.sort()")}}
- {{jsxref("Array.prototype.toReversed()")}}
- {{jsxref("TypedArray.prototype.reverse()")}}
````
