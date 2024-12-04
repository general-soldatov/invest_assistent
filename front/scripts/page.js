function addHeader() {
    const header = {
      "Главная": "main",
      "Отчёты": "reports",
      "Календарь": "calendar",
      "Меню": "menu",
      "Настройки": "setting"
    };
    const divHeader = document.getElementsByClassName("topnav")[0];
    for (key in header) {
      let newElement = document.createElement("a");
      newElement.textContent = key;
      newElement.addEventListener("click", function() {
        const active = document.getElementsByClassName("active");
        for (item of active) {
          item.className = "";
        };
        newElement.classList.add("active");
      });
      newElement.addEventListener("click", getMenu.bind(this, header[key]), false)
      newElement.href = "#";
      divHeader.appendChild(newElement);
    };
};

function isFloat(n){
  return Number(n) === n && n % 1 !== 0;
}

async function getEnrollments(dataDB=[], cash=0, tableName = 'coupons', section="reports") {
    const dataJSON = await eel.import_table(section, tableName)();
    const vision = document.getElementById("content");
    vision.innerHTML = '';
    let table = document.createElement("table");
    table.style = "width:100%";
    vision.appendChild(table);
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

};

const menu = {
  "reports": {
        'Купоны': async function() {
          data_coupon = await eel.coupons("купон")();
          getEnrollments(data_coupon[0], data_coupon[1]);
      },
        'Иные доходы': async function() {
          data_coupon = await eel.coupons()();
          getEnrollments(data_coupon[0], data_coupon[1]);
      },
        'Покупки': async function() {
          data_coupon = await eel.transactions('Покупка')();
          getEnrollments(data_coupon[0], data_coupon[1], tableName="transactions");
      },
        'Продажи': async function() {
          data_coupon = await eel.transactions('Продажа')();
          getEnrollments(data_coupon[0], data_coupon[1], tableName="transactions");
      },
      'Облигации': async function() {
        data_coupon = await eel.moex_data()();
        getEnrollments(data_coupon, 0, tableName="bonds");
      },
  },
  "main": {
      'Дашборд': async function() {
        const vision = document.getElementById("content");
        vision.innerHTML = '';
        function data_lans() {
          const divs = document.createElement("div");
          binaryImage(divs);
          vision.appendChild(divs);
        }
        data_lans();
        data_lans();
        data_lans();
        // div_1.style = "float: left";
        // const div_2 = document.createElement("div");
        // binaryImage(div_2);
        // div_2.style = "width: 25%";


        // vision.appendChild(div_2);

      },
      'Портфель': async function() {
        data_coupon = await eel.brief_case()();
        getEnrollments(data_coupon[0], data_coupon[1], tableName="briefcase");
      },
  },
  "calendar": {
      'Ttt': async function() {
        data_coupon = await eel.brief_case()();
        getEnrollments(data_coupon[0], data_coupon[1], tableName="briefcase");
      }
  },
  "menu": {
      'Портd': async function() {
        data_coupon = await eel.brief_case()();
        getEnrollments(data_coupon[0], data_coupon[1], tableName="briefcase");
      }
  },
  "setting": {
      'add': async function() {
        data_coupon = await eel.brief_case()();
        getEnrollments(data_coupon[0], data_coupon[1], tableName="briefcase");
      }
  },
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


async function binaryImage(elem, width='100%') {
  const base64String = await eel.get_image()();
  const imageSrc = `data:image/png;base64,${base64String}`;
  const img = document.createElement('img');
  img.src = imageSrc;
  img.style = `width: ${width}`
  // elem.innerHTML = '';
  elem.appendChild(img);
}

// binaryImage(document.body);