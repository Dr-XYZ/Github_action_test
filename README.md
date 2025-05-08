---
title: 使用 DOM 進行網頁與 XML 開發的範例
slug: Web/API/Document_Object_Model/Examples
page-type: guide
---

{{DefaultAPISidebar("DOM")}}

本章提供一些較長的使用 DOM 進行網頁與 XML 開發的範例。在可行情況下，這些範例使用 JavaScript 中常見的 API、技巧及模式來操作 document 物件。

## 範例 1：height 與 width

以下範例展示 `height` 與 `width` 屬性與不同尺寸的圖片一起使用的情況：

```html
<!doctype html>
<html lang="en">
  <head>
    <title>width/height 範例</title>
    <script>
      function init() {
        const arrImages = new Array(3);

        arrImages[0] = document.getElementById("image1");
        arrImages[1] = document.getElementById("image2");
        arrImages[2] = document.getElementById("image3");

        const objOutput = document.getElementById("output");
        let strHtml = "<ul>";

        for (let i = 0; i < arrImages.length; i++) {
          strHtml +=
            "<li>image" +
            (i + 1) +
            ": height=" +
            arrImages[i].height +
            ", width=" +
            arrImages[i].width +
            ", style.height=" +
            arrImages[i].style.height +
            ", style.width=" +
            arrImages[i].style.width +
            "</li>";
        }

        strHtml += "</ul>";

        objOutput.innerHTML = strHtml;
      }
    </script>
  </head>
  <body onload="init();">
    <p>
      圖片 1：無 height、width 或 style
      <img
        id="image1"
        src="[https://www.mozilla.org/images/mozilla-banner.gif](https://www.mozilla.org/images/mozilla-banner.gif)" />
    </p>

    <p>
      圖片 2：height="50"、width="500"，但無 style
      <img
        id="image2"
        src="[https://www.mozilla.org/images/mozilla-banner.gif](https://www.mozilla.org/images/mozilla-banner.gif)"
        height="50"
        width="500" />
    </p>

    <p>
      圖片 3：無 height、width，但 style="height: 50px; width: 500px;"
      <img
        id="image3"
        src="[https://www.mozilla.org/images/mozilla-banner.gif](https://www.mozilla.org/images/mozilla-banner.gif)"
        style="height: 50px; width: 500px;" />
    </p>

    <div id="output"></div>
  </body>
</html>
```

## 範例 2：圖片屬性

```html
<!doctype html>
<html lang="en">
  <head>
    <title>修改圖片邊框</title>

    <script>
      function setBorderWidth(width) {
        document.getElementById("img1").style.borderWidth = width + "px";
      }
    </script>
  </head>

  <body>
    <p>
      <img
        id="img1"
        src="image1.gif"
        style="border: 5px solid green;"
        width="100"
        height="100"
        alt="邊框測試" />
    </p>

    <form name="FormName">
      <input
        type="button"
        value="將邊框設為 20px 寬"
        onclick="setBorderWidth(20);" />
      <input
        type="button"
        value="將邊框設為 5px 寬"
        onclick="setBorderWidth(5);" />
    </form>
  </body>
</html>
```

## 範例 3：操作樣式

在這個簡單的範例中，透過元素上的 style 物件及其 CSS 樣式屬性來存取 HTML 段落元素的某些基本樣式屬性，這些屬性可以從 DOM 中取得並設定。在這個情況下，你是直接操作個別樣式。在下一個範例（參見範例 4）中，你可以使用樣式表及其規則來更改整個文件的樣式。

```html
<!doctype html>
<html lang="en">
  <head>
    <title>更改顏色與字體大小範例</title>

    <script>
      function changeText() {
        const p = document.getElementById("pid");

        p.style.color = "blue";
        p.style.fontSize = "18pt";
      }
    </script>
  </head>
  <body>
    <p id="pid" onclick="window.location.href = '[http://www.cnn.com/](http://www.cnn.com/)';">
      連結器
    </p>

    <form>
      <p><input value="變更" type="button" onclick="changeText();" /></p>
    </form>
  </body>
</html>
```

## 範例 4：使用樣式表

{{domxref("document")}} 物件上的 {{domxref("document.styleSheets", "styleSheets")}} 屬性會回傳載入至該文件的樣式表列表。你可以使用 stylesheet、style 與 {{domxref("CSSRule")}} 物件個別存取這些樣式表及其規則，如本範例所示，它會將所有樣式規則的選擇器印出到控制台。

