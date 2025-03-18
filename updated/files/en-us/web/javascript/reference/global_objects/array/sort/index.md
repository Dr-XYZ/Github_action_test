````
---
title: Array.prototype.sort()
slug: Web/JavaScript/Reference/Global_Objects/Array/sort
page-type: javascript-instance-method
browser-compat: javascript.builtins.Array.sort
---

{{JSRef}}

{{jsxref("Array")}} 實例的 **`sort()`** 方法會將陣列的元素原地排序（[in place](https://en.wikipedia.org/wiki/In-place_algorithm)），並回傳已排序的同一個陣列的參照。預設的排序順序是遞增，其建立在將元素轉換為字串的基礎上，然後比較它們的 UTF-16 程式碼單元值的序列。

排序的時間和空間複雜度無法保證，因為它取決於實作。

若要在不改變原始陣列的情況下排序陣列中的元素，請使用 {{jsxref("Array/toSorted", "toSorted()")}}。

{{InteractiveExample("JavaScript Demo: Array.prototype.sort()")}}

```js interactive-example
const months = ["March", "Jan", "Feb", "Dec"];
months.sort();
console.log(months);
// Expected output: Array ["Dec", "Feb", "Jan", "March"]

const array1 = [1, 30, 4, 21, 100000];
array1.sort();
console.log(array1);
// Expected output: Array [1, 100000, 21, 30, 4]
```

## 語法

```js-nolint
sort()
sort(compareFn)
```

### 參數

- `compareFn` {{optional_inline}}

  - : 一個決定元素順序的函式。此函式會使用以下引數呼叫：

    - `a`
      - : 第一個用於比較的元素。永遠不會是 `undefined`。
    - `b`
      - : 第二個用於比較的元素。永遠不會是 `undefined`。

    它應該回傳一個數字，其中：

    - 負值表示 `a` 應該在 `b` 之前。
    - 正值表示 `a` 應該在 `b` 之後。
    - 零或 `NaN` 表示 `a` 和 `b` 被認為相等。

    為了記住這一點，請記住 `(a, b) => a - b` 會以遞增順序排序數字。

    如果省略，陣列元素會轉換為字串，然後根據每個字元的 Unicode 程式碼點值進行排序。

### 回傳值

已排序之原始陣列的參照。請注意，該陣列是原地（[in place](https://en.wikipedia.org/wiki/In-place_algorithm)）排序的，且不進行複製。

## 描述

如果未提供 `compareFn`，則所有非 `undefined` 陣列元素都會透過將它們轉換為字串並以 UTF-16 程式碼單元順序比較字串來排序。例如，"banana" 在 "cherry" 之前。在數值排序中，9 在 80 之前，但由於數字會轉換為字串，因此在 Unicode 順序中 "80" 在 "9" 之前。所有 `undefined` 元素都會排序到陣列的末尾。

`sort()` 方法會保留空槽。如果原始陣列是[稀疏陣列](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections#sparse_arrays)，則空槽會移到陣列的末尾，並且永遠在所有 `undefined` 之後。

> [!NOTE]
> 在 UTF-16 中，高於 `\uFFFF` 的 Unicode 字元會被編碼為兩個代理程式碼單元，範圍為 `\uD800` - `\uDFFF`。每個程式碼單元的值會被單獨考慮用於比較。因此，由代理字組 `\uD855\uDE51` 形成的字元將在字元 `\uFF3A` 之前排序。

如果提供了 `compareFn`，則所有非 `undefined` 陣列元素都會根據比較函式的回傳值進行排序（所有 `undefined` 元素都會排序到陣列的末尾，且不呼叫 `compareFn`）。

| `compareFn(a, b)` 回傳值 | 排序順序                         |
| ------------------------------ | ---------------------------------- |
| > 0                            | 將 `a` 排序在 `b` 之後，例如 `[b, a]`  |
| < 0                            | 將 `a` 排序在 `b` 之前，例如 `[a, b]` |
| === 0                          | 保持 `a` 和 `b` 的原始順序 |

因此，比較函式的形式如下：

```js-nolint
function compareFn(a, b) {
  if (a 小於 b（依據某種排序標準）) {
    return -1;
  } else if (a 大於 b（依據排序標準）) {
    return 1;
  }
  // a 必須等於 b
  return 0;
}
```

更正式地說，比較器應具有以下屬性，以確保正確的排序行為：

- _純粹性（Pure）_：比較器不會改變正在比較的物件或任何外部狀態。（這很重要，因為無法保證_何時_以及_如何_呼叫比較器，因此任何特定呼叫都不應對外部產生可見的影響。）
- _穩定性（Stable）_：比較器對同一對輸入回傳相同的結果。
- _自反性（Reflexive）_：`compareFn(a, a) === 0`。
- _反對稱性（Anti-symmetric）_：`compareFn(a, b)` 和 `compareFn(b, a)` 必須都為 `0` 或具有相反的符號。
- _傳遞性（Transitive）_：如果 `compareFn(a, b)` 和 `compareFn(b, c)` 都為正、零或負，則 `compareFn(a, c)` 具有與前兩者相同的正負性。

符合上述約束的比較器將始終能夠回傳 `1`、`0` 和 `-1`，或始終如一地回傳 `0`。例如，如果比較器僅回傳 `1` 和 `0`，或僅回傳 `0` 和 `-1`，它將無法可靠地排序，因為_反對稱性_被破壞。始終回傳 `0` 的比較器將導致陣列根本不被更改，但仍然是可靠的。

預設的詞彙比較器滿足上述所有約束。

若要比較數字而不是字串，比較函式可以從 `a` 中減去 `b`。以下函式將以遞增順序排序陣列（如果它不包含 `NaN`）：

```js
function compareNumbers(a, b) {
  return a - b;
}
```

`sort()` 方法是[泛型的](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array#generic_array_methods)。它僅期望 `this` 值具有 `length` 屬性和整數鍵屬性。雖然字串也是類陣列，但此方法不適合應用於它們，因為字串是不可變的。

## 範例

### 建立、顯示和排序陣列

以下範例建立四個陣列，並顯示原始陣列，然後顯示排序後的陣列。數值陣列在沒有比較函式的情況下排序，然後在使用比較函式的情況下排序。

```js
const stringArray = ["Blue", "Humpback", "Beluga"];
const numberArray = [40, 1, 5, 200];
const numericStringArray = ["80", "9", "700"];
const mixedNumericArray = ["80", "9", "700", 40, 1, 5, 200];

function compareNumbers(a, b) {
  return a - b;
}

stringArray.join(); // 'Blue,Humpback,Beluga'
stringArray.sort(); // ['Beluga', 'Blue', 'Humpback']

numberArray.join(); // '40,1,5,200'
numberArray.sort(); // [1, 200, 40, 5]
numberArray.sort(compareNumbers); // [1, 5, 40, 200]

numericStringArray.join(); // '80,9,700'
numericStringArray.sort(); // ['700', '80', '9']
numericStringArray.sort(compareNumbers); // ['9', '80', '700']

mixedNumericArray.join(); // '80,9,700,40,1,5,200'
mixedNumericArray.sort(); // [1, 200, 40, 5, '700', '80', '9']
mixedNumericArray.sort(compareNumbers); // [1, 5, '9', 40, '80', 200, '700']
```

### 排序物件陣列

物件陣列可以透過比較它們的其中一個屬性的值來排序。

```js
const items = [
  { name: "Edward", value: 21 },
  { name: "Sharpe", value: 37 },
  { name: "And", value: 45 },
  { name: "The", value: -12 },
  { name: "Magnetic", value: 13 },
  { name: "Zeros", value: 37 },
];

// sort by value
items.sort((a, b) => a.value - b.value);

// sort by name
items.sort((a, b) => {
  const nameA = a.name.toUpperCase(); // ignore upper and lowercase
  const nameB = b.name.toUpperCase(); // ignore upper and lowercase
  if (nameA < nameB) {
    return -1;
  }
  if (nameA > nameB) {
    return 1;
  }

  // names must be equal
  return 0;
});
```

### 排序非 ASCII 字元

對於排序具有非 {{Glossary("ASCII")}} 字元的字串，即具有重音符號的字串（e, é, è, a, ä 等），以及來自英語以外語言的字串，請使用 {{jsxref("String.prototype.localeCompare()")}}。此函式可以比較這些字元，以便它們以正確的順序顯示。

```js
const items = ["réservé", "premier", "communiqué", "café", "adieu", "éclair"];
items.sort((a, b) => a.localeCompare(b));

// items is ['adieu', 'café', 'communiqué', 'éclair', 'premier', 'réservé']
```

### 使用 map 排序

`compareFn` 可以在陣列中的每個元素呼叫多次。根據 `compareFn` 的性質，這可能會產生很高的負擔。`compareFn` 執行的工作越多，並且要排序的元素越多，使用 [`map()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/map) 進行排序可能更有效率。這個想法是遍歷陣列一次，以將用於排序的實際值提取到一個臨時陣列中，對臨時陣列進行排序，然後遍歷臨時陣列以實現正確的順序。

```js
// the array to be sorted
const data = ["delta", "alpha", "charlie", "bravo"];

// temporary array holds objects with position and sort-value
const mapped = data.map((v, i) => {
  return { i, value: someSlowOperation(v) };
});

// sorting the mapped array containing the reduced values
mapped.sort((a, b) => {
  if (a.value > b.value) {
    return 1;
  }
  if (a.value < b.value) {
    return -1;
  }
  return 0;
});

const result = mapped.map((v) => data[v.i]);
```

有一個名為 [mapsort](https://github.com/Pimm/mapsort) 的開放原始碼函式庫可用，它應用了這種方法。

### sort() 回傳對同一個陣列的參照

`sort()` 方法會回傳對原始陣列的參照，因此更改回傳的陣列也會更改原始陣列。

```js
const numbers = [3, 1, 4, 1, 5];
const sorted = numbers.sort((a, b) => a - b);
// numbers and sorted are both [1, 1, 3, 4, 5]
sorted[0] = 10;
console.log(numbers[0]); // 10
```

如果你希望 `sort()` 不會更改原始陣列，而是像其他陣列方法（例如 [`map()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/map)）一樣回傳一個[淺複製](/zh-TW/docs/Glossary/Shallow_copy)的陣列，請使用 {{jsxref("Array/toSorted", "toSorted()")}} 方法。或者，你可以在呼叫 `sort()` 之前使用[展開語法](/zh-TW/docs/Web/JavaScript/Reference/Operators/Spread_syntax) 或 [`Array.from()`](/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/from) 進行淺複製。

```js
const numbers = [3, 1, 4, 1, 5];
// [...numbers] creates a shallow copy, so sort() does not mutate the original
const sorted = [...numbers].sort((a, b) => a - b);
sorted[0] = 10;
console.log(numbers[0]); // 3
```

### 排序穩定性

自 10 版（或 ECMAScript 2019）以來，規範規定 `Array.prototype.sort` 是穩定的。

例如，假設你有一個學生名單以及他們的成績。請注意，學生名單已經按字母順序依名稱預先排序：

```js
const students = [
  { name: "Alex", grade: 15 },
  { name: "Devlin", grade: 15 },
  { name: "Eagle", grade: 13 },
  { name: "Sam", grade: 14 },
];
```

在依 `grade` 以遞增順序排序此陣列後：

```js
students.sort((firstItem, secondItem) => firstItem.grade - secondItem.grade);
```

`students` 變數將具有以下值：

```js
[
  { name: "Eagle", grade: 13 },
  { name: "Sam", grade: 14 },
  { name: "Alex", grade: 15 }, // original maintained for similar grade (stable sorting)
  { name: "Devlin", grade: 15 }, // original maintained for similar grade (stable sorting)
];
```

重要的是要注意，具有相同成績的學生（例如，Alex 和 Devlin）將保持與呼叫排序之前相同的順序。這是一個穩定排序演算法保證的。

在 10 版（或 ECMAScript 2019）之前，不保證排序穩定性，這意味著你可能會得到以下結果：

```js
[
  { name: "Eagle", grade: 13 },
  { name: "Sam", grade: 14 },
  { name: "Devlin", grade: 15 }, // original order not maintained
  { name: "Alex", grade: 15 }, // original order not maintained
];
```

### 使用非形式良好的比較器進行排序

如果比較函式不滿足[描述](#description)中解釋的所有純粹性、穩定性、自反性、反對稱性和傳遞性規則，則程式的行為未定義。

例如，考慮以下程式碼：

```js
const arr = [3, 1, 4, 1, 5, 9];
const compareFn = (a, b) => (a > b ? 1 : 0);
arr.sort(compareFn);
```

此處的 `compareFn` 函式不是形式良好的，因為它不滿足反對稱性：如果 `a > b`，它會回傳 `1`；但是透過交換 `a` 和 `b`，它會回傳 `0` 而不是負值。因此，產生的陣列在不同引擎之間會有所不同。例如，V8（由 Chrome、Node.js 等使用）和 JavaScriptCore（由 Safari 使用）根本不會排序陣列，並回傳 `[3, 1, 4, 1, 5, 9]`，而 SpiderMonkey（由 Firefox 使用）將回傳以遞增方式排序的陣列，如 `[1, 1, 3, 4, 5, 9]`。

但是，如果稍微更改 `compareFn` 函式，使其回傳 `-1` 或 `0`：

```js
const arr = [3, 1, 4, 1, 5, 9];
const compareFn = (a, b) => (a > b ? -1 : 0);
arr.sort(compareFn);
```

然後 V8 和 JavaScriptCore 會以遞減方式排序它，如 `[9, 5, 4, 3, 1, 1]`，而 SpiderMonkey 會將其原樣回傳：`[3, 1, 4, 1, 5, 9]`。

由於這種實作不一致性，始終建議你透過遵循五個約束來使你的比較器形式良好。

### 在稀疏陣列上使用 sort()

空槽會移到陣列的末尾。

```js
console.log(["a", "c", , "b"].sort()); // ['a', 'b', 'c', empty]
console.log([, undefined, "a", "b"].sort()); // ["a", "b", undefined, empty]
```

### 在非陣列物件上呼叫 sort()

`sort()` 方法會讀取 `this` 的 `length` 屬性。然後，它會收集 `0` 到 `length - 1` 範圍內的所有現有整數鍵屬性，對它們進行排序，然後將它們寫回。如果範圍內缺少屬性，則會[刪除](/zh-TW/docs/Web/JavaScript/Reference/Operators/delete)相應的尾隨屬性，就好像不存在的屬性已排序到末尾一樣。

```js
const arrayLike = {
  length: 3,
  unrelated: "foo",
  0: 5,
  2: 4,
};
console.log(Array.prototype.sort.call(arrayLike));
// { '0': 4, '1': 5, length: 3, unrelated: 'foo' }
```

## 規範

{{Specifications}}

## 瀏覽器相容性

{{Compat}}

## 參見

- [`core-js` 中具有現代行為（如穩定排序）的 `Array.prototype.sort` 的 Polyfill](https://github.com/zloirock/core-js#ecmascript-array)
- [索引集合](/zh-TW/docs/Web/JavaScript/Guide/Indexed_collections) 指南
- {{jsxref("Array")}}
- {{jsxref("Array.prototype.reverse()")}}
- {{jsxref("Array.prototype.toSorted()")}}
- {{jsxref("String.prototype.localeCompare()")}}
- {{jsxref("TypedArray.prototype.sort()")}}
- [在 v8.dev 上取得 V8 中的排序](https://v8.dev/blog/array-sort) (2018)
- [v8.dev 上的穩定 `Array.prototype.sort`](https://v8.dev/features/stable-sort) (2019)
- Mathias Bynens 的 [`Array.prototype.sort` 穩定性](https://mathiasbynens.be/demo/sort-stability)
````