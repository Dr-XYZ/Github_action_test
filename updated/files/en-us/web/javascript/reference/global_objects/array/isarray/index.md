````markdown
---
title: Array.isArray()
slug: Web/JavaScript/Reference/Global_Objects/Array/isArray
page-type: javascript-static-method
browser-compat: javascript.builtins.Array.isArray
---

{{JSRef}}

**`Array.isArray()`** 靜態方法是用來判斷傳入的值是否為 {{jsxref("Array")}}。

{{InteractiveExample("JavaScript Demo: Array.isArray()")}}

```js interactive-example
console.log(Array.isArray([1, 3, 5]));
// Expected output: true
// 預期輸出：true

console.log(Array.isArray("[]"));
// Expected output: false
// 預期輸出：false

console.log(Array.isArray(new Array(5)));
// Expected output: true
// 預期輸出：true

console.log(Array.isArray(new Int16Array([15, 33])));
// Expected output: false
// 預期輸出：false
```

## 語法

```js-nolint
Array.isArray(value)
```

### 參數

- `value`
  - : 要檢查的值。

### 回傳值如果 `value` 為 {{jsxref("Array")}}，則回傳 `true`；否則回傳 `false`。如果 `value` 為 {{jsxref("TypedArray")}} 的實例，則永遠回傳 `false`。

## 描述

`Array.isArray()` 檢查傳入的值是否為 {{jsxref("Array")}}。它會執行一種_品牌檢查（branded check）_，類似於[`in`](/en-US/docs/Web/JavaScript/Reference/Operators/in)運算子，檢查由 {{jsxref("Array/Array", "Array()")}} 建構子初始化的私有屬性。

這是一個比[`instanceof Array`](/en-US/docs/Web/JavaScript/Reference/Operators/instanceof)更穩健的替代方案，因為它可以避免誤判：

- `Array.isArray()` 會拒絕不是 `Array` 實例的值，即使它們的 prototype 鏈中有 `Array.prototype` — `instanceof Array` 會接受這些值，因為它會檢查 prototype 鏈。
- `Array.isArray()` 會接受在另一個 realm 中建構的 `Array` 物件 — `instanceof Array` 會為這些物件回傳 `false`，因為 `Array` 建構子的識別在不同的 realm 中是不同的。

參見文章[「絕對精確地判斷 JavaScript 物件是否為陣列」](https://web.mit.edu/jwalden/www/isArray.html)以取得更多詳細資訊。

## 範例

### 使用 Array.isArray()

```js
// 以下所有呼叫都會回傳 true
Array.isArray([]);
Array.isArray([1]);
Array.isArray(new Array());
Array.isArray(new Array("a", "b", "c", "d"));
Array.isArray(new Array(3));
// 鮮為人知的事實：Array.prototype 本身就是一個陣列：
Array.isArray(Array.prototype);

// 以下所有呼叫都會回傳 false
Array.isArray();
Array.isArray({});
Array.isArray(null);
Array.isArray(undefined);
Array.isArray(17);
Array.isArray("Array");
Array.isArray(true);
Array.isArray(false);
Array.isArray(new Uint8Array(32));
// 這不是一個陣列，因為它不是使用
// 陣列字面值語法或 Array 建構子建立的
Array.isArray({ __proto__: Array.prototype });
```

### instanceof vs. Array.isArray()

當檢查 `Array` 實例時，`Array.isArray()` 比 `instanceof` 更受歡迎，因為它可以跨 realm 工作。

```js
const iframe = document.createElement("iframe");
document.body.appendChild(iframe);
const xArray = window.frames[window.frames.length - 1].Array;
const arr = new xArray(1, 2, 3); // [1, 2, 3]

// 正確地檢查 Array
Array.isArray(arr); // true
// arr 的 prototype 是 xArray.prototype，
// 這是一個與 Array.prototype 不同的物件
arr instanceof Array; // false
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`core-js` 中 `Array.isArray` 的 Polyfill](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.isArray` 的 es-shims polyfill](https://www.npmjs.com/package/array.isarray)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
````