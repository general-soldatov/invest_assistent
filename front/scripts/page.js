const dataJSON = {
  "coupons": {
      "head": {"Date": 15, "Operation": 20, "Name Paper": 45, "Sum": 20},
      "keys": ["date_operation", "type_operation", "name_paper",  "sum_enroll"]
  },
  "transactions": {
      "head": {"Date": 15, "Name Paper": 25, "type_deal": 10, "Price Paper": 20, "Count Paper": 10, "Sum": 20},
      "keys": ["date_deal", "name_paper", "type_deal", "price_paper",  "count_paper", "sum"]
  },
  "bonds": {
      "head": {"Облигация": 20, "Номинал": 10, "Купон": 10, "НКД": 10, "Следующая выплата": 15, "Дата погашения": 15, "Периодичность выплат": 10, "Купонная доходность": 10},
      "keys": ["name_paper", "nominal", "coupon_value", "nkd",  "next_coupon_date", "maturity_date", "coupon_period", "coupon_enroll"]
  }
};

// # print(f'''
//   # Облигация: {short_name}
//   # Идентификатор: {security_id}
//   # Номинал: {nominal}
//   # Купон: {coupon_value}
//   # НКД: {nkd}
//   # ISIN: {isin}
//   # Следующая выплата: {next_coupon_date}
//   # Дата погашения: {maturity_date}
//   # Периодичность выплат: {coupon_period}
//   # ''')

function getEnrollments(dataDB=[], cash=0, tableName = 'coupons') {
    const head = dataJSON[tableName].head;
    const keys = dataJSON[tableName].keys;
    const vision = document.getElementById("content");
    vision.innerHTML = '';
    let table = document.createElement("table");
    table.style = "width:100%"
    vision.appendChild(table);
    let tr = document.createElement("tr");
    table.appendChild(tr);
    for (const key in head) {
      let th = document.createElement("th");
      th.textContent = key;
      th.style = `width: ${head[key]}%`;
      tr.appendChild(th);
    };
    for (item of dataDB) {
      let tr_cikle = document.createElement("tr");
      table.appendChild(tr_cikle);
      for (const key of keys) {
        let td = document.createElement("td");
        td.textContent = item[key];
        tr_cikle.appendChild(td);
      };
    };
    if (cash != 0) {
      let cash_tr = document.createElement("tr");
      cash_tr.innerHTML = `${"<th></th>".repeat(keys.length - 2)}<th>Summary</th><th>${cash}</th>`;
      table.appendChild(cash_tr);
    }

};

function getMenu() {
  const menu = {
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
              }};
  const vision = document.getElementById("menu");
  for (const key in menu) {
      const elem = document.createElement("a");
      elem.innerHTML = `${key}<br>`;
      elem.href = `#${key}`;
      elem.addEventListener("click", menu[key]);
      vision.appendChild(elem);
  };
  };

getMenu()