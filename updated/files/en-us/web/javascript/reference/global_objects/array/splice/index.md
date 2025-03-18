````
---
title: Array.prototype.splice()
slug: Web/JavaScript/Reference/Global_Objects/Array/splice
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.splice
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`splice()`** 方法，藉由移除、替換既有元素及／或加入新元素來改變陣列的內容（[原地](https://en.wikipedia.org/wiki/In-place_algorithm)）。

若要建立一個移除及／或替換部分元素後的新陣列，且不更動到原始陣列，請使用 {{jsxref("Array/toSpliced", "toSpliced()")}}。若要存取陣列的一部分而不修改它，請參見 {{jsxref("Array/slice", "slice()")}}。

{{InteractiveExample("JavaScript Demo: Array.prototype.splice()")}}

```js interactive-example
const months = ["Jan", "March", "April", "June"];
months.splice(1, 0, "Feb");
// 在索引 1 處插入
console.log(months);
// Expected output: Array ["Jan", "Feb", "March", "April", "June"]

months.splice(4, 1, "May");
// 替換索引 4 處的 1 個元素
console.log(months);
// Expected output: Array ["Jan", "Feb", "March", "April", "May"]
```

## 語法

```js-nolint
splice(start)
splice(start, deleteCount)
splice(start, deleteCount, item1)
splice(start, deleteCount, item1, item2)
splice(start, deleteCount, item1, item2, /* …, */ itemN)
```

### 參數

- `start`

  - : 從 0 開始的索引，表示要從哪個位置開始變更陣列，會[轉換為整數](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Number#integer_conversion)。
    - 負數索引會從陣列的尾端開始倒數——如果 `-array.length <= start < 0`，則會使用 `start + array.length`。
    - 如果 `start < -array.length`，則會使用 `0`。
    - 如果 `start >= array.length`，則不會刪除任何元素，但此方法會作為新增函式，並新增所有提供的元素。
    - 如果省略 `start`（且呼叫 `splice()` 時沒有帶任何引數），則不會刪除任何東西。這與傳遞 `undefined` 不同，後者會轉換為 `0`。

- `deleteCount` {{optional_inline}}

  - : 一個整數，表示要從 `start` 移除的陣列元素數量。

    如果省略 `deleteCount`，或其值大於或等於 `start` 指定位置之後的元素數量，則會刪除從 `start` 到陣列結尾的所有元素。但是，如果你希望傳遞任何 `itemN` 參數，則應傳遞 `Infinity` 作為 `deleteCount` 以刪除 `start` 之後的所有元素，因為明確的 `undefined` 會[轉換](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Number#integer_conversion)為 `0`。

    如果 `deleteCount` 為 `0` 或負數，則不會移除任何元素。
    在這種情況下，你應該指定至少一個新元素（見下文）。

- `item1`，…，`itemN` {{optional_inline}}

  - : 要新增到陣列的元素，從 `start` 開始。

    如果你未指定任何元素，則 `splice()` 將只會從陣列中移除元素。

### 回傳值

一個包含已刪除元素的陣列。

如果只移除一個元素，則會回傳一個包含一個元素的陣列。

如果未移除任何元素，則會回傳一個空陣列。

## 描述

`splice()` 方法是一種[變異方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#copying_methods_and_mutating_methods)。它可能會更改 `this` 的內容。如果指定的插入元素數量與要移除的元素數量不同，則陣列的 `length` 也會被更改。同時，它使用 [`[Symbol.species]`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/Symbol.species) 來建立要回傳的新陣列實例。

如果刪除的部分是[稀疏的](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)，則 `splice()` 回傳的陣列也是稀疏的，且那些對應的索引為空槽。

`splice()` 方法是[泛用的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它只期望 `this` 值具有 `length` 屬性和整數鍵屬性。雖然字串也是類陣列，但此方法不適合應用於字串，因為字串是不可變的。

## 範例

### 在索引 2 之前移除 0 個元素，並插入 "drum"

```js
const myFish = ["angel", "clown", "mandarin", "sturgeon"];
const removed = myFish.splice(2, 0, "drum");

// myFish is ["angel", "clown", "drum", "mandarin", "sturgeon"]
// removed is [], no elements removed
```

### 在索引 2 之前移除 0 個元素，並插入 "drum" 和 "guitar"

```js
const myFish = ["angel", "clown", "mandarin", "sturgeon"];
const removed = myFish.splice(2, 0, "drum", "guitar");

// myFish is ["angel", "clown", "drum", "guitar", "mandarin", "sturgeon"]
// removed is [], no elements removed
```

### 在索引 0 處移除 0 個元素，並插入 "angel"

`splice(0, 0, ...elements)` 像 {{jsxref("Array/unshift", "unshift()")}} 一樣在陣列的開頭插入元素。

```js
const myFish = ["clown", "mandarin", "sturgeon"];
const removed = myFish.splice(0, 0, "angel");

// myFish is ["angel", "clown", "mandarin", "sturgeon"]
// no items removed
```

### 在最後一個索引處移除 0 個元素，並插入 "sturgeon"

`splice(array.length, 0, ...elements)` 像 {{jsxref("Array/push", "push()")}} 一樣在陣列的結尾插入元素。

```js
const myFish = ["angel", "clown", "mandarin"];
const removed = myFish.splice(myFish.length, 0, "sturgeon");

// myFish is ["angel", "clown", "mandarin", "sturgeon"]
// no items removed
```

### 移除索引 3 處的 1 個元素

```js
const myFish = ["angel", "clown", "drum", "mandarin", "sturgeon"];
const removed = myFish.splice(3, 1);

// myFish is ["angel", "clown", "drum", "sturgeon"]
// removed is ["mandarin"]
```

### 移除索引 2 處的 1 個元素，並插入 "trumpet"

```js
const myFish = ["angel", "clown", "drum", "sturgeon"];
const removed = myFish.splice(2, 1, "trumpet");

// myFish is ["angel", "clown", "trumpet", "sturgeon"]
// removed is ["drum"]
```

### 從索引 0 開始移除 2 個元素，並插入 "parrot"、"anemone" 和 "blue"

```js
const myFish = ["angel", "clown", "trumpet", "sturgeon"];
const removed = myFish.splice(0, 2, "parrot", "anemone", "blue");

// myFish is ["parrot", "anemone", "blue", "trumpet", "sturgeon"]
// removed is ["angel", "clown"]
```

### 從索引 2 開始移除 2 個元素

```js
const myFish = ["parrot", "anemone", "blue", "trumpet", "sturgeon"];
const removed = myFish.splice(2, 2);

// myFish is ["parrot", "anemone", "sturgeon"]
// removed is ["blue", "trumpet"]
```

### 從索引 -2 移除 1 個元素

```js
const myFish = ["angel", "clown", "mandarin", "sturgeon"];
const removed = myFish.splice(-2, 1);

// myFish is ["angel", "clown", "sturgeon"]
// removed is ["mandarin"]
```

### 移除從索引 2 開始的所有元素

```js
const myFish = ["angel", "clown", "mandarin", "sturgeon"];
const removed = myFish.splice(2);

// myFish is ["angel", "clown"]
// removed is ["mandarin", "sturgeon"]
```

### 在稀疏陣列上使用 splice()

`splice()` 方法會保留陣列的稀疏性。

```js
const arr = [1, , 3, 4, , 6];
console.log(arr.splice(1, 2)); // [empty, 3]
console.log(arr); // [1, 4, empty, 6]
```

### 在非陣列物件上呼叫 splice()

`splice()` 方法會讀取 `this` 的 `length` 屬性。然後，它會根據需要更新整數鍵屬性和 `length` 屬性。

```js
const arrayLike = {
  length: 3,
  unrelated: "foo",
  0: 5,
  2: 4,
};
console.log(Array.prototype.splice.call(arrayLike, 0, 1, 2, 3));
// [ 5 ]
console.log(arrayLike);
// { '0': 2, '1': 3, '3': 4, length: 4, unrelated: 'foo' }
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.concat()")}}
- {{jsxref("Array.prototype.push()")}}
- {{jsxref("Array.prototype.pop()")}}
- {{jsxref("Array.prototype.shift()")}}
- {{jsxref("Array.prototype.slice()")}}
- {{jsxref("Array.prototype.toSpliced()")}}
- {{jsxref("Array.prototype.unshift()")}}
````