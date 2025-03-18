````
---
title: "Array: length"
slug: Web/JavaScript/Reference/Global_Objects/Array/length
page-type: javascript-instance-data-property
browser-compat: javascript.builtins.Array.length
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`length`** 資料屬性代表該陣列中的元素數量。此值是一個無符號的 32 位元整數，其數值總是比陣列中最高的索引值還要大。

{{InteractiveExample("JavaScript Demo: Array: length", "shorter")}}

```js interactive-example
const clothing = ["shoes", "shirts", "socks", "sweaters"];

console.log(clothing.length);
// Expected output: 4
```

## Value

一個小於 2<sup>32</sup> 的非負整數。

{{js_property_attributes(1, 0, 0)}}

## Description

`length` 屬性的值是一個小於 2<sup>32</sup> 的非負整數。

```js
const listA = [1, 2, 3];
const listB = new Array(6);

console.log(listA.length);
// 3

console.log(listB.length);
// 6

listB.length = 2 ** 32; // 4294967296
// RangeError: Invalid array length

const listC = new Array(-100); // Negative numbers are not allowed
// RangeError: Invalid array length
```

陣列物件會觀察 `length` 屬性，並自動將 `length` 值與陣列的內容同步。這表示：

- 將 `length` 設定為小於目前長度的值會截斷陣列——超出新 `length` 的元素會被刪除。
- 設定任何超出目前 `length` 的陣列索引（小於 2<sup>32</sup> 的非負整數）會擴展陣列——`length` 屬性會增加以反映新的最高索引。
- 將 `length` 設定為無效值（例如，負數或非整數）會拋出 `RangeError` 例外。

當 `length` 被設定為大於目前長度的值時，陣列會通過新增[空插槽](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)來擴展，而不是實際的 `undefined` 值。空插槽與陣列方法有一些特殊的互動；參見[陣列方法與空插槽](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#array_methods_and_empty_slots)。

```js
const arr = [1, 2];
console.log(arr);
// [ 1, 2 ]

arr.length = 5; // set array length to 5 while currently 2.
console.log(arr);
// [ 1, 2, <3 empty items> ]

arr.forEach((element) => console.log(element));
// 1
// 2
```

另請參閱 [`length` 與數值屬性之間的關係](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#relationship_between_length_and_numerical_properties)。

## Examples

### 迭代陣列

在以下範例中，陣列 `numbers` 通過查看 `length` 屬性進行迭代。然後將每個元素中的值加倍。

```js
const numbers = [1, 2, 3, 4, 5];
const length = numbers.length;
for (let i = 0; i < length; i++) {
  numbers[i] *= 2;
}
// numbers is now [2, 4, 6, 8, 10]
```

### 縮短陣列

如果目前長度大於 3，則以下範例將陣列 `numbers` 縮短為長度 3。

```js
const numbers = [1, 2, 3, 4, 5];

if (numbers.length > 3) {
  numbers.length = 3;
}

console.log(numbers); // [1, 2, 3]
console.log(numbers.length); // 3
console.log(numbers[3]); // undefined; the extra elements are deleted
```

### 建立固定長度的空陣列

將 `length` 設定為大於目前長度的值會建立一個[稀疏陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)。

```js
const numbers = [];
numbers.length = 3;
console.log(numbers); // [empty x 3]
```

### 具有不可寫入長度的陣列

當元素被新增到超出目前長度時，陣列會自動更新 `length` 屬性。如果 `length` 屬性被設定為不可寫入，則陣列將無法更新它。這會在[嚴格模式](/zh-TW/docs/Web/JavaScript/Reference/Strict_mode)中導致錯誤。

```js
"use strict";

const numbers = [1, 2, 3, 4, 5];
Object.defineProperty(numbers, "length", { writable: false });
numbers[5] = 6; // TypeError: Cannot assign to read only property 'length' of object '[object Array]'
numbers.push(5); // // TypeError: Cannot assign to read only property 'length' of object '[object Array]'
```

## Specifications

{{Specifications}}

## Browser compatibility

{{Compat}}

## See also

- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- [`TypedArray.prototype.length`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/length)
- [`String`: `length`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/String/length)
- [RangeError: invalid array length](/zh-TW/docs/Web/JavaScript/Reference/Errors/Invalid_array_length)
````