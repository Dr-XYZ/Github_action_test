````markdown
---
title: Array.prototype.reduce()
slug: Web/JavaScript/Reference/Global_Objects/Array/reduce
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.reduce
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`reduce()`** 方法會依序針對陣列中的每個元素執行用戶提供的「reducer」回呼函式，傳入前一個元素計算的回傳值。對陣列中的所有元素執行 reducer 後的最終結果會是單一值。

第一次執行回呼時，沒有「先前計算的回傳值」。如果提供 `initialValue`，則可以使用其來取代。否則，索引 0 的陣列元素會用作初始值，且迭代會從下一個元素開始（索引 1 而非索引 0）。

{{InteractiveExample("JavaScript Demo: Array.prototype.reduce()")}}

```js interactive-example
const array1 = [1, 2, 3, 4];

// 0 + 1 + 2 + 3 + 4
const initialValue = 0;
const sumWithInitial = array1.reduce(
  (accumulator, currentValue) => accumulator + currentValue,
  initialValue,
);

console.log(sumWithInitial);
// Expected output: 10
// 預期輸出：10
```

## Syntax

```js-nolint
reduce(callbackFn)
reduce(callbackFn, initialValue)
```

### Parameters

- `callbackFn`
  - : 針對陣列中的每個元素執行的函式。其回傳值會成為下次呼叫 `callbackFn` 時的 `accumulator` 參數值。對於最後一次呼叫，回傳值會成為 `reduce()` 的回傳值。呼叫此函式時會帶有以下引數：
    - `accumulator`
      - : 先前呼叫 `callbackFn` 所產生的值。在第一次呼叫時，如果指定了 `initialValue`，則其值為 `initialValue`；否則其值為 `array[0]`。
    - `currentValue`
      - : 目前元素的值。在第一次呼叫時，如果指定了 `initialValue`，則其值為 `array[0]`；否則其值為 `array[1]`。
    - `currentIndex`
      - : `currentValue` 在陣列中的索引位置。在第一次呼叫時，如果指定了 `initialValue`，則其值為 `0`；否則為 `1`。
    - `array`
      - : 呼叫 `reduce()` 的陣列。
- `initialValue` {{optional_inline}}
  - : 第一次呼叫回呼時，`accumulator` 初始化為的值。
    如果指定了 `initialValue`，則 `callbackFn` 會以陣列中的第一個值作為 `currentValue` 開始執行。
    如果 _未_ 指定 `initialValue`，則 `accumulator` 會初始化為陣列中的第一個值，且 `callbackFn` 會以陣列中的第二個值作為 `currentValue` 開始執行。在這種情況下，如果陣列是空的（因此沒有第一個值可以作為 `accumulator` 回傳），則會擲回錯誤。

### Return value

對整個陣列執行「reducer」回呼函式完成後所產生的值。

### Exceptions

- {{jsxref("TypeError")}}
  - : 如果陣列不包含任何元素且未提供 `initialValue`，則會擲回。

## Description

