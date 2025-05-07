````markdown
---
title: Array.prototype.with()
slug: Web/JavaScript/Reference/Global_Objects/Array/with
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.with
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`with()`** 方法是使用[中括號表示法](/en-US/docs/Web/JavaScript/Reference/Operators/Property_accessors#bracket_notation)變更指定索引值的[複製](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array#copying_methods_and_mutating_methods)版本。它會回傳一個新陣列，並將指定索引上的元素替換為給定的值。

## 語法

```js-nolint
arrayInstance.with(index, value)
```

### 參數

- `index`
  - : 要變更陣列的從零開始的索引，[轉換為整數](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number#integer_conversion)。
    - 負索引從陣列末尾開始倒數——如果 `-array.length <= index < 0`，則使用 `index + array.length`。
    - 如果正規化後的索引超出範圍，則會丟出 {{jsxref("RangeError")}}。
- `value`
  - : 要分配給指定索引的任何值。

### 回傳值回傳一個新陣列，其 `index` 上的元素已替換為 `value`。

### 例外

- {{jsxref("RangeError")}}
  - : 如果 `index >= array.length` 或 `index < -array.length`，則丟出。

## 描述

`with()` 方法會變更陣列中指定索引的值，並回傳一個新陣列，其指定索引上的元素已替換為給定的值。原始陣列不會被修改。這允許你在執行操作時串聯陣列方法。

透過將 `with()` 與 {{jsxref("Array/at", "at()")}} 結合使用，你可以使用負索引來寫入和讀取（分別）陣列。

`with()` 方法永遠不會產生[稀疏陣列](/en-US/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)。如果來源陣列是稀疏的，則新陣列中的空插槽將被替換為 `undefined`。

`with()` 方法是[泛用的](/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它只需要 `this` 值具有 `length` 屬性和整數鍵屬性。

## 範例

### 建立一個變更單一元素的新陣列

```js
const arr = [1, 2, 3, 4, 5];
console.log(arr.with(2, 6)); // [1, 2, 6, 4, 5]
console.log(arr); // [1, 2, 3, 4, 5]
```

### 串聯陣列方法使用 `with()` 方法，你可以更新陣列中的單一元素，然後套用其他陣列方法。

```js
const arr = [1, 2, 3, 4, 5];
console.log(arr.with(2, 6).map((x) => x ** 2)); // [1, 4, 36, 16, 25]
```

### 在稀疏陣列上使用 with()

`with()` 方法總是建立一個密集陣列。

```js
const arr = [1, , 3, 4, , 6];
console.log(arr.with(0, 2)); // [2, undefined, 3, 4, undefined, 6]
```

### 在非陣列物件上呼叫 with()

`with()` 方法會建立並回傳一個新陣列。它會讀取 `this` 的 `length` 屬性，然後存取每個鍵是非負整數且小於 `length` 的屬性。當存取 `this` 的每個屬性時，陣列元素（其索引等於屬性的鍵）會被設定為屬性的值。最後，`index` 處的陣列值會被設定為 `value`。

```js
const arrayLike = {
  length: 3,
  unrelated: "foo",
  0: 5,
  2: 4,
  3: 3, // with() 忽略，因為 length 為 3
};
console.log(Array.prototype.with.call(arrayLike, 0, 1));
// [ 1, undefined, 4 ]
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`Array.prototype.with` 的 Polyfill 位於 `core-js`](https://github.com/zloirock/core-js#change-array-by-copy)
- [`Array.prototype.with` 的 es-shims Polyfill](https://www.npmjs.com/package/array.prototype.with)
- [索引集合](/en-US/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array.prototype.toReversed()")}}
- {{jsxref("Array.prototype.toSorted()")}}
- {{jsxref("Array.prototype.toSpliced()")}}
- {{jsxref("Array.prototype.at()")}}
- {{jsxref("TypedArray.prototype.with()")}}
````