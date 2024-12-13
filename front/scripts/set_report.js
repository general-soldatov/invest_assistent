function isFloat(n){
    return Number(n) === n && n % 1 !== 0;
  };

const zip = (a, b) => a.map((k, i) => [k, b[i]]);

class Dashboard {
    constructor() {
      this.dashboard = {
        'money_cb': "Курсы валют ЦБ",
        'my_cash': "Динамика использования собственных средств",
        'enrollments': "Динамика погашений по годам",
        'coupons': "Динамика купонов по годам",
        'get_cash': "Вывод средств со счёта"
      };
    }
    async init() {
      this.data = await eel.get_image()();
    }
    image(dataStr, elem) {
      const img = document.createElement('img');
      img.src = `data:image/png;base64,${dataStr}`;
      img.style = "width:100%";
      elem.appendChild(img);
    }
    async dataFill(elem) {
      await this.init();
      let tab_graph = document.createElement("table");
      tab_graph.id = 'dashboard';
      const dashboardKey = Object.keys(this.dashboard);
      let count = 0;
      while (count < dashboardKey.length) {
        let trImg = document.createElement("tr");
        let trStr = document.createElement("tr");
        for (let j = 0; j < 2; j++) {
          if (count >= dashboardKey.length) {
            break
          }
          const tdImg = document.createElement("td");
          const tdStr = document.createElement("td");
          let dk = dashboardKey[count];
          this.image(this.data[dk], tdImg);
          tdStr.textContent = this.dashboard[dk];
          trImg.appendChild(tdImg);
          trStr.appendChild(tdStr);
          count++;
        };
        tab_graph.appendChild(trImg);
        tab_graph.appendChild(trStr);
      };

      elem.innerHTML = '';
      elem.appendChild(tab_graph);
    }
  };


async function getEnrollments(dataDB=[], cash=0, tableName = 'coupons', section="reports", resetText=true) {
    const dataJSON = await eel.import_table(section, tableName)();
    const vision = document.getElementById("content");
    if (resetText) {
      vision.innerHTML = '';
    }
    let table = document.createElement("table");
    table.style = "width:100%";
    let tr = document.createElement("tr");
    table.appendChild(tr);
    for (const key in dataJSON.head) {
      let th = document.createElement("th");
      th.textContent = key;
      th.style = `width: ${dataJSON.head[key]}%`;
      tr.appendChild(th);
    };
    for (item of dataDB) {
      let tr_cikle = document.createElement("tr");
      table.appendChild(tr_cikle);
      for (const key of dataJSON.keys) {
        let td = document.createElement("td");
        let content = item[key];
        if (isFloat(content)) {
          content = content.toFixed(2);
        }
        td.textContent = content
        tr_cikle.appendChild(td);
      };
    };
    if (cash != 0) {
      let cash_tr = document.createElement("tr");
      if (isFloat(cash)) {
        cash = cash.toFixed(2);
      }
      cash_tr.innerHTML = `${"<th></th>".repeat(dataJSON.keys.length - 2)}<th>Summary</th><th>${cash}</th>`;
      table.appendChild(cash_tr);
    }
    vision.appendChild(table);

};

function getMenu(select) {
    const vision = document.getElementById("menu");
    vision.innerHTML = "";
    for (const key in menu[select]) {
        const elem = document.createElement("button");
        elem.className = "tablinks"
        elem.innerHTML = key;
        elem.href = `#${key}`;
        elem.addEventListener("click", function () {
            const content = document.getElementById("content");
            content.innerHTML = '';
            const div_load = document.createElement("div");
            div_load.className ="spinner";
            content.appendChild(div_load);
            menu[select][key]();
            const tablinks = document.getElementsByClassName("tablinks");
            for (tab of tablinks) {
            tab.className = tab.className.replace(" active", "");
            };
            elem.className += " active";
        });
        vision.appendChild(elem);
    };
    };