`reduce()` 方法是一種[迭代方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#iterative_methods)。它會依遞增索引順序對陣列中的所有元素執行「reducer」回呼函式，並將它們累積成單一值。每次，`callbackFn` 的回傳值會作為 `accumulator` 在下一次呼叫時再次傳遞到 `callbackFn` 中。`accumulator` 的最終值（也就是從陣列的最終迭代中 `callbackFn` 回傳的值）會成為 `reduce()` 的回傳值。請閱讀[迭代方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#iterative_methods)章節，以取得更多關於這些方法如何運作的資訊。

只有針對已賦值的陣列索引才會呼叫 `callbackFn`。它不會針對[稀疏陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)中的空插槽呼叫。

與其他[迭代方法](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#iterative_methods)不同，`reduce()` 不接受 `thisArg` 引數。始終使用 `undefined` 作為 `this` 呼叫 `callbackFn`，如果 `callbackFn` 不是嚴格模式，則會將 `undefined` 替換為 `globalThis`。

`reduce()` 是[函數式程式設計](https://en.wikipedia.org/wiki/Functional_programming)中的一個核心概念，在函數式程式設計中，無法變更任何值，因此為了累積陣列中的所有值，必須在每次迭代時回傳一個新的 accumulator 值。此慣例會傳播到 JavaScript 的 `reduce()`：應盡可能使用[展開](/zh-TW/docs/Web/JavaScript/Reference/Operators/Spread_syntax)或其他複製方法來建立新的陣列和物件作為 accumulator，而不是變更現有的陣列或物件。如果你決定變更 accumulator 而不是複製它，請記得仍然在回呼中回傳修改後的物件，否則下一次迭代將會收到 undefined。然而，請注意，複製 accumulator 反而可能導致記憶體使用量增加和效能降低 — 請參閱[何時不使用 reduce()](#when_to_not_use_reduce)以取得更多詳細資訊。在這種情況下，為了避免效能不佳和程式碼難以閱讀，最好改用 `for` 迴圈。

`reduce()` 方法是[泛型](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它只期望 `this` 值具有 `length` 屬性和整數鍵屬性。

### Edge cases

如果陣列只有一個元素（無論位置如何）且未提供 `initialValue`，或者如果提供了 `initialValue` 但陣列為空，則將回傳單獨的值，_而不會_呼叫 `callbackFn`。

如果提供了 `initialValue` 且陣列不為空，則 reduce 方法將始終從索引 0 開始呼叫回呼函式。

如果未提供 `initialValue`，則 reduce 方法對於長度大於 1、等於 1 和 0 的陣列的行為會有所不同，如下面的範例所示：

```js
const getMax = (a, b) => Math.max(a, b);

// callback is invoked for each element in the array starting at index 0
// 回呼會針對陣列中的每個元素（從索引 0 開始）呼叫
[1, 100].reduce(getMax, 50); // 100
[50].reduce(getMax, 10); // 50

// callback is invoked once for element at index 1
// 回呼會針對索引 1 的元素呼叫一次
[1, 100].reduce(getMax); // 100

// callback is not invoked
// 不會呼叫回呼
[50].reduce(getMax); // 50
[].reduce(getMax, 1); // 1

[].reduce(getMax); // TypeError
```

## Examples

### How reduce() works without an initial value

The code below shows what happens if we call `reduce()` with an array and no initial value.

```js
const array = [15, 16, 17, 18, 19];

function reducer(accumulator, currentValue, index) {
  const returns = accumulator + currentValue;
  console.log(
    `accumulator: ${accumulator}, currentValue: ${currentValue}, index: ${index}, returns: ${returns}`,
  );
  return returns;
}

array.reduce(reducer);
```

The callback would be invoked four times, with the arguments and return values in each call being as follows:

|             | `accumulator` | `currentValue` | `index` | Return value |
| ----------- | ------------- | -------------- | ------- | ------------ |
| First call  | `15`          | `16`           | `1`     | `31`         |
| Second call | `31`          | `17`           | `2`     | `48`         |
| Third call  | `48`          | `18`           | `3`     | `66`         |
| Fourth call | `66`          | `19`           | `4`     | `85`         |

The `array` parameter never changes through the process — it's always `[15, 16, 17, 18, 19]`. The value returned by `reduce()` would be that of the last callback invocation (`85`).

### 如何在沒有初始值的情況下使用 reduce()

以下程式碼示範了如果我們使用陣列呼叫 `reduce()` 且沒有初始值會發生什麼事。

```js
const array = [15, 16, 17, 18, 19];

function reducer(accumulator, currentValue, index) {
  const returns = accumulator + currentValue;
  console.log(
    `accumulator: ${accumulator}, currentValue: ${currentValue}, index: ${index}, returns: ${returns}`,
  );
  return returns;
}

array.reduce(reducer);
```

回呼將被呼叫四次，每次呼叫時的引數和回傳值如下：

|             | `accumulator` | `currentValue` | `index` | Return value |
| ----------- | ------------- | -------------- | ------- | ------------ |
| First call  | `15`          | `16`           | `1`     | `31`         |
| Second call | `31`          | `17`           | `2`     | `48`         |
| Third call  | `48`          | `18`           | `3`     | `66`         |
| Fourth call | `66`          | `19`           | `4`     | `85`         |

在整個過程中，`array` 參數永遠不會變更 — 它始終是 `[15, 16, 17, 18, 19]`。`reduce()` 回傳的值將會是最後一次回呼呼叫的值 (`85`)。

### How reduce() works with an initial value

Here we reduce the same array using the same algorithm, but with an `initialValue` of `10` passed as the second argument to `reduce()`:

```js
[15, 16, 17, 18, 19].reduce(
  (accumulator, currentValue) => accumulator + currentValue,
  10,
);
```

The callback would be invoked five times, with the arguments and return values in each call being as follows:

|             | `accumulator` | `currentValue` | `index` | Return value |
| ----------- | ------------- | -------------- | ------- | ------------ |
| First call  | `10`          | `15`           | `0`     | `25`         |
| Second call | `25`          | `16`           | `1`     | `41`         |
| Third call  | `41`          | `17`           | `2`     | `58`         |
| Fourth call | `58`          | `18`           | `3`     | `76`         |
| Fifth call  | `76`          | `19`           | `4`     | `95`         |

The value returned by `reduce()` in this case would be `95`.

### 如何在使用初始值的情況下使用 reduce()

在這裡，我們使用相同的演算法縮減相同的陣列，但將 `initialValue` 設為 `10`，並將其作為第二個引數傳遞給 `reduce()`：

```js
[15, 16, 17, 18, 19].reduce(
  (accumulator, currentValue) => accumulator + currentValue,
  10,
);
```

回呼將被呼叫五次，每次呼叫時的引數和回傳值如下：

|             | `accumulator` | `currentValue` | `index` | Return value |
| ----------- | ------------- | -------------- | ------- | ------------ |
| First call  | `10`          | `15`           | `0`     | `25`         |
| Second call | `25`          | `16`           | `1`     | `41`         |
| Third call  | `41`          | `17`           | `2`     | `58`         |
| Fourth call | `58`          | `18`           | `3`     | `76`         |
| Fifth call  | `76`          | `19`           | `4`     | `95`         |

在這種情況下，`reduce()` 回傳的值將會是 `95`。

### Sum of values in an object array

To sum up the values contained in an array of objects, you **must** supply
an `initialValue`, so that each item passes through your function.

```js
const objects = [{ x: 1 }, { x: 2 }, { x: 3 }];
const sum = objects.reduce(
  (accumulator, currentValue) => accumulator + currentValue.x,
  0,
);

console.log(sum); // 6
```

### 物件陣列中的值總和若要加總物件陣列中包含的值，**必須**提供 `initialValue`，以便每個項目都能傳遞到你的函式中。

```js
const objects = [{ x: 1 }, { x: 2 }, { x: 3 }];
const sum = objects.reduce(
  (accumulator, currentValue) => accumulator + currentValue.x,
  0,
);

console.log(sum); // 6
```

### Function sequential piping

The `pipe` function takes a sequence of functions and returns a new function. When the new function is called with an argument, the sequence of functions are called in order, which each one receiving the return value of the previous function.

```js
const pipe =
  (...functions) =>
  (initialValue) =>
    functions.reduce((acc, fn) => fn(acc), initialValue);

// Building blocks to use for composition
const double = (x) => 2 * x;
const triple = (x) => 3 * x;
const quadruple = (x) => 4 * x;

// Composed functions for multiplication of specific values
const multiply6 = pipe(double, triple);
const multiply9 = pipe(triple, triple);
const multiply16 = pipe(quadruple, quadruple);
const multiply24 = pipe(double, triple, quadruple);

// Usage
multiply6(6); // 36
multiply9(9); // 81
multiply16(16); // 256
multiply24(10); // 240
```

### 函式循序管道

`pipe` 函式會接收一系列函式並回傳一個新的函式。當使用引數呼叫新的函式時，會依序呼叫這一系列函式，每個函式都會接收前一個函式的回傳值。

```js
const pipe =
  (...functions) =>
  (initialValue) =>
    functions.reduce((acc, fn) => fn(acc), initialValue);

// Building blocks to use for composition
// 用於組合的建構區塊
const double = (x) => 2 * x;
const triple = (x) => 3 * x;
const quadruple = (x) => 4 * x;

// Composed functions for multiplication of specific values
// 用於特定值乘法的組合函式
const multiply6 = pipe(double, triple);
const multiply9 = pipe(triple, triple);
const multiply16 = pipe(quadruple, quadruple);
const multiply24 = pipe(double, triple, quadruple);

// Usage
// 用法
multiply6(6); // 36
multiply9(9); // 81
multiply16(16); // 256
multiply24(10); // 240
```

### Running promises in sequence

[Promise sequencing](/zh-TW/docs/Web/JavaScript/Guide/Using_promises#composition) is essentially function piping demonstrated in the previous section, except done asynchronously.

```js
// Compare this with pipe: fn(acc) is changed to acc.then(fn),
// and initialValue is ensured to be a promise
const asyncPipe =
  (...functions) =>
  (initialValue) =>
    functions.reduce((acc, fn) => acc.then(fn), Promise.resolve(initialValue));

// Building blocks to use for composition
const p1 = async (a) => a * 5;
const p2 = async (a) => a * 2;
// The composed functions can also return non-promises, because the values are
// all eventually wrapped in promises
const f3 = (a) => a * 3;
const p4 = async (a) => a * 4;

asyncPipe(p1, p2, f3, p4)(10).then(console.log); // 1200
```

`asyncPipe` can also be implemented using `async`/`await`, which better demonstrates its similarity with `pipe`:

```js
const asyncPipe =
  (...functions) =>
  (initialValue) =>
    functions.reduce(async (acc, fn) => fn(await acc), initialValue);
```

### 依序執行 promise

[Promise 排序](/zh-TW/docs/Web/JavaScript/Guide/Using_promises#composition) 本質上是上一節示範的函式管道，只是以非同步方式完成。

```js
// Compare this with pipe: fn(acc) is changed to acc.then(fn),
// and initialValue is ensured to be a promise
// 將其與 pipe 進行比較：fn(acc) 變更為 acc.then(fn)，
// 並確保 initialValue 是一個 promise
const asyncPipe =
  (...functions) =>
  (initialValue) =>
    functions.reduce((acc, fn) => acc.then(fn), Promise.resolve(initialValue));

// Building blocks to use for composition
// 用於組合的建構區塊
const p1 = async (a) => a * 5;
const p2 = async (a) => a * 2;
// The composed functions can also return non-promises, because the values are
// all eventually wrapped in promises
// 組合函式也可以回傳非 promise，因為這些值最終會包裝在 promise 中
const f3 = (a) => a * 3;
const p4 = async (a) => a * 4;

asyncPipe(p1, p2, f3, p4)(10).then(console.log); // 1200
```

`asyncPipe` 也可以使用 `async`/`await` 實作，這可以更好地示範其與 `pipe` 的相似性：

```js
const asyncPipe =
  (...functions) =>
  (initialValue) =>
    functions.reduce(async (acc, fn) => fn(await acc), initialValue);
```

### Using reduce() with sparse arrays

`reduce()` skips missing elements in sparse arrays, but it does not skip `undefined` values.

```js
console.log([1, 2, , 4].reduce((a, b) => a + b)); // 7
console.log([1, 2, undefined, 4].reduce((a, b) => a + b)); // NaN
```

### 將 reduce() 與稀疏陣列搭配使用

`reduce()` 會跳過稀疏陣列中遺失的元素，但不會跳過 `undefined` 值。

```js
console.log([1, 2, , 4].reduce((a, b) => a + b)); // 7
console.log([1, 2, undefined, 4].reduce((a, b) => a + b)); // NaN
```

### Calling reduce() on non-array objects

The `reduce()` method reads the `length` property of `this` and then accesses each property whose key is a nonnegative integer less than `length`.

```js
const arrayLike = {
  length: 3,
  0: 2,
  1: 3,
  2: 4,
  3: 99, // ignored by reduce() since length is 3
};
console.log(Array.prototype.reduce.call(arrayLike, (x, y) => x + y));
// 9
```

### 在非陣列物件上呼叫 reduce()

`reduce()` 方法會讀取 `this` 的 `length` 屬性，然後存取每個索引鍵為小於 `length` 的非負整數的屬性。

```js
const arrayLike = {
  length: 3,
  0: 2,
  1: 3,
  2: 4,
  3: 99, // ignored by reduce() since length is 3
  // reduce() 忽略，因為長度為 3
};
console.log(Array.prototype.reduce.call(arrayLike, (x, y) => x + y));
// 9
```

### When to not use reduce()

Multipurpose higher-order functions like `reduce()` can be powerful but sometimes difficult to understand, especially for less-experienced JavaScript developers. If code becomes clearer when using other array methods, developers must weigh the readability tradeoff against the other benefits of using `reduce()`.

Note that `reduce()` is always equivalent to a `for...of` loop, except that instead of mutating a variable in the upper scope, we now return the new value for each iteration:

```js
const val = array.reduce((acc, cur) => update(acc, cur), initialValue);

// Is equivalent to:
let val = initialValue;
for (const cur of array) {
  val = update(val, cur);
}
```

As previously stated, the reason why people may want to use `reduce()` is to mimic functional programming practices of immutable data. Therefore, developers who uphold the immutability of the accumulator often copy the entire accumulator for each iteration, like this:

```js example-bad
const names = ["Alice", "Bob", "Tiff", "Bruce", "Alice"];
const countedNames = names.reduce((allNames, name) => {
  const currCount = Object.hasOwn(allNames, name) ? allNames[name] : 0;
  return {
    ...allNames,
    [name]: currCount + 1,
  };
}, {});
```

This code is ill-performing, because each iteration has to copy the entire `allNames` object, which could be big, depending how many unique names there are. This code has worst-case `O(N^2)` performance, where `N` is the length of `names`.

A better alternative is to _mutate_ the `allNames` object on each iteration. However, if `allNames` gets mutated anyway, you may want to convert the `reduce()` to a `for` loop instead, which is much clearer:

```js example-bad
const names = ["Alice", "Bob", "Tiff", "Bruce", "Alice"];
const countedNames = names.reduce((allNames, name) => {
  const currCount = allNames[name] ?? 0;
  allNames[name] = currCount + 1;
  // return allNames, otherwise the next iteration receives undefined
  // 回傳 allNames，否則下一次迭代會收到 undefined
  return allNames;
}, Object.create(null));
```

```js example-good
const names = ["Alice", "Bob", "Tiff", "Bruce", "Alice"];
const countedNames = Object.create(null);
for (const name of names) {
  const currCount = countedNames[name] ?? 0;
  countedNames[name] = currCount + 1;
}
```

Therefore, if your accumulator is an array or an object and you are copying the array or object on each iteration, you may accidentally introduce quadratic complexity into your code, causing performance to quickly degrade on large data. This has happened in real-world code — see for example [Making Tanstack Table 1000x faster with a 1 line change](https://jpcamara.com/2023/03/07/making-tanstack-table.html).

Some of the acceptable use cases of `reduce()` are given above (most notably, summing an array, promise sequencing, and function piping). There are other cases where better alternatives than `reduce()` exist.

- Flattening an array of arrays. Use {{jsxref("Array/flat", "flat()")}} instead.

  ```js example-bad
  const flattened = array.reduce((acc, cur) => acc.concat(cur), []);
  ```

  ```js example-good
  const flattened = array.flat();
  ```

- Grouping objects by a property. Use {{jsxref("Object.groupBy()")}} instead.

  ```js example-bad
  const groups = array.reduce((acc, obj) => {
    const key = obj.name;
    const curGroup = acc[key] ?? [];
    return { ...acc, [key]: [...curGroup, obj] };
  }, {});
  ```

  ```js example-good
  const groups = Object.groupBy(array, (obj) => obj.name);
  ```

- Concatenating arrays contained in an array of objects. Use {{jsxref("Array/flatMap", "flatMap()")}} instead.

  ```js example-bad
  const friends = [
    { name: "Anna", books: ["Bible", "Harry Potter"] },
    { name: "Bob", books: ["War and peace", "Romeo and Juliet"] },
    { name: "Alice", books: ["The Lord of the Rings", "The Shining"] },
  ];
  const allBooks = friends.reduce((acc, cur) => [...acc, ...cur.books], []);
  ```

  ```js example-good
  const allBooks = friends.flatMap((person) => person.books);
  ```

- Removing duplicate items in an array. Use {{jsxref("Set")}} and {{jsxref("Array.from()")}} instead.

  ```js example-bad
  const uniqArray = array.reduce(
    (acc, cur) => (acc.includes(cur) ? acc : [...acc, cur]),
    [],
  );
  ```

  ```js example-good
  const uniqArray = Array.from(new Set(array));
  ```

- Eliminating or adding elements in an array. Use {{jsxref("Array/flatMap", "flatMap()")}} instead.

  ```js example-bad
  // Takes an array of numbers and splits perfect squares into its square roots
  // 接收數字陣列，並將完全平方數分割成其平方根
  const roots = array.reduce((acc, cur) => {
    if (cur < 0) return acc;
    const root = Math.sqrt(cur);
    if (Number.isInteger(root)) return [...acc, root, root];
    return [...acc, cur];
  }, []);
  ```

  ```js example-good
  const roots = array.flatMap((val) => {
    if (val < 0) return [];
    const root = Math.sqrt(val);
    if (Number.isInteger(root)) return [root, root];
    return [val];
  });
  ```

  If you are only eliminating elements from an array, you also can use {{jsxref("Array/filter", "filter()")}}.

- Searching for elements or testing if elements satisfy a condition. Use {{jsxref("Array/find", "find()")}} and {{jsxref("Array/find", "findIndex()")}}, or {{jsxref("Array/some", "some()")}} and {{jsxref("Array/every", "every()")}} instead. These methods have the additional benefit that they return as soon as the result is certain, without iterating the entire array.

  ```js example-bad
  const allEven = array.reduce((acc, cur) => acc && cur % 2 === 0, true);
  ```

  ```js example-good
  const allEven = array.every((val) => val % 2 === 0);
  ```

In cases where `reduce()` is the best choice, documentation and semantic variable naming can help mitigate readability drawbacks.

### 何時不該使用 reduce()

像 `reduce()` 這樣多用途的高階函式可能很強大，但有時難以理解，對於經驗不足的 JavaScript 程式設計師尤其如此。如果在使用的其他陣列方法時，程式碼變得更清晰，則程式設計師必須權衡可讀性的取捨，以及使用 `reduce()` 的其他好處。

請注意，`reduce()` 始終等效於 `for...of` 迴圈，只是我們現在不是變更上層範圍中的變數，而是為每次迭代回傳新的值：

```js
const val = array.reduce((acc, cur) => update(acc, cur), initialValue);

// Is equivalent to:
// 等效於：
let val = initialValue;
for (const cur of array) {
  val = update(val, cur);
}
```

如先前所述，人們可能想要使用 `reduce()` 的原因是為了模仿不可變資料的函數式程式設計實務。因此，堅持 accumulator 不可變性的程式設計師通常會複製整個 accumulator 以進行每次迭代，如下所示：

```js example-bad
const names = ["Alice", "Bob", "Tiff", "Bruce", "Alice"];
const countedNames = names.reduce((allNames, name) => {
  const currCount = Object.hasOwn(allNames, name) ? allNames[name] : 0;
  return {
    ...allNames,
    [name]: currCount + 1,
  };
}, {});
```

此程式碼效能不佳，因為每次迭代都必須複製整個 `allNames` 物件，這可能會很大，取決於有多少個唯一名稱。此程式碼的最差情況效能為 `O(N^2)`，其中 `N` 是 `names` 的長度。

更好的替代方案是在每次迭代時 _變更_ `allNames` 物件。但是，如果 `allNames` 仍然被變更，你可能想要將 `reduce()` 轉換為 `for` 迴圈，這會更清晰：

```js example-bad
const names = ["Alice", "Bob", "Tiff", "Bruce", "Alice"];
const countedNames = names.reduce((allNames, name) => {
  const currCount = allNames[name] ?? 0;
  allNames[name] = currCount + 1;
  // return allNames, otherwise the next iteration receives undefined
  // 回傳 allNames，否則下一次迭代會收到 undefined
  return allNames;
}, Object.create(null));
```

```js example-good
const names = ["Alice", "Bob", "Tiff", "Bruce", "Alice"];
const countedNames = Object.create(null);
for (const name of names) {
  const currCount = countedNames[name] ?? 0;
  countedNames[name] = currCount + 1;
}
```

因此，如果你的 accumulator 是一個陣列或物件，並且你在每次迭代時複製該陣列或物件，你可能會不小心將二次複雜度引入到你的程式碼中，導致效能在大型資料上快速降低。這種情況發生在真實世界的程式碼中 — 例如，請參閱 [Making Tanstack Table 1000x faster with a 1 line change](https://jpcamara.com/2023/03/07/making-tanstack-table.html)。

上面給出了一些 `reduce()` 的可接受使用案例（最值得注意的是，加總陣列、promise 排序和函式管道）。在其他情況下，存在比 `reduce()` 更好的替代方案。

- 扁平化陣列的陣列。請改用 {{jsxref("Array/flat", "flat()")}}。

  ```js example-bad
  const flattened = array.reduce((acc, cur) => acc.concat(cur), []);
  ```

  ```js example-good
  const flattened = array.flat();
  ```

- 按屬性分組物件。請改用 {{jsxref("Object.groupBy()")}}。

  ```js example-bad
  const groups = array.reduce((acc, obj) => {
    const key = obj.name;
    const curGroup = acc[key] ?? [];
    return { ...acc, [key]: [...curGroup, obj] };
  }, {});
  ```

  ```js example-good
  const groups = Object.groupBy(array, (obj) => obj.name);
  ```

- 連接包含在物件陣列中的陣列。請改用 {{jsxref("Array/flatMap", "flatMap()")}}。

  ```js example-bad
  const friends = [
    { name: "Anna", books: ["Bible", "Harry Potter"] },
    { name: "Bob", books: ["War and peace", "Romeo and Juliet"] },
    { name: "Alice", books: ["The Lord of the Rings", "The Shining"] },
  ];
  const allBooks = friends.reduce((acc, cur) => [...acc, ...cur.books], []);
  ```

  ```js example-good
  const allBooks = friends.flatMap((person) => person.books);
  ```

- 移除陣列中的重複項目。請改用 {{jsxref("Set")}} 和 {{jsxref("Array.from()")}}。

  ```js example-bad
  const uniqArray = array.reduce(
    (acc, cur) => (acc.includes(cur) ? acc : [...acc, cur]),
    [],
  );
  ```

  ```js example-good
  const uniqArray = Array.from(new Set(array));
  ```

- 消除或新增陣列中的元素。請改用 {{jsxref("Array/flatMap", "flatMap()")}}。

  ```js example-bad
  // Takes an array of numbers and splits perfect squares into its square roots
  // 接收數字陣列，並將完全平方數分割成其平方根
  const roots = array.reduce((acc, cur) => {
    if (cur < 0) return acc;
    const root = Math.sqrt(cur);
    if (Number.isInteger(root)) return [...acc, root, root];
    return [...acc, cur];
  }, []);
  ```

  ```js example-good
  const roots = array.flatMap((val) => {
    if (val < 0) return [];
    const root = Math.sqrt(val);
    if (Number.isInteger(root)) return [root, root];
    return [val];
  });
  ```

  If you are only eliminating elements from an array, you also can use {{jsxref("Array/filter", "filter()")}}.
  如果你只是要從陣列中消除元素，你也可以使用 {{jsxref("Array/filter", "filter()")}}。

- 搜尋元素或測試元素是否滿足條件。請改用 {{jsxref("Array/find", "find()")}} 和 {{jsxref("Array/find",