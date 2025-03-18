````markdown
---
title: Array.prototype.shift()
slug: Web/JavaScript/Reference/Global_Objects/Array/shift
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.shift
---

{{JSRef}}

**`shift()`** 是 {{jsxref("Array")}} 實例的方法，它會移除陣列的**第一個**元素並回傳該元素。這個方法會改變陣列的長度。

{{InteractiveExample("JavaScript Demo: Array.prototype.shift()")}}

```js interactive-example
const array1 = [1, 2, 3];

const firstElement = array1.shift();

console.log(array1);
// Expected output: Array [2, 3]

console.log(firstElement);
// Expected output: 1
```

## 形式語法

```js-nolint
shift()
```

### 參數

無。

### 回傳值

從陣列中移除的元素；如果陣列為空，則回傳 {{jsxref("undefined")}}。

## 描述

`shift()` 方法會將所有值向左移動 1 位，並將長度減 1，導致第一個元素被移除。如果 {{jsxref("Array/length", "length")}} 屬性為 0，則回傳 {{jsxref("undefined")}}。

{{jsxref("Array/pop", "pop()")}} 方法的行為與 `shift()` 相似，但作用於陣列中的最後一個元素。

`shift()` 方法是一種[變異方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#複製方法與變異方法)。它會改變 `this` 的長度和內容。如果你希望 `this` 的值不變，但回傳一個移除第一個元素的新陣列，則可以使用 [`arr.slice(1)`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/slice) 來代替。

`shift()` 方法是[泛用的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#泛用陣列方法)。它只期望 `this` 值具有 `length` 屬性和整數鍵屬性。雖然字串也類似陣列，但此方法不適合應用於字串，因為字串是不可變的。

## 範例

### 從陣列中移除元素

以下程式碼顯示移除第一個元素前後的 `myFish` 陣列。它也顯示了移除的元素：

```js
const myFish = ["angel", "clown", "mandarin", "surgeon"];

console.log("myFish before:", myFish);
// myFish before: ['angel', 'clown', 'mandarin', 'surgeon']

const shifted = myFish.shift();

console.log("myFish after:", myFish);
// myFish after: ['clown', 'mandarin', 'surgeon']

console.log("Removed this element:", shifted);
// Removed this element: angel
```

### 在 while 迴圈中使用 shift() 方法

`shift()` 方法經常在 while 迴圈的條件中使用。在以下範例中，每次迭代都會從陣列中移除下一個元素，直到陣列為空：

```js
const names = ["Andrew", "Tyrone", "Paul", "Maria", "Gayatri"];

while (typeof (i = names.shift()) !== "undefined") {
  console.log(i);
}
// Andrew, Tyrone, Paul, Maria, Gayatri
```

### 在非陣列物件上呼叫 shift()

`shift()` 方法讀取 `this` 的 `length` 屬性。如果[正規化長度](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#length_屬性的正規化)為 0，則 `length` 會再次被設定為 `0`（而它之前可能是負數或 `undefined`）。否則，索引 `0` 的屬性會被回傳，其餘的屬性則會向左移動一位。索引 `length - 1` 的屬性會被[刪除](/zh-TW/docs/Web/JavaScript/Reference/Operators/delete)，且 `length` 屬性會遞減 1。

```js
const arrayLike = {
  length: 3,
  unrelated: "foo",
  2: 4,
};
console.log(Array.prototype.shift.call(arrayLike));
// undefined, because it is an empty slot
console.log(arrayLike);
// { '1': 4, length: 2, unrelated: 'foo' }

const plainObj = {};
// There's no length property, so the length is 0
Array.prototype.shift.call(plainObj);
console.log(plainObj);
// { length: 0 }
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 教學
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.push()")}}
- {{jsxref("Array.prototype.pop()")}}
- {{jsxref("Array.prototype.unshift()")}}
- {{jsxref("Array.prototype.concat()")}}
- {{jsxref("Array.prototype.splice()")}}
````