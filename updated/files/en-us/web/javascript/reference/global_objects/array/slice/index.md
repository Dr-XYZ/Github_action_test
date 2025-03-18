````markdown
---
title: Array.prototype.slice()
slug: Web/JavaScript/Reference/Global_Objects/Array/slice
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.slice
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`slice()`** 方法會回傳陣列一部分的[淺拷貝](/zh-TW/docs/Glossary/Shallow_copy)，並放入一個由 `start` 到 `end` 之間選取的（不含 `end`）新陣列物件，其中 `start` 和 `end` 代表該陣列中項目的索引。原始陣列將不會被修改。

{{InteractiveExample("JavaScript Demo: Array.prototype.slice()", "taller")}}

```js interactive-example
const animals = ["ant", "bison", "camel", "duck", "elephant"];

console.log(animals.slice(2));
// Expected output: Array ["camel", "duck", "elephant"]
// 預期輸出：陣列 ["camel", "duck", "elephant"]

console.log(animals.slice(2, 4));
// Expected output: Array ["camel", "duck"]
// 預期輸出：陣列 ["camel", "duck"]

console.log(animals.slice(1, 5));
// Expected output: Array ["bison", "camel", "duck", "elephant"]
// 預期輸出：陣列 ["bison", "camel", "duck", "elephant"]

console.log(animals.slice(-2));
// Expected output: Array ["duck", "elephant"]
// 預期輸出：陣列 ["duck", "elephant"]

console.log(animals.slice(2, -1));
// Expected output: Array ["camel", "duck"]
// 預期輸出：陣列 ["camel", "duck"]

console.log(animals.slice());
// Expected output: Array ["ant", "bison", "camel", "duck", "elephant"]
// 預期輸出：陣列 ["ant", "bison", "camel", "duck", "elephant"]
```

## 語法

```js-nolint
slice()
slice(start)
slice(start, end)
```

### 參數

