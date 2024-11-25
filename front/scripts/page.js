function getEnrollments(data=[]) {
    const head = {'Date': 15, 'Operation': 20, 'Name Paper': 45, 'Sum': 20};
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
    const keys = ['date_operation', 'type_operation', 'name_paper',  'sum_enroll'];
    for (item of data) {
      let tr_cikle = document.createElement("tr");
      table.appendChild(tr_cikle);
      for (const key of keys) {
        let td = document.createElement("td");
        td.textContent = item[key];
        tr_cikle.appendChild(td);
      };
    };
};

function coupons() {
  const data = [{
      'Date': '12/33/22',
      'Operation': 'Sale',
      'Name Paper': 'OFS',
      'Sum': 332
    },
    {
      'Date': '12/33/22',
      'Operation': 'Sale',
      'Name Paper': 'OFS-7',
      'Sum': 335
    },];
    getEnrollments(data);
};

function enrollments() {
  const data = [{
      'Date': '12/33/22',
      'Operation': 'Sale',
      'Name Paper': 'OFS',
      'Sum': 332
    }];
    getEnrollments(data);
};

function transactions() {
  const data = [{
      'Date': '12/13/21',
      'Operation': 'Market',
      'Name Paper': 'RSHB',
      'Sum': 312
    }];
    getEnrollments(data);
};
