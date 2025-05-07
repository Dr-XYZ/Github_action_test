````
---
title: Array.prototype.map()
slug: Web/JavaScript/Reference/Global_Objects/Array/map
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.map
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`map()`** 方法會建立一個新的陣列，其元素為呼叫此陣列中每一個元素所產生的結果。

{{InteractiveExample("JavaScript Demo: Array.prototype.map()")}}

```js interactive-example
const array1 = [1, 4, 9, 16];

// Pass a function to map
// 傳遞一個函式給 map
const map1 = array1.map((x) => x * 2);

console.log(map1);
// Expected output: Array [2, 8, 18, 32]
// 預期輸出：Array [2, 8, 18, 32]
```

## 語法

```js-nolint
map(callbackFn)
map(callbackFn, thisArg)
```

### 參數

- `callbackFn`
  - : 一個為陣列中的每個元素執行的函式。其回傳值會作為一個單一元素被加到新的陣列中。該函式會以下列參數呼叫：
    - `element`
      - : 陣列中目前正在處理的元素。
    - `index`
      - : 陣列中目前正在處理之元素的索引。
    - `array`
      - : 呼叫 `map()` 的陣列。
- `thisArg` {{optional_inline}}
  - : 當執行 `callbackFn` 時，用來作為 `this` 的值。參見[迭代方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#iterative_methods)。

### 回傳值一個新的陣列，其每個元素皆是回呼函式的結果。

## 描述

`map()` 方法是一個[迭代方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#iterative_methods)。它會為陣列中的每個元素呼叫一次所提供的 `callbackFn` 函式，並從結果中建構一個新的陣列。閱讀[迭代方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#iterative_methods)章節以獲得關於這些方法如何運作的更多訊息。

`callbackFn` 僅會為有賦值的陣列索引呼叫。它不會為[稀疏陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)中的空缺呼叫。

`map()` 方法是[泛用的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它僅預期 `this` 值具有 `length` 屬性與整數鍵屬性。

由於 `map` 會建立一個新的陣列，因此在沒有使用回傳陣列的情況下呼叫它是一種反模式；請改用 {{jsxref("Array/forEach", "forEach")}} 或 {{jsxref("Statements/for...of", "for...of")}}。

## 範例

### 將數字陣列映射到平方根陣列下列程式碼取得一個數字陣列，並建立一個新的陣列，其中包含第一個陣列中數字的平方根。

```js
const numbers = [1, 4, 9];
const roots = numbers.map((num) => Math.sqrt(num));

// roots is now     [1, 2, 3]
// roots 現在是 [1, 2, 3]
// numbers is still [1, 4, 9]
// numbers 仍然是 [1, 4, 9]
```

### 使用 map 重新格式化陣列中的物件下列程式碼取得一個物件陣列，並建立一個新的陣列，其中包含新重新格式化的物件。

```js
const kvArray = [
  { key: 1, value: 10 },
  { key: 2, value: 20 },
  { key: 3, value: 30 },
];

const reformattedArray = kvArray.map(({ key, value }) => ({ [key]: value }));

console.log(reformattedArray); // [{ 1: 10 }, { 2: 20 }, { 3: 30 }]
console.log(kvArray);
// [
//   { key: 1, value: 10 },
//   { key: 2, value: 20 },
//   { key: 3, value: 30 }
// ]
```

### 將 parseInt() 與 map() 搭配使用通常會使用帶有一個參數（正在遍歷的元素）的回呼。某些函式也常與一個參數一起使用，即使它們帶有額外的可選參數。這些習慣可能會導致混淆的行為。請考慮：

```js
["1", "2", "3"].map(parseInt);
```

雖然可能會預期 `[1, 2, 3]`，但實際結果是 `[1, NaN, NaN]`。

{{jsxref("parseInt")}} 經常與一個參數一起使用，但接受兩個參數。第一個是表達式，第二個是回呼函式的進位基底，`Array.prototype.map` 傳遞 3 個參數：元素、索引和陣列。第三個參數會被 {{jsxref("parseInt")}} 忽略——但 _不是_ 第二個參數！這是可能造成混淆的原因。

以下是迭代步驟的簡潔範例：

```js
/* first iteration  (index is 0): */ parseInt("1", 0); // 1
/* 第一次迭代（索引為 0）：*/ parseInt("1", 0); // 1
/* second iteration (index is 1): */ parseInt("2", 1); // NaN
/* 第二次迭代（索引為 1）：*/ parseInt("2", 1); // NaN
/* third iteration  (index is 2): */ parseInt("3", 2); // NaN
/* 第三次迭代（索引為 2）：*/ parseInt("3", 2); // NaN
```

若要解決此問題，請定義另一個僅接受一個參數的函式：

```js
["1", "2", "3"].map((str) => parseInt(str, 10)); // [1, 2, 3]
```

你也可以使用 {{jsxref("Number")}} 函式，它僅接受一個參數：

```js
["1", "2", "3"].map(Number); // [1, 2, 3]

// But unlike parseInt(), Number() will also return a float or (resolved) exponential notation:
// 但與 parseInt() 不同，Number() 也會回傳浮點數或（已解析的）指數表示法：
["1.1", "2.2e2", "3e300"].map(Number); // [1.1, 220, 3e+300]

// For comparison, if we use parseInt() on the array above:
// 為了比較，如果我們在上面的陣列上使用 parseInt()：
["1.1", "2.2e2", "3e300"].map((str) => parseInt(str, 10)); // [1, 2, 3]
```

參見 Allen Wirfs-Brock 的[A JavaScript optional argument hazard](https://wirfs-brock.com/allen/posts/166)以獲得更多討論。

### 映射的陣列包含 undefined

當回傳 {{jsxref("undefined")}} 或沒有回傳任何東西時，產生的陣列會包含 `undefined`。如果你想要改為刪除元素，請串聯 {{jsxref("Array/filter", "filter()")}} 方法，或使用 {{jsxref("Array/flatMap", "flatMap()")}} 方法並回傳一個空陣列以表示刪除。

```js
const numbers = [1, 2, 3, 4];
const filteredNumbers = numbers.map((num, index) => {
  if (index < 3) {
    return num;
  }
});

// index goes from 0, so the filterNumbers are 1,2,3 and undefined.
// 索引從 0 開始，因此 filterNumbers 為 1,2,3 和 undefined。
// filteredNumbers is [1, 2, 3, undefined]
// filteredNumbers 為 [1, 2, 3, undefined]
// numbers is still [1, 2, 3, 4]
// numbers 仍然為 [1, 2, 3, 4]
```

### 具有副作用的映射回呼可以具有副作用。

```js
const cart = [5, 15, 25];
let total = 0;
const withTax = cart.map((cost) => {
  total += cost;
  return cost * 1.2;
});
console.log(withTax); // [6, 18, 30]
console.log(total); // 45
```

不建議這樣做，因為複製方法最好與純函式一起使用。在這種情況下，我們可以選擇迭代陣列兩次。

```js
const cart = [5, 15, 25];
const total = cart.reduce((acc, cost) => acc + cost, 0);
const withTax = cart.map((cost) => cost * 1.2);
```

有時這種模式會達到極致，而 `map()` 唯一有用的事情就是造成副作用。

```js
const products = [
  { name: "sports car" },
  { name: "laptop" },
  { name: "phone" },
];

products.map((product) => {
  product.price = 100;
});
```

如前所述，這是一種反模式。如果你沒有使用 `map()` 的回傳值，請改用 `forEach()` 或 `for...of` 迴圈。

```js
products.forEach((product) => {
  product.price = 100;
});
```

或者，如果你想要建立一個新的陣列：

```js
const productsWithPrice = products.map((product) => {
  return { ...product, price: 100 };
});
```

### 使用 callbackFn 的第三個參數如果你想要存取陣列中的另一個元素，`array` 參數會很有用，尤其是當你沒有現有變數指向該陣列時。下列範例首先使用 `filter()` 提取正值，然後使用 `map()` 建立一個新的陣列，其中每個元素都是其相鄰元素與其自身的平均值。

```js
const numbers = [3, -1, 1, 4, 1, 5, 9, 2, 6];
const averaged = numbers
  .filter((num) => num > 0)
  .map((num, idx, arr) => {
    // Without the arr argument, there's no way to easily access the
    // intermediate array without saving it to a variable.
    // 如果沒有 arr 參數，就無法輕易存取中間陣列，而無需將其儲存到變數中。
    const prev = arr[idx - 1];
    const next = arr[idx + 1];
    let count = 1;
    let total = num;
    if (prev !== undefined) {
      count++;
      total += prev;
    }
    if (next !== undefined) {
      count++;
      total += next;
    }
    const average = total / count;
    // Keep two decimal places
    // 保留兩位小數
    return Math.round(average * 100) / 100;
  });
console.log(averaged); // [2, 2.67, 2, 3.33, 5, 5.33, 5.67, 4]
```

`array` 參數 _不是_ 正在建立的陣列——沒有辦法從回呼函式存取正在建立的陣列。

### 在稀疏陣列上使用 map()

稀疏陣列在 `map()` 之後仍然是稀疏的。空缺的索引在回傳的陣列中仍然是空的，並且不會在這些索引上呼叫回呼函式。

```js
console.log(
  [1, , 3].map((x, index) => {
    console.log(`Visit ${index}`);
    return x * 2;
  }),
);
// Visit 0
// 走訪 0
// Visit 2
// 走訪 2
// [2, empty, 6]
// [2, 空, 6]
```

### 在非陣列物件上呼叫 map()

`map()` 方法讀取 `this` 的 `length` 屬性，然後存取每個鍵為小於 `length` 的非負整數的屬性。

```js
const arrayLike = {
  length: 3,
  0: 2,
  1: 3,
  2: 4,
  3: 5, // ignored by map() since length is 3
  // map() 忽略，因為長度為 3
};
console.log(Array.prototype.map.call(arrayLike, (x) => x ** 2));
// [ 4, 9, 16 ]
```

此範例展示如何迭代由 `querySelectorAll` 收集的物件集合。這是因為 `querySelectorAll` 會回傳一個 `NodeList`（它是物件的集合）。在這種情況下，我們會回傳畫面上所有選取的 `option` 的值：

```js
const elems = document.querySelectorAll("select option:checked");
const values = Array.prototype.map.call(elems, ({ value }) => value);
```

你也可以使用 {{jsxref("Array.from()")}} 將 `elems` 轉換為陣列，然後存取 `map()` 方法。

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`Array.prototype.map` 在 `core-js` 中的 Polyfill](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.prototype.map` 的 es-shims polyfill](https://www.npmjs.com/package/array.prototype.map)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections)指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.forEach()")}}
- {{jsxref("Array.from()")}}
- {{jsxref("TypedArray.prototype.map()")}}
- {{jsxref("Map")}}
````