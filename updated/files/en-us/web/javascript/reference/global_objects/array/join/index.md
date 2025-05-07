````markdown
---
title: Array.prototype.join()
slug: Web/JavaScript/Reference/Global_Objects/Array/join
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.join
---

{{JSRef}}

**`join()`** 是 {{jsxref("Array")}} 實例的方法，透過串連這個陣列中的所有元素來建立並回傳一個新的字串，元素之間會以逗號或指定的分隔字串隔開。如果陣列只有一個項目，則會直接回傳該項目而不使用分隔符。

{{InteractiveExample("JavaScript Demo: Array.prototype.join()")}}

```js interactive-example
const elements = ["Fire", "Air", "Water"];

console.log(elements.join());
// Expected output: "Fire,Air,Water"

console.log(elements.join(""));
// Expected output: "FireAirWater"

console.log(elements.join("-"));
// Expected output: "Fire-Air-Water"
```

## 語法

```js-nolint
join()
join(separator)
```

### 參數

- `separator` {{optional_inline}}
  - : 用於分隔陣列中每對相鄰元素的字串。如果省略，陣列元素會以逗號（「,」）分隔。

### 回傳值一個包含所有陣列元素的串連字串。如果 `array.length` 為 `0`，則回傳空字串。

## 描述所有陣列元素的字串轉換會被合併成一個字串。如果元素是 `undefined` 或 `null`，它會被轉換成空字串，而不是字串 `"null"` 或 `"undefined"`。

`join` 方法在內部會被沒有參數的[`Array.prototype.toString()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/toString)存取。覆寫陣列實例的 `join` 也會覆寫其 `toString` 行為。

`Array.prototype.join` 會遞迴地將每個元素（包含其他陣列）轉換為字串。由於 `Array.prototype.toString`（與呼叫 `join()` 相同）回傳的字串沒有分隔符，因此巢狀陣列看起來像是被扁平化了。你只能控制第一層的分隔符，而更深的層級總是使用預設的逗號。

```js
const matrix = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9],
];

console.log(matrix.join()); // 1,2,3,4,5,6,7,8,9
console.log(matrix.join(";")); // 1,2,3;4,5,6;7,8,9
```

當陣列是環狀的（它包含一個本身就是元素的元素），瀏覽器會忽略環狀參照以避免無限遞迴。

```js
const arr = [];
arr.push(1, [3, arr, 4], 2);
console.log(arr.join(";")); // 1;3,,4;2
```

當用於[稀疏陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)時，`join()` 方法會將空插槽迭代為具有值 `undefined`。

`join()` 方法是[泛用的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它只需要 `this` 值具有 `length` 屬性和整數鍵屬性。

## 範例

### 以四種不同方式加入陣列以下範例建立一個具有三個元素的陣列 `a`，然後加入該陣列四次：使用預設分隔符、逗號和空格、加號以及空字串。

```js
const a = ["Wind", "Water", "Fire"];
a.join(); // 'Wind,Water,Fire'
a.join(", "); // 'Wind, Water, Fire'
a.join(" + "); // 'Wind + Water + Fire'
a.join(""); // 'WindWaterFire'
```

### 在稀疏陣列上使用 join()

`join()` 將空插槽視為與 `undefined` 相同，並產生額外的分隔符：

```js
console.log([1, , 3].join()); // '1,,3'
console.log([1, undefined, 3].join()); // '1,,3'
```

### 在非陣列物件上呼叫 join()

`join()` 方法讀取 `this` 的 `length` 屬性，然後存取每個鍵為小於 `length` 的非負整數的屬性。

```js
const arrayLike = {
  length: 3,
  0: 2,
  1: 3,
  2: 4,
  3: 5, // 被 join() 忽略，因為 length 為 3
};
console.log(Array.prototype.join.call(arrayLike));
// 2,3,4
console.log(Array.prototype.join.call(arrayLike, "."));
// 2.3.4
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`Array.prototype.join` 在 `core-js` 中的 Polyfill](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.prototype.join` 的 es-shims polyfill](https://www.npmjs.com/package/array.prototype.join)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.toString()")}}
- {{jsxref("TypedArray.prototype.join()")}}
- {{jsxref("String.prototype.split()")}}
````