- `start` {{optional_inline}}
  - : 從零開始的索引，以此為起點開始提取，[轉換為整數](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Number#integer_conversion)。
    - 負索引從陣列末端開始倒數——如果 `-array.length <= start < 0`，則使用 `start + array.length`。
    - 如果 `start < -array.length` 或 `start` 被省略，則使用 `0`。
    - 如果 `start >= array.length`，則會回傳一個空陣列。
- `end` {{optional_inline}}
  - : 從零開始的索引，以此為起點結束提取，[轉換為整數](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Number#integer_conversion)。`slice()` 提取到 `end` 但不包含 `end`。
    - 負索引從陣列末端開始倒數——如果 `-array.length <= end < 0`，則使用 `end + array.length`。
    - 如果 `end < -array.length`，則使用 `0`。
    - 如果 `end >= array.length` 或 `end` 被省略，則使用 `array.length`，導致提取到最後的所有元素。
    - 如果 `end` 隱含的位置在 `start` 隱含的位置之前或相同，則會回傳一個空陣列。

### 回傳值

包含提取元素的新陣列。

## 描述

`slice()` 方法是一種[複製方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#copying_methods_and_mutating_methods)。它不會改變 `this`，而是回傳一個[淺拷貝](/zh-TW/docs/Glossary/Shallow_copy)，其中包含與原始陣列中相同的某些元素。

`slice()` 方法會保留空槽。如果切片的部分是[稀疏的](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)，則回傳的陣列也是稀疏的。

`slice()` 方法是[泛用的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它只需要 `this` 值具有 `length` 屬性和整數鍵屬性。

## 範例

### 回傳現有陣列的一部分

```js
const fruits = ["Banana", "Orange", "Lemon", "Apple", "Mango"];
const citrus = fruits.slice(1, 3);

// fruits contains ['Banana', 'Orange', 'Lemon', 'Apple', 'Mango']
// fruits 包含 ['Banana', 'Orange', 'Lemon', 'Apple', 'Mango']
// citrus contains ['Orange','Lemon']
// citrus 包含 ['Orange','Lemon']
```

在此範例中，`slice(1, 3)` 提取索引 `1` 到索引 `3` 之間的元素（不包括索引 `3`），從而產生一個新陣列 `['Orange', 'Lemon']`。

### 省略 end 參數

```js
const fruits = ["Apple", "Banana", "Orange", "Mango", "Pineapple"];

const tropical = fruits.slice(2);
console.log(tropical); // ['Orange', 'Mango', 'Pineapple']
```

在此範例中，`slice(2)` 提取索引 `2` 到陣列末端的元素。

### 使用負索引

```js
const fruits = ["Apple", "Banana", "Orange", "Mango", "Pineapple"];

const lastTwo = fruits.slice(-2);
console.log(lastTwo); // ['Mango', 'Pineapple']
```

在此範例中，`slice(-2)` 提取陣列的最後兩個元素。將負索引與 `slice` 方法一起使用時，負索引從陣列的末端開始計數，最後一個元素從 `-1` 開始，倒數第二個元素從 `-2` 開始，依此類推。負索引 `-2` 本身會被包含在內，因為它是提取的起點。

```plain
|     |     |     |     |     |
|  S  |  L  |  I  |  C  |  E  |
|     |     |     |     |     |
  -5    -4    -3    -2    -1

<--- read from reverse
<--- 從反向讀取
```

### 使用正 start 索引和負 end 索引

```js
const fruits = ["Apple", "Banana", "Orange", "Mango", "Pineapple"];

// Using positive start index and negative end index
// 使用正 start 索引和負 end 索引
const sliceExample = fruits.slice(1, -1);
console.log(sliceExample); // ['Banana', 'Orange', 'Mango']
```

在此範例中，`slice(1, -1)` 從索引 `1` 開始提取，並提取到索引 `-1`（即最後一個元素）的元素，但不包含該元素。這會產生一個新陣列 `['Banana', 'Orange', 'Mango']`。`slice` 方法始終排除最終指定索引處的元素，無論它是正數還是負數。

```plain
read from start --->
從頭讀取 --->

   0     1     2     3     4
|     |     |     |     |     |
|  S  |  L  |  I  |  C  |  E  |
|     |     |     |     |     |
  -5    -4    -3    -2    -1

<--- read from reverse
<--- 從反向讀取
```

### 將 slice 與物件陣列一起使用

在以下範例中，`slice` 從 `myCar` 建立一個新陣列 `newCar`。兩者都包含對物件 `myHonda` 的參照。當 `myHonda` 的顏色變更為紫色時，兩個陣列都會反映此變更。

```js
// Using slice, create newCar from myCar.
// 使用 slice，從 myCar 建立 newCar。
const myHonda = {
  color: "red",
  wheels: 4,
  engine: { cylinders: 4, size: 2.2 },
};
const myCar = [myHonda, 2, "cherry condition", "purchased 1997"];
const newCar = myCar.slice(0, 2);

console.log("myCar =", myCar);
console.log("newCar =", newCar);
console.log("myCar[0].color =", myCar[0].color);
console.log("newCar[0].color =", newCar[0].color);

// Change the color of myHonda.
// 變更 myHonda 的顏色。
myHonda.color = "purple";
console.log("The new color of my Honda is", myHonda.color);
// myHonda 的新顏色是 purple

console.log("myCar[0].color =", myCar[0].color);
console.log("newCar[0].color =", newCar[0].color);
```

此腳本會寫入：

```plain
myCar = [
  { color: 'red', wheels: 4, engine: { cylinders: 4, size: 2.2 } },
  2,
  'cherry condition',
  'purchased 1997'
]
newCar = [ { color: 'red', wheels: 4, engine: { cylinders: 4, size: 2.2 } }, 2 ]
myCar[0].color = red
newCar[0].color = red
The new color of my Honda is purple
myHonda 的新顏色是 purple
myCar[0].color = purple
newCar[0].color = purple
```

### 在非陣列物件上呼叫 slice()

`slice()` 方法會讀取 `this` 的 `length` 屬性。然後，它會讀取從 `start` 到 `end` 的整數鍵屬性，並在新建的陣列上定義它們。

```js
const arrayLike = {
  length: 3,
  0: 2,
  1: 3,
  2: 4,
  3: 33, // ignored by slice() since length is 3
  // slice() 會忽略此項，因為 length 為 3
};
console.log(Array.prototype.slice.call(arrayLike, 1, 3));
// [ 3, 4 ]
```

### 使用 slice() 將類陣列物件轉換為陣列

`slice()` 方法通常與 {{jsxref("Function/bind", "bind()")}} 和 {{jsxref("Function/call", "call()")}} 一起使用，以建立一個將類陣列物件轉換為陣列的工具方法。

```js
// slice() is called with `this` passed as the first argument
// 呼叫 slice() 時，會將 `this` 作為第一個引數傳遞
const slice = Function.prototype.call.bind(Array.prototype.slice);

function list() {
  return slice(arguments);
}

const list1 = list(1, 2, 3); // [1, 2, 3]
```

### 在稀疏陣列上使用 slice()

如果來源是稀疏的，則從 `slice()` 回傳的陣列可能是稀疏的。

```js
console.log([1, 2, , 4, 5].slice(1, 4)); // [2, empty, 4]
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`Array.prototype.slice` 的 Polyfill 位於 `core-js`](https://github.com/zloirock/core-js#ecmascript-array)
- [`Array.prototype.slice` 的 es-shims polyfill](https://www.npmjs.com/package/array.prototype.slice)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.pop()")}}
- {{jsxref("Array.prototype.shift()")}}
- {{jsxref("Array.prototype.concat()")}}
- {{jsxref("Array.prototype.splice()")}}
- {{jsxref("TypedArray.prototype.slice()")}}
- {{jsxref("String.prototype.slice()")}}
````