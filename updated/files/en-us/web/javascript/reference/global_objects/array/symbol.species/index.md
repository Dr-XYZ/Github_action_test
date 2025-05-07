````markdown
---
title: Array[Symbol.species]
slug: Web/JavaScript/Reference/Global_Objects/Array/Symbol.species
page-type: javascript-static-accessor-property
browser-compat: javascript.builtins.Array.@@species
---

{{JSRef}}

**`Array[Symbol.species]`** 靜態存取子屬性會回傳用來建構陣列方法的回傳值的建構子。

> [!WARNING]
> `[Symbol.species]` 的存在允許任意程式碼的執行，並可能產生安全性漏洞。這也使某些最佳化變得更加困難。引擎實作者正在[研究是否要移除此功能](https://github.com/tc39/proposal-rm-builtin-subclassing)。如果可能，請避免依賴它。現代陣列方法，例如 {{jsxref("Array/toReversed", "toReversed()")}}，不使用 `[Symbol.species]`，並且總是回傳一個新的 `Array` 基礎類別實例。

## 語法

```js-nolint
Array[Symbol.species]
```

### 回傳值呼叫 `get [Symbol.species]` 的建構子（`this`）的值。回傳值用於從建立新陣列的陣列方法建構回傳值。

## 描述

`[Symbol.species]` 存取子屬性會回傳 `Array` 物件的預設建構子。子類別建構子可能會覆寫它，以變更建構子的指定。預設實作基本上是：

```js
// 假設的底層實作，僅用於說明
class Array {
  static get [Symbol.species]() {
    return this;
  }
}
```

由於這種多型實作，衍生子類別的 `[Symbol.species]` 預設也會回傳建構子本身。

```js
class SubArray extends Array {}
SubArray[Symbol.species] === SubArray; // true
```

當呼叫不會改變現有陣列，而是回傳新陣列實例的陣列方法（例如，[`filter()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/filter) 和 [`map()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/map)）時，將會存取陣列的 `constructor[Symbol.species]`。回傳的建構子將用於建構陣列方法的回傳值。這在技術上使得陣列方法可以回傳與陣列無關的物件。

```js
class NotAnArray {
  constructor(length) {
    this.length = length;
  }
}

const arr = [0, 1, 2];
arr.constructor = { [Symbol.species]: NotAnArray };
arr.map((i) => i); // NotAnArray { '0': 0, '1': 1, '2': 2, length: 3 }
arr.filter((i) => i); // NotAnArray { '0': 1, '1': 2, length: 0 }
arr.concat([1, 2]); // NotAnArray { '0': 0, '1': 1, '2': 2, '3': 1, '4': 2, length: 5 }
```

## 範例

### 一般物件中的 species

`[Symbol.species]` 屬性會回傳預設建構子函式，也就是 `Array` 的 `Array` 建構子。

```js
Array[Symbol.species]; // [Function: Array]
```

### 衍生物件中的 species

在自訂 `Array` 子類別（例如 `MyArray`）的實例中，`MyArray` 的 species 是 `MyArray` 建構子。但是，你可能想要覆寫此值，以便在衍生類別方法中回傳父 `Array` 物件：

```js
class MyArray extends Array {
  // 將 MyArray species 覆寫為父 Array 建構子
  static get [Symbol.species]() {
    return Array;
  }
}
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`core-js` 中 `Array[Symbol.species]` 的 Polyfill 以及所有受影響的 `Array` 方法中對 `[Symbol.species]` 的支援](https://github.com/zloirock/core-js#ecmascript-array)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Symbol.species")}}
````