```js
const ss = document.styleSheets;

for (let i = 0; i < ss.length; i++) {
  for (let j = 0; j < ss[i].cssRules.length; j++) {
    console.log(`${ss[i].cssRules[j].selectorText}\n`);
  }
}
```

對於一個只有一個樣式表且定義了以下三個規則的文件來說：

```css
body {
  background-color: darkblue;
}
p {
  font-family: Arial;
  font-size: 10pt;
  margin-left: 0.125in;
}
#lumpy {
  display: none;
}
```

這個腳本會輸出以下內容：

```plain
BODY
P
#LUMPY
```

## 範例 5：事件傳播

這個範例非常簡單地示範了事件在 DOM 中如何觸發與處理。當這個 HTML 文件的 BODY 載入時，會在 TABLE 的頂部列註冊一個事件監聽器。事件監聽器透過執行 stopEvent 函式來處理事件，該函式會改變表格底部儲存格中的值。

然而，stopEvent 也會呼叫一個事件物件方法 {{domxref("event.stopPropagation")}}，它會阻止事件進一步向上傳播到 DOM。請注意，表格本身有一個 {{domxref("Element.click_event","onclick")}} 事件處理器，當點擊表格時應該顯示訊息。但 stopEvent 方法已經阻止了傳播，所以在表格中的資料更新後，事件階段實際上就結束了，並會顯示一個警示框來確認這點。

```html
<!doctype html>
<html lang="en">
  <head>
    <title>事件傳播</title>

    <style>
      #t-daddy {
        border: 1px solid red;
      }
      #c1 {
        background-color: pink;
      }
    </style>

    <script>
      function stopEvent(event) {
        const c2 = document.getElementById("c2");
        c2.textContent = "hello";

        // 這應該阻止 t-daddy 收到點擊事件。
        event.stopPropagation();
        alert("事件傳播已停止。");
      }

      function load() {
        const elem = document.getElementById("tbl1");
        elem.addEventListener("click", stopEvent, false);
      }
    </script>
  </head>

  <body onload="load();">
    <table id="t-daddy" onclick="alert('hi');">
      <tr id="tbl1">
        <td id="c1">one</td>
      </tr>
      <tr>
        <td id="c2">two</td>
      </tr>
    </table>
  </body>
</html>
```

## 範例 6：getComputedStyle

此範例示範如何使用 {{domxref("window.getComputedStyle")}} 方法來取得未使用 `style` 屬性或 JavaScript（例如 `elt.style.backgroundColor="rgb(173 216 230)"`）設定的元素樣式。後者類型的樣式可以透過更直接的 {{domxref("HTMLElement.style", "elt.style")}} 屬性來取得，其屬性列於 [DOM CSS Properties List](/zh-TW/docs/Web/CSS/Reference)。

`getComputedStyle()` 回傳一個 {{domxref("CSSStyleDeclaration")}} 物件，可以使用此物件的 {{domxref("CSSStyleDeclaration.getPropertyValue()", "getPropertyValue()")}} 方法來參照其個別樣式屬性，如下方範例文件所示。

```html
<!doctype html>
<html lang="en">
  <head>
    <title>getComputedStyle 範例</title>

    <script>
      function cStyles() {
        const RefDiv = document.getElementById("d1");
        const txtHeight = document.getElementById("t1");
        const h_style = document.defaultView
          .getComputedStyle(RefDiv, null)
          .getPropertyValue("height");

        txtHeight.value = h_style;

        const txtWidth = document.getElementById("t2");
        const w_style = document.defaultView
          .getComputedStyle(RefDiv, null)
          .getPropertyValue("width");

        txtWidth.value = w_style;

        const txtBackgroundColor = document.getElementById("t3");
        const b_style = document.defaultView
          .getComputedStyle(RefDiv, null)
          .getPropertyValue("background-color");

        txtBackgroundColor.value = b_style;
      }
    </script>

    <style>
      #d1 {
        margin-left: 10px;
        background-color: rgb(173 216 230);
        height: 20px;
        max-width: 20px;
      }
    </style>
  </head>

  <body>
    <div id="d1">&nbsp;</div>

    <form action="">
      <p>
        <button type="button" onclick="cStyles();">getComputedStyle</button>
        height<input id="t1" type="text" value="1" /> max-width<input
          id="t2"
          type="text"
          value="2" />
        背景顏色<input id="t3" type="text" value="3" />
      </p>
    </form>
  </body>
</html>
```

