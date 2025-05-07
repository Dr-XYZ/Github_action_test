````markdown
---
title: Array.fromAsync()
slug: Web/JavaScript/Reference/Global_Objects/Array/fromAsync
page-type: javascript-static-method
browser-compat: javascript.builtins.Array.fromAsync
---

{{JSRef}}

**`Array.fromAsync()`** 靜態方法會從一個[非同步可迭代](/zh-TW/docs/Web/JavaScript/Reference/Iteration_protocols#the_async_iterator_and_async_iterable_protocols)、[可迭代](/zh-TW/docs/Web/JavaScript/Reference/Iteration_protocols#the_iterable_protocol)或[類陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#working_with_array-like_objects)物件建立一個新的、淺複製的 `Array` 實例。

## 語法

```js-nolint
Array.fromAsync(arrayLike)
Array.fromAsync(arrayLike, mapFn)
Array.fromAsync(arrayLike, mapFn, thisArg)
```

### 參數

- `arrayLike`
  - : 一個要轉換為陣列的非同步可迭代、可迭代或類陣列物件。
- `mapFn` {{optional_inline}}
  - : 將在陣列的每個元素上呼叫的函式。如果提供，則要新增到陣列的每個值都會先經過此函式，並且會將 `mapFn` 的回傳值（在[await](/zh-TW/docs/Web/JavaScript/Reference/Operators/await)之後）新增到陣列中。該函式會使用以下引數呼叫：
    - `element`
      - : 陣列中目前正在處理的元素。由於所有元素都首先被 [await](/zh-TW/docs/Web/JavaScript/Reference/Operators/await)，因此此值永遠不會是 [thenable](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Promise#thenables)。
    - `index`
      - : 陣列中目前正在處理的元素的索引。
- `thisArg` {{optional_inline}}
  - : 執行 `mapFn` 時要用作 `this` 的值。

### 回傳值一個新的 {{jsxref("Promise")}}，其 fulfillment value 是一個新的 {{jsxref("Array")}} 實例。

## 描述

`Array.fromAsync()` 允許你從以下項目建立陣列：

- [非同步可迭代物件](/zh-TW/docs/Web/JavaScript/Reference/Iteration_protocols#the_async_iterator_and_async_iterable_protocols)（例如 {{domxref("ReadableStream")}} 和 {{jsxref("AsyncGenerator")}} 的物件）；或者，如果該物件不是非同步可迭代的，
- [可迭代物件](/zh-TW/docs/Web/JavaScript/Reference/Iteration_protocols#the_iterable_protocol)（例如 {{jsxref("Map")}} 和 {{jsxref("Set")}} 的物件）；或者，如果該物件不是可迭代的，
- 類陣列物件（具有 `length` 屬性和索引元素的物件）。

`Array.fromAsync()` 以非常類似於 {{jsxref("Statements/for-await...of", "for await...of")}} 的方式迭代非同步可迭代物件。`Array.fromAsync()` 在行為方面幾乎等同於 {{jsxref("Array.from()")}}，除了以下幾點：

- `Array.fromAsync()` 處理非同步可迭代物件。
- `Array.fromAsync()` 回傳一個 {{jsxref("Promise")}}，該 Promise 會 fulfill 為陣列實例。
- 如果呼叫 `Array.fromAsync()` 時使用非非同步可迭代物件，則要新增到陣列的每個元素都會先被 [await](/zh-TW/docs/Web/JavaScript/Reference/Operators/await)。
- 如果提供了 `mapFn`，則其輸入和輸出會在內部被 await。

`Array.fromAsync()` 和 {{jsxref("Promise.all()")}} 都可以將 promises 的可迭代物件轉換為 promise 的陣列。但是，它們之間有兩個關鍵差異：

- `Array.fromAsync()` 循序地 await 從物件產生的每個值。`Promise.all()` 同時 await 所有值。
- `Array.fromAsync()` 延遲地迭代可迭代物件，並且在目前的值 settled 之前不會檢索下一個值。`Promise.all()` 提前檢索所有值並 await 它們。

## 範例

### 從非同步可迭代物件建立陣列

```js
const asyncIterable = (async function* () {
  for (let i = 0; i < 5; i++) {
    await new Promise((resolve) => setTimeout(resolve, 10 * i));
    yield i;
  }
})();

Array.fromAsync(asyncIterable).then((array) => console.log(array));
// [0, 1, 2, 3, 4]
```

### 從同步可迭代物件建立陣列

```js
Array.fromAsync(
  new Map([
    [1, 2],
    [3, 4],
  ]),
).then((array) => console.log(array));
// [[1, 2], [3, 4]]
```

### 從產生 promises 的同步可迭代物件建立陣列

```js
Array.fromAsync(
  new Set([Promise.resolve(1), Promise.resolve(2), Promise.resolve(3)]),
).then((array) => console.log(array));
// [1, 2, 3]
```

### 從類陣列的 promises 物件建立陣列

```js
Array.fromAsync({
  length: 3,
  0: Promise.resolve(1),
  1: Promise.resolve(2),
  2: Promise.resolve(3),
}).then((array) => console.log(array));
// [1, 2, 3]
```

### 使用 mapFn

`mapFn` 的輸入和輸出都在內部被 `Array.fromAsync()` await。

```js
function delayedValue(v) {
  return new Promise((resolve) => setTimeout(() => resolve(v), 100));
}

Array.fromAsync(
  [delayedValue(1), delayedValue(2), delayedValue(3)],
  (element) => delayedValue(element * 2),
).then((array) => console.log(array));
// [2, 4, 6]
```

### 與 Promise.all() 的比較

`Array.fromAsync()` 循序地 await 從物件產生的每個值。`Promise.all()` 同時 await 所有值。

```js
function* makeIterableOfPromises() {
  for (let i = 0; i < 5; i++) {
    yield new Promise((resolve) => setTimeout(resolve, 100));
  }
}

(async () => {
  console.time("Array.fromAsync() time");
  await Array.fromAsync(makeIterableOfPromises());
  console.timeEnd("Array.fromAsync() time");
  // Array.fromAsync() time: 503.610ms

  console.time("Promise.all() time");
  await Promise.all(makeIterableOfPromises());
  console.timeEnd("Promise.all() time");
  // Promise.all() time: 101.728ms
})();
```

### 對於同步可迭代物件沒有錯誤處理與[`for await...of`](/zh-TW/docs/Web/JavaScript/Reference/Statements/for-await...of#iterating_over_sync_iterables_and_generators)類似，如果迭代的物件是同步可迭代物件，並且在迭代時發生錯誤，則不會呼叫底層迭代器的 `return()` 方法，因此迭代器不會關閉。

```js
function* generatorWithRejectedPromises() {
  try {
    yield 0;
    yield Promise.reject(3);
  } finally {
    console.log("called finally");
  }
}

(async () => {
  try {
    await Array.fromAsync(generatorWithRejectedPromises());
  } catch (e) {
    console.log("caught", e);
  }
})();
// caught 3
// No "called finally" message
```

如果你需要關閉迭代器，則需要改用 {{jsxref("Statements/for...of", "for...of")}} 迴圈，並自己 `await` 每個值。

```js
(async () => {
  const arr = [];
  try {
    for (const val of generatorWithRejectedPromises()) {
      arr.push(await val);
    }
  } catch (e) {
    console.log("caught", e);
  }
})();
// called finally
// caught 3
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`core-js` 中 `Array.fromAsync` 的 Polyfill](https://github.com/zloirock/core-js#arrayfromasync)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Array/Array", "Array()")}}
- {{jsxref("Array.of()")}}
- {{jsxref("Array.from()")}}
- {{jsxref("Statements/for-await...of", "for await...of")}}
````