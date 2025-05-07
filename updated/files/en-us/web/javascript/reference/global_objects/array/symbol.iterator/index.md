````markdown
---
title: Array.prototype[Symbol.iterator]()
slug: Web/JavaScript/Reference/Global_Objects/Array/Symbol.iterator
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.@@iterator
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`[Symbol.iterator]()`** 方法實作了 [iterable protocol（可迭代協定）](/zh-TW/docs/Web/JavaScript/Reference/Iteration_protocols)，並允許陣列被大多數需要可迭代物件的語法所使用，例如[展開語法](/zh-TW/docs/Web/JavaScript/Reference/Operators/Spread_syntax)和 {{jsxref("Statements/for...of", "for...of")}} 迴圈。它會回傳一個 [array iterator object（陣列迭代器物件）](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Iterator)，該物件會產生陣列中每個索引的值。

此屬性的初始值與 {{jsxref("Array.prototype.values")}} 屬性的初始值相同。

{{InteractiveExample("JavaScript Demo: Array.prototype[Symbol.iterator]()")}}

```js interactive-example
const array1 = ["a", "b", "c"];
const iterator1 = array1[Symbol.iterator]();

for (const value of iterator1) {
  console.log(value);
}

// Expected output: "a"
// Expected output: "b"
// Expected output: "c"
```

## 形式語法

```js-nolint
array[Symbol.iterator]()
```

### 參數無。

### 回傳值與 {{jsxref("Array.prototype.values()")}} 相同的回傳值：一個新的 [iterable iterator object（可迭代的迭代器物件）](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Iterator)，該物件會產生陣列中每個索引的值。

## 範例

### 使用 for...of 迴圈進行迭代請注意，你很少需要直接呼叫此方法。`[Symbol.iterator]()` 方法的存在使陣列成為 [iterable（可迭代的）](/zh-TW/docs/Web/JavaScript/Reference/Iteration_protocols#the_iterable_protocol)，並且像 `for...of` 迴圈這樣的迭代語法會自動呼叫此方法以取得要迴圈的迭代器。

#### HTML

```html
<ul id="letterResult"></ul>
```

#### JavaScript

```js
const arr = ["a", "b", "c"];
const letterResult = document.getElementById("letterResult");
for (const letter of arr) {
  const li = document.createElement("li");
  li.textContent = letter;
  letterResult.appendChild(li);
}
```

#### 結果

{{EmbedLiveSample("Iteration_using_for...of_loop", "", "")}}

### 手動控制迭代器你仍然可以手動呼叫回傳的迭代器物件的 `next()` 方法，以實現對迭代過程的最大控制。

```js
const arr = ["a", "b", "c", "d", "e"];
const arrIter = arr[Symbol.iterator]();
console.log(arrIter.next().value); // a
console.log(arrIter.next().value); // b
console.log(arrIter.next().value); // c
console.log(arrIter.next().value); // d
console.log(arrIter.next().value); // e
```

### 使用相同函式處理字串和字串陣列由於[strings（字串）](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/String/Symbol.iterator)和陣列都實作了 iterable protocol（可迭代協定），因此可以設計一個通用函式以相同的方式處理這兩種輸入。這比直接呼叫 {{jsxref("Array.prototype.values()")}} 更好，後者要求輸入必須是陣列，或者至少是一個具有此方法的物件。

```js
function logIterable(it) {
  if (typeof it[Symbol.iterator] !== "function") {
    console.log(it, "is not iterable.");
    return;
  }
  for (const letter of it) {
    console.log(letter);
  }
}

// Array（陣列）
logIterable(["a", "b", "c"]);
// a
// b
// c

// String（字串）
logIterable("abc");
// a
// b
// c

// Number（數字）
logIterable(123);
// 123 is not iterable.
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`Array.prototype[Symbol.iterator]` 的 Polyfill 位於 `core-js`](https://github.com/zloirock/core-js#ecmascript-array)
- [Indexed collections（索引集合）](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.keys()")}}
- {{jsxref("Array.prototype.entries()")}}
- {{jsxref("Array.prototype.values()")}}
- [`TypedArray.prototype[Symbol.iterator]()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/Symbol.iterator)
- [`String.prototype[Symbol.iterator]()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/String/Symbol.iterator)
- {{jsxref("Symbol.iterator")}}
- [Iteration protocols（迭代協定）](/zh-TW/docs/Web/JavaScript/Reference/Iteration_protocols)
````