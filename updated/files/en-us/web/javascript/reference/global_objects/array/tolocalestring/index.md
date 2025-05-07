````markdown
---
title: Array.prototype.toLocaleString()
slug: Web/JavaScript/Reference/Global_Objects/Array/toLocaleString
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.toLocaleString
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`toLocaleString()`** 方法會回傳一個字串，其表示陣列中的各個元素。這些元素會使用它們的 `toLocaleString` 方法轉換為字串，並且這些字串會以特定語系的字串（例如逗號「,」）分隔。

{{InteractiveExample("JavaScript Demo: Array.prototype.toLocaleString()", "shorter")}}

```js interactive-example
const array1 = [1, "a", new Date("21 Dec 1997 14:12:00 UTC")];
const localeString = array1.toLocaleString("en", { timeZone: "UTC" });

console.log(localeString);
// Expected output: "1,a,12/21/1997, 2:12:00 PM",
// This assumes "en" locale and UTC timezone - your results may vary
// 預期輸出：「1,a,12/21/1997, 2:12:00 PM」
// 這假設是「en」語系和 UTC 時區——你的結果可能會不同
```

## 形式語法

```js-nolint
toLocaleString()
toLocaleString(locales)
toLocaleString(locales, options)
```

### 參數

- `locales` {{optional_inline}}
  - : 帶有 BCP 47 語言標籤的字串，或此類字串的陣列。關於 `locales` 參數的一般形式和解釋，參見 [`Intl` 主要頁面上的參數描述](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Intl#locales_argument)。
- `options` {{optional_inline}}
  - : 具有組態屬性的物件。你可以在此處傳遞的內容取決於要轉換的元素。例如，對於數字，參見 {{jsxref("Number.prototype.toLocaleString()")}}。

### 回傳值一個表示陣列中各個元素的字串。

## 描述

`Array.prototype.toLocaleString` 方法會遍歷其內容，使用提供的 `locales` 和 `options` 參數呼叫每個元素的 `toLocaleString` 方法，並使用實作定義的分隔符（例如逗號「,」）將它們串連起來。請注意，此方法本身不會使用這兩個參數——它只會將它們傳遞給每個元素的 `toLocaleString()`。分隔符字串的選擇取決於主機目前的語系，而不是 `locales` 參數。

如果元素為 `undefined` 或 `null`，則會將其轉換為空字串，而不是字串 `"null"` 或 `"undefined"`。

當在[稀疏陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)上使用時，`toLocaleString()` 方法會迭代空插槽，就像它們具有值 `undefined` 一樣。

`toLocaleString()` 方法是[泛型的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它僅預期 `this` 值具有 `length` 屬性和整數鍵屬性。

## 範例

### 使用 locales 和 options

陣列中的元素會使用它們的 `toLocaleString` 方法轉換為字串。例如，此程式碼片段隱式呼叫 {{jsxref("Number.prototype.toLocaleString()")}} 方法，以顯示 `prices` 陣列中字串和數字的貨幣：

```js
const prices = ["￥7", 500, 8123, 12];
prices.toLocaleString("ja-JP", { style: "currency", currency: "JPY" });

// "￥7,￥500,￥8,123,￥12"
```

### 在稀疏陣列上使用 toLocaleString()

`toLocaleString()` 將空插槽視為與 `undefined` 相同，並產生額外的分隔符：

```js
console.log([1, , 3].toLocaleString()); // '1,,3'
```

### 在非陣列物件上呼叫 toLocaleString()

`toLocaleString()` 方法會讀取 `this` 的 `length` 屬性，然後存取每個鍵為小於 `length` 的非負整數的屬性。

```js
const arrayLike = {
  length: 3,
  0: 1,
  1: 2,
  2: 3,
  3: 4, // ignored by toLocaleString() since length is 3
  // toLocaleString() 忽略，因為 length 為 3
};
console.log(Array.prototype.toLocaleString.call(arrayLike));
// 1,2,3
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections)指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.toString()")}}
- {{jsxref("TypedArray.prototype.toLocaleString()")}}
- {{jsxref("Intl")}}
- {{jsxref("Intl.ListFormat")}}
- {{jsxref("Object.prototype.toLocaleString()")}}
- {{jsxref("Number.prototype.toLocaleString()")}}
- {{jsxref("Temporal/PlainDate/toLocaleString", "Temporal.PlainDate.prototype.toLocaleString()")}}
````