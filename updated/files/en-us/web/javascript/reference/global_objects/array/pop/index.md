````markdown
---
title: Array.prototype.pop()
slug: Web/JavaScript/Reference/Global_Objects/Array/pop
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.pop
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`pop()`** 方法會移除陣列的**最後一個**元素，並回傳該元素。此方法會變更陣列的長度。

{{InteractiveExample("JavaScript Demo: Array.prototype.pop()")}}

```js interactive-example
const plants = ["broccoli", "cauliflower", "cabbage", "kale", "tomato"];

console.log(plants.pop());
// Expected output: "tomato"
// 預期輸出：「tomato」

console.log(plants);
// Expected output: Array ["broccoli", "cauliflower", "cabbage", "kale"]
// 預期輸出：陣列 ["broccoli", "cauliflower", "cabbage", "kale"]

plants.pop();

console.log(plants);
// Expected output: Array ["broccoli", "cauliflower", "cabbage"]
// 預期輸出：陣列 ["broccoli", "cauliflower", "cabbage"]
```

## Syntax

```js-nolint
pop()
```

### Parameters

無。

### Return value

從陣列中移除的元素；如果陣列為空，則回傳 {{jsxref("undefined")}}。

## Description

`pop()` 方法會從陣列中移除最後一個元素，並將該值回傳給呼叫者。如果你在空陣列上呼叫 `pop()`，它會回傳 {{jsxref("undefined")}}。

{{jsxref("Array.prototype.shift()")}} 具有與 `pop()` 相似的行為，但應用於陣列中的第一個元素。

`pop()` 方法是一個變異（mutating）方法。它會變更 `this` 的長度和內容。如果你希望 `this` 的值保持不變，但回傳一個移除了最後一個元素的新陣列，則可以使用 [`arr.slice(0, -1)`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/slice) 來代替。

`pop()` 方法是[泛型的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它只需要 `this` 值具有 `length` 屬性和整數鍵屬性。雖然字串也是類陣列（array-like），但此方法不適合應用於它們，因為字串是不可變的（immutable）。

## Examples

### Removing the last element of an array

以下程式碼建立包含四個元素的 `myFish` 陣列，然後移除其最後一個元素。

```js
const myFish = ["angel", "clown", "mandarin", "sturgeon"];

const popped = myFish.pop();

console.log(myFish); // ['angel', 'clown', 'mandarin' ]

console.log(popped); // 'sturgeon'
```

### Calling pop() on non-array objects

`pop()` 方法會讀取 `this` 的 `length` 屬性。如果[標準化的長度](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#normalization_of_the_length_property)為 0，則 `length` 會再次被設為 `0`（而它之前可能是負數或 `undefined`）。否則，位於 `length - 1` 的屬性會被回傳，並[刪除](/zh-TW/docs/Web/JavaScript/Reference/Operators/delete)。

```js
const arrayLike = {
  length: 3,
  unrelated: "foo",
  2: 4,
};
console.log(Array.prototype.pop.call(arrayLike));
// 4
console.log(arrayLike);
// { length: 2, unrelated: 'foo' }

const plainObj = {};
// There's no length property, so the length is 0
// 沒有 length 屬性，所以長度為 0
Array.prototype.pop.call(plainObj);
console.log(plainObj);
// { length: 0 }
```

### Using an object in an array-like fashion

`push` 和 `pop` 是故意設計成泛型的，我們可以利用這一點——如下面的範例所示。

請注意，在這個範例中，我們沒有建立陣列來儲存物件的集合。相反地，我們將集合儲存在物件本身上，並在 `Array.prototype.push` 和 `Array.prototype.pop` 上使用 `call`，來欺騙這些方法，讓它們以為我們正在處理陣列。

```js
const collection = {
  length: 0,
  addElements(...elements) {
    // obj.length will be incremented automatically
    // every time an element is added.
    // 每次添加元素時，obj.length 都會自動遞增。

    // Returning what push returns; that is
    // the new value of length property.
    // 回傳 push 回傳的內容；也就是 length 屬性的新值。
    return [].push.call(this, ...elements);
  },
  removeElement() {
    // obj.length will be decremented automatically
    // every time an element is removed.
    // 每次移除元素時，obj.length 都會自動遞減。

    // Returning what pop returns; that is
    // the removed element.
    // 回傳 pop 回傳的內容；也就是被移除的元素。
    return [].pop.call(this);
  },
};

collection.addElements(10, 20, 30);
console.log(collection.length); // 3
collection.removeElement();
console.log(collection.length); // 2
```

## Specifications

{{Specifications}}

## Browser compatibility

{{Compat}}

## See also

- [Indexed collections](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) guide
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.push()")}}
- {{jsxref("Array.prototype.shift()")}}
- {{jsxref("Array.prototype.unshift()")}}
- {{jsxref("Array.prototype.concat()")}}
- {{jsxref("Array.prototype.splice()")}}
````