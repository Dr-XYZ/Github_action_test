````
---
title: Array.prototype[Symbol.unscopables]
slug: Web/JavaScript/Reference/Global_Objects/Array/Symbol.unscopables
page-type: javascript-instance-data-property
browser-compat: javascript.builtins.Array.@@unscopables
---

{{JSRef}}

{{jsxref("Array.prototype")}} 的 **`[Symbol.unscopables]`** 資料屬性由所有 {{jsxref("Array")}} 實例共享。它包含 ES2015 版本之前未包含在 ECMAScript 標準中，且為了[`with`](/zh-TW/docs/Web/JavaScript/Reference/Statements/with)陳述式綁定目的而被忽略的屬性名稱。

## 值具有下列屬性名稱且其值設定為 `true` 的 [`null`-prototype 物件](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Object#null-prototype_objects)。

{{js_property_attributes(0, 0, 1)}}

## 描述為了 `with` 陳述式綁定目的而被忽略的預設 `Array` 屬性為：

- [`at()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/at)
- [`copyWithin()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/copyWithin)
- [`entries()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/entries)
- [`fill()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/fill)
- [`find()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/find)
- [`findIndex()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/findIndex)
- [`findLast()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/findLast)
- [`findLastIndex()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/findLastIndex)
- [`flat()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/flat)
- [`flatMap()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/flatMap)
- [`includes()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/includes)
- [`keys()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/keys)
- [`toReversed()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/toReversed)
- [`toSorted()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/toSorted)
- [`toSpliced()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/toSpliced)
- [`values()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/values)

`Array.prototype[Symbol.unscopables]` 是一個僅包含上述所有屬性名稱且值為 `true` 的空物件。它的[原型為 `null`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Object#null-prototype_objects)，因此像[`toString`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Object/toString)這樣的 `Object.prototype` 屬性不會意外地變成 unscopable，且 `with` 陳述式中的 `toString()` 將繼續在陣列上呼叫。

參見 {{jsxref("Symbol.unscopables")}} 以了解如何為你自己的物件設定 unscopable 屬性。

## 範例假設下方的 `values.push('something')` 呼叫位於 ECMAScript 2015 之前編寫的程式碼中。

```js
var values = [];

with (values) {
  values.push("something");
}
```

當 ECMAScript 2015 引入了 {{jsxref("Array.prototype.values()")}} 方法時，上述程式碼中的 `with` 陳述式開始將 `values` 解釋為 `values.values` 陣列方法，而不是外部的 `values` 變數。`values.push('something')` 呼叫會中斷，因為它現在正在存取 `values.values` 方法上的 `push`。這導致一個錯誤回報給 Firefox ([Firefox Bug 883914](https://bugzil.la/883914))。

因此，`Array.prototype` 的 `[Symbol.unscopables]` 資料屬性會使 ECMAScript 2015 中引入的 `Array` 屬性為了 `with` 陳述式綁定目的而被忽略——允許 ECMAScript 2015 之前編寫的程式碼繼續如預期般運作，而不是中斷。

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`core-js` 中 `Array.prototype[Symbol.unscopables]` 的 Polyfill](https://github.com/zloirock/core-js#ecmascript-array)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Statements/with", "with")}}
- {{jsxref("Symbol.unscopables")}}
````