## 範例 7：顯示事件物件屬性

此範例使用 DOM 方法將 {{domxref("Window.load_event", "onload")}} {{domxref("event")}} 物件的所有屬性及其值顯示在表格中。它也展示了一種使用 [`for...in`](/zh-TW/docs/Web/JavaScript/Reference/Statements/for...in) 迴圈來迭代物件屬性以取得其值的實用技巧。

事件物件的屬性在不同瀏覽器之間差異很大，[WHATWG DOM Standard](https://dom.spec.whatwg.org/) 列出了標準屬性，但許多瀏覽器已大幅擴展了這些屬性。

將以下程式碼放入空白文字檔案中，並在各種瀏覽器中載入它，你會對屬性數量與名稱的差異感到驚訝。你可能也想在頁面中加入一些元素，並從不同的事件處理器中呼叫此函式。

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>顯示事件屬性</title>

    <style>
      table {
        border-collapse: collapse;
      }
      thead {
        font-weight: bold;
      }
      td {
        padding: 2px 10px 2px 10px;
      }

      .odd {
        background-color: #efdfef;
      }
      .even {
        background-color: #ffffff;
      }
    </style>

    <script>
      function showEventProperties(e) {
        function addCell(row, text) {
          const cell = row.insertCell(-1);
          cell.appendChild(document.createTextNode(text));
        }

        const event = e || window.event;
        document.getElementById("eventType").textContent = event.type;

        const table = document.createElement("table");
        const thead = table.createTHead();
        let row = thead.insertRow(-1);
        // 標頭：#, 屬性, 值
        const labelList = ["#", "屬性", "值"];
        const len = labelList.length;

        for (let i = 0; i < len; i++) {
          addCell(row, labelList[i]);
        }

        const tbody = document.createElement("tbody");
        table.appendChild(tbody);

        for (const p in event) {
          row = tbody.insertRow(-1);
          row.className = row.rowIndex % 2 ? "odd" : "even";
          addCell(row, row.rowIndex);
          addCell(row, p);
          addCell(row, event[p]);
        }

        document.body.appendChild(table);
      }

      window.onload = (event) => {
        showEventProperties(event);
      };
    </script>
  </head>

  <body>
    <h1>DOM <span id="eventType"></span> 事件物件的屬性</h1>
  </body>
</html>
```

## 範例 8：使用 DOM Table 介面

DOM {{domxref("HTMLTableElement")}} 介面提供了一些便利方法來建立和操作表格。兩個常用的方法是 {{domxref("HTMLTableElement.insertRow")}} 和 {{domxref("HTMLTableRowElement.insertCell")}}。

若要將列和一些儲存格新增到現有表格：

```html
<table id="table0">
  <tr>
    <td>第 0 列 第 0 儲存格</td>
    <td>第 0 列 第 1 儲存格</td>
  </tr>
</table>

<script>
  const table = document.getElementById("table0");
  const row = table.insertRow(-1);
  let cell;
  let text;

  for (let i = 0; i < 2; i++) {
    cell = row.insertCell(-1);
    // 以下字串將顯示在儲存格中。
    text = "第 " + row.rowIndex + " 列 第 " + i + " 儲存格";
    cell.appendChild(document.createTextNode(text));
  }
</script>
```

### 備註

- 不應使用表格的 {{domxref("element.innerHTML","innerHTML")}} 屬性來修改表格，但你可以使用它來寫入整個表格或儲存格的內容。
- 如果使用 DOM Core 方法 {{domxref("document.createElement")}} 和 {{domxref("Node.appendChild")}} 來建立列和儲存格，IE 要求將它們附加到 {{HTMLElement("tbody")}} 元素，而其他瀏覽器則允許附加到 {{HTMLElement("table")}} 元素（列將新增到最後一個 `<tbody>` 元素）。
- [`HTMLTableElement` 介面](/zh-TW/docs/Web/API/HTMLTableElement#instance_methods)還有許多其他便利方法可用於建立和修改表格。
