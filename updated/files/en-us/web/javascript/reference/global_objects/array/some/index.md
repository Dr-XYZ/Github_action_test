````markdown
---
title: Array.prototype.some()
slug: Web/JavaScript/Reference/Global_Objects/Array/some
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.some
---

{{JSRef}}

**`some()`** 是 {{jsxref("Array")}} 實例的方法，用於測試陣列中是否至少有一個元素通過了提供的函式所實作的測試。如果此方法在陣列中找到一個能使提供的函式回傳 `true` 的元素，則回傳 true；否則回傳 false。此方法不會修改陣列。

{{InteractiveExample("JavaScript Demo: Array.prototype.some()")}}

```js interactive-example
const array = [1, 2, 3, 4, 5];

// 檢查元素是否為偶數
const even = (element) => element % 2 === 0;

console.log(array.some(even));
// Expected output: true
```

## 語法

```js-nolint
some(callbackFn)
some(callbackFn, thisArg)
```

### 參數

- `callbackFn`
  - : 針對陣列中的每個元素執行的函式。此函式應回傳一個 [真值](/zh-TW/docs/Glossary/Truthy) 以表示該元素通過測試，否則回傳一個 [假值](/zh-TW/docs/Glossary/Falsy)。呼叫此函式時會帶有以下引數：
    - `element`
      - : 陣列中目前正在處理的元素。
    - `index`
      - : 陣列中目前正在處理之元素的索引。
    - `array`
      - : 呼叫 `some()` 的陣列。
- `thisArg` {{optional_inline}}
  - : 執行 `callbackFn` 時作為 `this` 使用的值。參見 [迭代方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#iterative_methods)。

### 回傳值

除非 `callbackFn` 為陣列元素回傳一個 {{Glossary("truthy")}} 值，否則回傳 `false`；在這種情況下，會立即回傳 `true`。

## 描述

`some()` 方法是一種[迭代方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#iterative_methods)。它會為陣列中的每個元素呼叫一次提供的 `callbackFn` 函式，直到 `callbackFn` 回傳一個[真值](/zh-TW/docs/Glossary/Truthy)為止。如果找到這樣的元素，`some()` 會立即回傳 `true` 並停止迭代陣列。否則，如果 `callbackFn` 為所有元素都回傳一個[假值](/zh-TW/docs/Glossary/Falsy)，`some()` 則回傳 `false`。請閱讀[迭代方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#iterative_methods)章節以取得更多關於這些方法運作方式的資訊。

`some()` 的行為就像數學中的「存在量詞」。特別是，對於空陣列，它會針對任何條件回傳 `false`。

`callbackFn` 僅會針對已賦值的陣列索引呼叫。它不會針對[稀疏陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)中的空插槽呼叫。

`some()` 不會改變呼叫它的陣列，但作為 `callbackFn` 提供的函式可以。但是請注意，陣列的長度會在第一次呼叫 `callbackFn` _之前_儲存。因此：

- 當呼叫 `some()` 開始時，`callbackFn` 不會存取任何超出陣列初始長度之外新增的元素。
- 對已存取索引的變更不會導致再次針對它們呼叫 `callbackFn`。
- 如果陣列中現有但尚未存取的元素被 `callbackFn` 變更，則傳遞給 `callbackFn` 的值將是該元素被存取時的值。[已刪除](/zh-TW/docs/Web/JavaScript/Reference/Operators/delete)的元素不會被存取。

> [!WARNING]
> 上述這種並行修改通常會導致難以理解的程式碼，因此通常應避免（除非在特殊情況下）。

`some()` 方法是[通用的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它僅期望 `this` 值具有 `length` 屬性和整數鍵屬性。

## 範例

### 測試陣列元素的值

以下範例測試陣列中是否有任何元素大於 10。

```js
function isBiggerThan10(element, index, array) {
  return element > 10;
}

[2, 5, 8, 1, 4].some(isBiggerThan10); // false
[12, 5, 8, 1, 4].some(isBiggerThan10); // true
```

### 使用箭頭函式測試陣列元素

[箭頭函式](/zh-TW/docs/Web/JavaScript/Reference/Functions/Arrow_functions)
為相同的測試提供更簡短的語法。

```js
[2, 5, 8, 1, 4].some((x) => x > 10); // false
[12, 5, 8, 1, 4].some((x) => x > 10); // true
```

### 檢查陣列中是否存在某個值

為了模仿 `includes()` 方法的功能，這個自訂函式會在元素存在於陣列中時回傳 `true`：

```js
const fruits = ["apple", "banana", "mango", "guava"];

function checkAvailability(arr, val) {
  return arr.some((arrVal) => val === arrVal);
}

checkAvailability(fruits, "grapefruit"); // false
checkAvailability(fruits, "banana"); // true
```

### 將任何值轉換為布林值

```js
const TRUTHY_VALUES = [true, "true", 1];

function getBoolean(value) {
  if (typeof value === "string") {
    value = value.toLowerCase().trim();
  }

  return TRUTHY_VALUES.some((t) => t === value);
}

getBoolean(false); // false
getBoolean("false"); // false
getBoolean(1); // true
getBoolean("true"); // true
```

### 使用 callbackFn 的第三個引數

如果你想存取陣列中的另一個元素，特別是當你沒有現有變數指向該陣列時，`array` 引數會很有用。以下範例首先使用 `filter()` 提取正值，然後使用 `some()` 檢查陣列是否嚴格遞增。

```js
const numbers = [3, -1, 1, 4, 1, 5];
const isIncreasing = !numbers
  .filter((num) => num > 0)
  .some((num, idx, arr) => {
    // 如果沒有 arr 引數，就沒有辦法在不將其儲存到變數的情況下輕鬆存取
    // 中介陣列。
    if (idx === 0) return false;
    return num <= arr[idx - 1];
  });
console.log(isIncreasing); // false
```

### 在稀疏陣列上使用 some()

`some()` 不會在空插槽上執行其謂詞。

```js
console.log([1, , 3].some((x) => x === undefined)); // false
console.log([1, , 1].some((x) => x !== 1)); // false
console.log([1, undefined, 1].some((x) => x !== 1)); // true
```

### 在非陣列物件上呼叫 some()

`some()` 方法會讀取 `this` 的 `length` 屬性，然後存取每個鍵為小於 `length` 的非負整數的屬性，直到它們全部被存取或 `callbackFn` 回傳 `true`。

```js
const arrayLike = {
  length: 3,
  0: "a",
  1: "b",
  2: "c",
  3: 3, // some() 會忽略，因為 length 為 3
};
console.log(Array.prototype.some.call(arrayLike, (x) => typeof x === "number"));
// false
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`core-js` 中 `Array.prototype.some` 的 Polyfill](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.prototype.some` 的 es-shims Polyfill](https://www.npmjs.com/package/array.prototype.some)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections)指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.every()")}}
- {{jsxref("Array.prototype.forEach()")}}
- {{jsxref("Array.prototype.find()")}}
- {{jsxref("Array.prototype.includes()")}}
- {{jsxref("TypedArray.prototype.some()")}}
````