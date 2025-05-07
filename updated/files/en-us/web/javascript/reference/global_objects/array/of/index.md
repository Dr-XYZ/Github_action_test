````markdown
---
title: Array.of()
slug: Web/JavaScript/Reference/Global_Objects/Array/of
page-type: javascript-static-method
browser-compat: javascript.builtins.Array.of
---

{{JSRef}}

**`Array.of()`** 靜態方法會從可變數量的引數建立一個新的 `Array` 實例，而引數的數量或類型則不拘。

{{InteractiveExample("JavaScript Demo: Array.of()", "shorter")}}

```js interactive-example
console.log(Array.of("foo", 2, "bar", true));
// Expected output: Array ["foo", 2, "bar", true]

console.log(Array.of());
// Expected output: Array []
```

## 語法

```js-nolint
Array.of()
Array.of(element1)
Array.of(element1, element2)
Array.of(element1, element2, /* …, */ elementN)
```

### 參數

- `element1`, …, `elementN`
  - : 用於建立陣列的元素。

### 回傳值一個新的 {{jsxref("Array")}} 實例。

## 描述

`Array.of()` 與[`Array()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/Array)建構子的差異在於處理單一引數的方式：`Array.of(7)` 建立一個包含單一元素 `7` 的陣列，而 `Array(7)` 建立一個 `length` 屬性為 `7` 的空陣列。（這意味著一個包含 7 個空欄位的陣列，而不是包含實際 {{jsxref("undefined")}} 值的欄位。）

```js
Array.of(7); // [7]
Array(7); // array of 7 empty slots

Array.of(1, 2, 3); // [1, 2, 3]
Array(1, 2, 3); // [1, 2, 3]
```

`Array.of()` 方法是一個泛用的工廠方法。舉例來說，如果 `Array` 的子類別繼承了 `of()` 方法，則繼承的 `of()` 方法會回傳子類別的新實例，而不是 `Array` 實例。實際上，`this` 的值可以是任何接受單一引數的建構子函式，該引數代表新陣列的長度，並且會使用傳遞給 `of()` 的引數數量來呼叫該建構子。當所有元素都已賦值後，最終的 `length` 會再次被設定。如果 `this` 的值不是建構子函式，則會改為使用普通的 `Array` 建構子。

## 範例

### 使用 Array.of()

```js
Array.of(1); // [1]
Array.of(1, 2, 3); // [1, 2, 3]
Array.of(undefined); // [undefined]
```

### 在非陣列建構子上呼叫 of()

`of()` 方法可以在任何接受單一引數的建構子函式上呼叫，該引數代表新陣列的長度。

```js
function NotArray(len) {
  console.log("NotArray called with length", len);
}

console.log(Array.of.call(NotArray, 1, 2, 3));
// NotArray called with length 3
// NotArray { '0': 1, '1': 2, '2': 3, length: 3 }

console.log(Array.of.call(Object)); // [Number: 0] { length: 0 }
```

當 `this` 值不是建構子時，會回傳一個普通的 `Array` 物件。

```js
console.log(Array.of.call({}, 1)); // [ 1 ]
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`core-js` 中 `Array.of` 的 Polyfill](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.of` 的 es-shims polyfill](https://www.npmjs.com/package/array.of)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Array/Array", "Array()")}}
- {{jsxref("Array.from()")}}
- {{jsxref("TypedArray.of()")}}
````