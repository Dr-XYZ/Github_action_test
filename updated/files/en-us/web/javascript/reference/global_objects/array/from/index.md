````markdown
---
title: Array.from()
slug: Web/JavaScript/Reference/Global_Objects/Array/from
page-type: javascript-static-method
browser-compat: javascript.builtins.Array.from
---

{{JSRef}}

**`Array.from()`** 靜態方法會從可迭代（iterable）或類陣列（array-like）物件建立一個新的、淺複製的 `Array` 實例。

{{InteractiveExample("JavaScript Demo: Array.from()", "shorter")}}

```js interactive-example
console.log(Array.from("foo"));
// Expected output: Array ["f", "o", "o"]

console.log(Array.from([1, 2, 3], (x) => x + x));
// Expected output: Array [2, 4, 6]
```

## 語法

```js-nolint
Array.from(arrayLike)
Array.from(arrayLike, mapFn)
Array.from(arrayLike, mapFn, thisArg)
```

### 參數

- `arrayLike`
  - : 要轉換為陣列的可迭代或類陣列物件。
- `mapFn` {{optional_inline}}
  - : 要在陣列的每個元素上呼叫的函式。如果提供此參數，則要新增至陣列的每個值都會先傳遞到此函式，並將 `mapFn` 的回傳值新增到陣列中。呼叫此函式時會帶有以下參數：
    - `element`
      - : 陣列中目前正在處理的元素。
    - `index`
      - : 陣列中目前正在處理的元素的索引。
- `thisArg` {{optional_inline}}
  - : 執行 `mapFn` 時作為 `this` 使用的值。

### 回傳值

一個新的 {{jsxref("Array")}} 實例。

## 描述

`Array.from()` 允許你從以下項目建立 `Array`：

- [可迭代物件](/zh-TW/docs/Web/JavaScript/Reference/Iteration_protocols)（例如 {{jsxref("Map")}} 和 {{jsxref("Set")}}）；或者，如果該物件不可迭代，
- 類陣列物件（具有 `length` 屬性和索引元素的物件）。

