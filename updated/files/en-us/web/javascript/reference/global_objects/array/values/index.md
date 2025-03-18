````markdown
---
title: Array.prototype.values()
slug: Web/JavaScript/Reference/Global_Objects/Array/values
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.values
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`values()`** 方法會回傳一個新的[陣列迭代器](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Iterator)（array iterator）物件，該物件會迭代陣列中每個項目的值。

{{InteractiveExample("JavaScript Demo: Array.prototype.values()")}}

```js interactive-example
const array1 = ["a", "b", "c"];
const iterator = array1.values();

for (const value of iterator) {
  console.log(value);
}

// Expected output: "a"
// Expected output: "b"
// Expected output: "c"
```

## 形式語法

```js-nolint
values()
```

### 參數

無。

### 回傳值

一個新的[可迭代的迭代器物件](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Iterator)。

## 描述

`Array.prototype.values()` 是 [`Array.prototype[Symbol.iterator]()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/Symbol.iterator) 的預設實作。

```js
Array.prototype.values === Array.prototype[Symbol.iterator]; // true
```

當用於[稀疏陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)時，`values()` 方法會將空插槽迭代為如同它們具有 `undefined` 值。

`values()` 方法是[泛型的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它僅期望 `this` 值具有 `length` 屬性以及整數鍵屬性。

## 範例

### 使用 for...of 迴圈進行迭代

因為 `values()` 會回傳一個可迭代的迭代器，所以你可以使用 [`for...of`](/zh-TW/docs/Web/JavaScript/Reference/Statements/for...of) 迴圈來迭代它。

```js
const arr = ["a", "b", "c", "d", "e"];
const iterator = arr.values();

for (const letter of iterator) {
  console.log(letter);
} // "a" "b" "c" "d" "e"
```

### 使用 next() 進行迭代

因為回傳值也是一個迭代器，所以你可以直接呼叫它的 `next()` 方法。

```js
const arr = ["a", "b", "c", "d", "e"];
const iterator = arr.values();
iterator.next(); // { value: "a", done: false }
iterator.next(); // { value: "b", done: false }
iterator.next(); // { value: "c", done: false }
iterator.next(); // { value: "d", done: false }
iterator.next(); // { value: "e", done: false }
iterator.next(); // { value: undefined, done: true }
console.log(iterator.next().value); // undefined
```

### 重複使用可迭代物件

> [!WARNING]
> 陣列迭代器物件應該是一次性使用的物件。請勿重複使用。

從 `values()` 回傳的可迭代物件是不可重複使用的。當 `next().done = true` 或 `currentIndex > length` 時，[`for...of` 迴圈結束](/zh-TW/docs/Web/JavaScript/Reference/Iteration_protocols#interactions_between_the_language_and_iteration_protocols)，並且進一步迭代它無效。

```js
const arr = ["a", "b", "c", "d", "e"];
const values = arr.values();
for (const letter of values) {
  console.log(letter);
}
// "a" "b" "c" "d" "e"
for (const letter of values) {
  console.log(letter);
}
// undefined
```

如果你使用 [`break`](/zh-TW/docs/Web/JavaScript/Reference/Statements/break) 敘述提早結束迭代，則當繼續迭代它時，迭代器可以從目前位置恢復。

```js
const arr = ["a", "b", "c", "d", "e"];
const values = arr.values();
for (const letter of values) {
  console.log(letter);
  if (letter === "b") {
    break;
  }
}
// "a" "b"

for (const letter of values) {
  console.log(letter);
}
// "c" "d" "e"
```

### 迭代期間的變更

沒有任何值儲存在從 `values()` 回傳的陣列迭代器物件中；相反地，它儲存了在其建立中使用的陣列的位址，並且在每次迭代時讀取目前存取的索引。因此，其迭代輸出取決於在步驟執行時儲存在該索引中的值。如果陣列中的值已變更，則陣列迭代器物件的值也會變更。

```js
const arr = ["a", "b", "c", "d", "e"];
const iterator = arr.values();
console.log(iterator); // Array Iterator { }
console.log(iterator.next().value); // "a"
arr[1] = "n";
console.log(iterator.next().value); // "n"
```

與[迭代方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#iterative_methods)不同，陣列迭代器物件不會儲存陣列建立時的長度，而是在每次迭代時讀取它一次。因此，如果陣列在迭代期間增長，則迭代器也將存取新的元素。這可能會導致無限迴圈。

```js
const arr = [1, 2, 3];
for (const e of arr) {
  arr.push(e * 10);
}
// RangeError: invalid array length
```

### 迭代稀疏陣列

`values()` 將存取空插槽，如同它們是 `undefined`。

```js
for (const element of [, "a"].values()) {
  console.log(element);
}
// undefined
// 'a'
```

### 在非陣列物件上呼叫 values()

`values()` 方法會讀取 `this` 的 `length` 屬性，然後存取每個鍵為小於 `length` 的非負整數的屬性。

```js
const arrayLike = {
  length: 3,
  0: "a",
  1: "b",
  2: "c",
  3: "d", // ignored by values() since length is 3
};
for (const entry of Array.prototype.values.call(arrayLike)) {
  console.log(entry);
}
// a
// b
// c
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`Array.prototype.values` 的 Polyfill 在 `core-js`](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.prototype.values` 的 es-shims polyfill](https://www.npmjs.com/package/array.prototype.values)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.entries()")}}
- {{jsxref("Array.prototype.keys()")}}
- [`Array.prototype[Symbol.iterator]()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/Symbol.iterator)
- {{jsxref("TypedArray.prototype.values()")}}
- [迭代協定](/zh-TW/docs/Web/JavaScript/Reference/Iteration_protocols)
````