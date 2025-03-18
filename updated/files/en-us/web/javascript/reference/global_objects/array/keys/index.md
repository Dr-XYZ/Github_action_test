````markdown
---
title: Array.prototype.keys()
slug: Web/JavaScript/Reference/Global_Objects/Array/keys
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.keys
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`keys()`** 方法會回傳一個新的[陣列迭代器](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Iterator)物件，其包含陣列中每個索引的鍵。

{{InteractiveExample("JavaScript Demo: Array.prototype.keys()")}}

```js interactive-example
const array1 = ["a", "b", "c"];
const iterator = array1.keys();

for (const key of iterator) {
  console.log(key);
}

// Expected output: 0
// Expected output: 1
// Expected output: 2
```

## 形式語法

```js-nolint
keys()
```

### 參數

無。

### 回傳值

一個新的[可迭代的迭代器物件](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Iterator)。

## 描述

當用於[稀疏陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)時，`keys()` 方法會迭代空插槽，如同它們具有 `undefined` 值一樣。

`keys()` 方法是[泛用的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它只要求 `this` 值具有 `length` 屬性和整數鍵屬性。

## 範例

### 在稀疏陣列上使用 keys()

與 {{jsxref("Object.keys()")}} 不同，後者僅包含陣列中實際存在的鍵，`keys()` 迭代器不會忽略代表遺失屬性的空缺。

```js
const arr = ["a", , "c"];
const sparseKeys = Object.keys(arr);
const denseKeys = [...arr.keys()];
console.log(sparseKeys); // ['0', '2']
console.log(denseKeys); // [0, 1, 2]
```

### 在非陣列物件上呼叫 keys()

`keys()` 方法讀取 `this` 的 `length` 屬性，然後產生 0 到 `length - 1` 之間的所有整數索引。實際上沒有發生索引存取。

```js
const arrayLike = {
  length: 3,
};
for (const entry of Array.prototype.keys.call(arrayLike)) {
  console.log(entry);
}
// 0
// 1
// 2
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`core-js` 中 `Array.prototype.keys` 的 Polyfill](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.prototype.keys` 的 es-shims Polyfill](https://www.npmjs.com/package/array.prototype.keys)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.entries()")}}
- {{jsxref("Array.prototype.values()")}}
- [`Array.prototype[Symbol.iterator]()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/Symbol.iterator)
- {{jsxref("TypedArray.prototype.keys()")}}
- [迭代協定](/zh-TW/docs/Web/JavaScript/Reference/Iteration_protocols)
````