若要將不是可迭代或類陣列的普通物件轉換為陣列（透過枚舉其屬性鍵、值或兩者），請使用 {{jsxref("Object.keys()")}}, {{jsxref("Object.values()")}}, 或 {{jsxref("Object.entries()")}}. 若要將 [async iterable](/zh-TW/docs/Web/JavaScript/Reference/Iteration_protocols#the_async_iterator_and_async_iterable_protocols) 轉換為陣列，請使用 {{jsxref("Array.fromAsync()")}}.

`Array.from()` 永遠不會建立稀疏陣列。如果 `arrayLike` 物件缺少某些索引屬性，則它們在新陣列中會變成 `undefined`。

`Array.from()` 具有一個可選參數 `mapFn`，允許你在正在建立的陣列的每個元素上執行函式，類似於 {{jsxref("Array/map", "map()")}}. 更清楚地說，`Array.from(obj, mapFn, thisArg)` 具有與 `Array.from(obj).map(mapFn, thisArg)` 相同的結果，但它不會建立中間陣列，並且 `mapFn` 只會接收兩個參數（`element`，`index`），而沒有整個陣列，因為該陣列仍在建構中。

> [!NOTE]
>
> 此行為對於 [typed arrays](/zh-TW/docs/Web/JavaScript/Guide/Typed_arrays) 而言更為重要，因為中間陣列必須將值截斷以適應適當的類型。`Array.from()` 的實作使其具有與 {{jsxref("TypedArray.from()")}} 相同的簽名。

`Array.from()` 方法是一個泛型工廠方法。例如，如果 `Array` 的子類別繼承了 `from()` 方法，則繼承的 `from()` 方法將會回傳子類別的新實例，而不是 `Array` 實例。實際上，`this` 值可以是任何接受單一參數（代表新陣列的長度）的建構函式。當可迭代物件作為 `arrayLike` 傳遞時，會呼叫不帶參數的建構函式；當類陣列物件傳遞時，會呼叫帶有類陣列物件的 [正規化長度](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#normalization_of_the_length_property) 的建構函式。在迭代完成時，最終的 `length` 將會再次設定。如果 `this` 值不是建構函式，則會改為使用 plain `Array` 建構函式。

## 範例

### 從字串建立陣列

```js
Array.from("foo");
// [ "f", "o", "o" ]
```

### 從 Set 建立陣列

```js
const set = new Set(["foo", "bar", "baz", "foo"]);
Array.from(set);
// [ "foo", "bar", "baz" ]
```

### 從 Map 建立陣列

```js
const map = new Map([
  [1, 2],
  [2, 4],
  [4, 8],
]);
Array.from(map);
// [[1, 2], [2, 4], [4, 8]]

const mapper = new Map([
  ["1", "a"],
  ["2", "b"],
]);
Array.from(mapper.values());
// ['a', 'b'];

Array.from(mapper.keys());
// ['1', '2'];
```

### 從 NodeList 建立陣列

```js
// 根據 DOM 元素的屬性建立陣列
const images = document.querySelectorAll("img");
const sources = Array.from(images, (image) => image.src);
const insecureSources = sources.filter((link) => link.startsWith("http://"));
```

### 從類陣列物件（arguments）建立陣列

```js
function f() {
  return Array.from(arguments);
}

f(1, 2, 3);

// [ 1, 2, 3 ]
```

### 使用箭頭函式和 Array.from()

```js
// 使用箭頭函式作為 map 函式來操作元素
Array.from([1, 2, 3], (x) => x + x);
// [2, 4, 6]

// 產生數字序列
// 由於陣列在每個位置都以 `undefined` 初始化，
// 因此下面的 `v` 的值將會是 `undefined`
Array.from({ length: 5 }, (v, i) => i);
// [0, 1, 2, 3, 4]
```

### 序列產生器（範圍）

```js
// 序列產生器函式（通常稱為「範圍」，參見 Python、Clojure 等）
const range = (start, stop, step) =>
  Array.from(
    { length: Math.ceil((stop - start) / step) },
    (_, i) => start + i * step,
  );

// 產生一個從 0（含）到 5（不含）的數字序列，以 1 遞增
range(0, 5, 1);
// [0, 1, 2, 3, 4]

// 產生一個從 1（含）到 10（不含）的數字序列，以 2 遞增
range(1, 10, 2);
// [1, 3, 5, 7, 9]

// 產生拉丁字母，並利用它作為序列排序
range("A".charCodeAt(0), "Z".charCodeAt(0) + 1, 1).map((x) =>
  String.fromCharCode(x),
);
// ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
```

### 在非陣列建構函式上呼叫 from()

`from()` 方法可以在任何接受單一參數（代表新陣列的長度）的建構函式上呼叫。

```js
function NotArray(len) {
  console.log("NotArray called with length", len);
}

// Iterable
console.log(Array.from.call(NotArray, new Set(["foo", "bar", "baz"])));
// NotArray called with length undefined
// NotArray { '0': 'foo', '1': 'bar', '2': 'baz', length: 3 }

// Array-like
console.log(Array.from.call(NotArray, { length: 1, 0: "foo" }));
// NotArray called with length 1
// NotArray { '0': 'foo', length: 1 }
```

當 `this` 值不是建構函式時，會回傳 plain `Array` 物件。

```js
console.log(Array.from.call({}, { length: 1, 0: "foo" })); // [ 'foo' ]
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`Array.from` 在 `core-js` 中的 Polyfill](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.from` 的 es-shims polyfill](https://www.npmjs.com/package/array.from)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Array/Array", "Array()")}}
- {{jsxref("Array.of()")}}
- {{jsxref("Array.fromAsync()")}}
- {{jsxref("Array.prototype.map()")}}
- {{jsxref("TypedArray.from()")}}
````