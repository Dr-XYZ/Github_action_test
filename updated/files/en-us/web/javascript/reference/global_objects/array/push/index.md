````markdown
---
title: Array.prototype.push()
slug: Web/JavaScript/Reference/Global_Objects/Array/push
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.push
---

{{JSRef}}

**`push()`** 是 {{jsxref("Array")}} 實例的方法，會將指定的元素加入到陣列的尾端，並回傳陣列的新長度。

{{InteractiveExample("JavaScript Demo: Array.prototype.push()")}}

```js interactive-example
const animals = ["pigs", "goats", "sheep"];

const count = animals.push("cows");
console.log(count);
// Expected output: 4
// 預期輸出：4
console.log(animals);
// Expected output: Array ["pigs", "goats", "sheep", "cows"]
// 預期輸出：陣列 ["pigs", "goats", "sheep", "cows"]

animals.push("chickens", "cats", "dogs");
console.log(animals);
// Expected output: Array ["pigs", "goats", "sheep", "cows", "chickens", "cats", "dogs"]
// 預期輸出：陣列 ["pigs", "goats", "sheep", "cows", "chickens", "cats", "dogs"]
```

## Syntax

```js-nolint
push()
push(element1)
push(element1, element2)
push(element1, element2, /* …, */ elementN)
```

### Parameters

- `element1`, …, `elementN`
  - : 要加到陣列尾端的元素。

### Return value

這個方法被呼叫後，物件的新 {{jsxref("Array/length", "length")}} 屬性。

## Description

`push()` 方法會附加值到陣列。

{{jsxref("Array.prototype.unshift()")}} 的行為與 `push()` 相似，但它是作用於陣列的開頭。

`push()` 方法是個[變異方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#copying_methods_and_mutating_methods)。它會改變 `this` 的長度與內容。如果你希望 `this` 的值維持不變，但回傳一個在尾端附加元素的新陣列，你可以使用 [`arr.concat([element0, element1, /* ... ,*/ elementN])`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/concat) 來替代。請注意，這些元素被包在一個額外的陣列中——否則，如果元素本身就是一個陣列，它會因為 `concat()` 的行為而被展開，而不是作為單一元素被加入。

`push()` 方法是[泛用的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它只預期 `this` 值具有 `length` 屬性以及整數鍵屬性。雖然字串也具有陣列的特性，但此方法不適合應用於字串，因為字串是不可變的。

## Examples

### Adding elements to an array

以下程式碼建立一個包含兩個元素的 `sports` 陣列，然後附加兩個元素到這個陣列。`total` 變數包含陣列的新長度。

```js
const sports = ["soccer", "baseball"];
const total = sports.push("football", "swimming");

console.log(sports); // ['soccer', 'baseball', 'football', 'swimming']
console.log(total); // 4
```

### Merging two arrays

這個範例使用 {{jsxref("Operators/Spread_syntax", "展開語法", "", 1)}} 將第二個陣列的所有元素加入到第一個陣列。

```js
const vegetables = ["parsnip", "potato"];
const moreVegs = ["celery", "beetroot"];

// Merge the second array into the first one
// 將第二個陣列合併到第一個陣列
vegetables.push(...moreVegs);

console.log(vegetables); // ['parsnip', 'potato', 'celery', 'beetroot']
```

合併兩個陣列也可以使用 {{jsxref("Array/concat", "concat()")}} 方法來完成。

### Calling push() on non-array objects

`push()` 方法讀取 `this` 的 `length` 屬性。然後，它會使用傳遞給 `push()` 的引數，從 `length` 開始設定 `this` 的每個索引。最後，它將 `length` 設定為先前的長度加上被加入的元素數量。

```js
const arrayLike = {
  length: 3,
  unrelated: "foo",
  2: 4,
};
Array.prototype.push.call(arrayLike, 1, 2);
console.log(arrayLike);
// { '2': 4, '3': 1, '4': 2, length: 5, unrelated: 'foo' }

const plainObj = {};
// There's no length property, so the length is 0
// 沒有 length 屬性，所以長度為 0
Array.prototype.push.call(plainObj, 1, 2);
console.log(plainObj);
// { '0': 1, '1': 2, length: 2 }
```

### Using an object in an array-like fashion

如上所述，`push` 刻意被設計為泛用的，我們可以善用這個特性。`Array.prototype.push` 可以在物件上正常運作，如下面的範例所示。

請注意，我們沒有建立陣列來儲存物件的集合。取而代之的是，我們將集合儲存在物件本身，並在 `Array.prototype.push` 上使用 `call` 來欺騙這個方法，使它以為我們正在處理陣列——而且它運作得很好，這要歸功於 JavaScript 允許我們以任何我們想要的方式來建立執行上下文。

```js
const obj = {
  length: 0,

  addElem(elem) {
    // obj.length is automatically incremented
    // every time an element is added.
    // 每次加入元素時，obj.length 都會自動遞增。
    [].push.call(this, elem);
  },
};

// Let's add some empty objects just to illustrate.
// 讓我們加入一些空物件來說明。
obj.addElem({});
obj.addElem({});
console.log(obj.length); // 2
```

請注意，雖然 `obj` 不是陣列，但 `push` 方法成功地遞增了 `obj` 的 `length` 屬性，就像我們正在處理實際的陣列一樣。

## Specifications

{{Specifications}}

## Browser compatibility

{{Compat}}

## See also

- [Polyfill of `Array.prototype.push` in `core-js` with fixes of this method](https://github.com/zloirock/core-js#ecmascript-array)
- [es-shims polyfill of `Array.prototype.push`](https://www.npmjs.com/package/array.prototype.push)
- [Indexed collections](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) guide
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.pop()")}}
- {{jsxref("Array.prototype.shift()")}}
- {{jsxref("Array.prototype.unshift()")}}
- {{jsxref("Array.prototype.concat()")}}
- {{jsxref("Array.prototype.splice()")}}
````