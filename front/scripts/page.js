function addHeader() {
    const header = {
      "Главная": "main",
      "Отчёты": "reports",
      "Операции": "operation",
      "Меню": "menu",
      "Настройки": "setting"
    };
    const divHeader = document.getElementsByClassName("topnav")[0];
    for (key in header) {
      let newElement = document.createElement("a");
      newElement.textContent = key;
      newElement.id = 'data_' + header[key];
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
        const db = new Dashboard();
        const vision = document.getElementById("content");
        await db.dataFill(vision);
      },
      'Портфель': async function() {
        data_coupon = await eel.brief_case()();
        getEnrollments(data_coupon[0], data_coupon[1], tableName="briefcase");
      },
  },
  "operation": {
      'Добавить сделку': async function() {
        await getForm("transaction");
      },
      'Добавить доход': async function() {
        await getForm("enroll");
      },
      'Добавить вывод со счёта': async function() {
        await getForm("write-down");
      },
      'Анализ отчёта брокера': async function() {
        await getForm("report");
      },
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

async function dataTableReport(lstData) {
  const nameTables = {
    "cash-flow": "Денежный поток за период",
    "delay-data": "Сделки купли/продажи",
    "security": "Справочник бумаг"
  };
  const vision = document.getElementById("content");
  for (item of zip(Object.keys(nameTables), lstData)) {
    const nameTable = document.createElement('p');
    nameTable.textContent = nameTables[item[0]];
    vision.appendChild(nameTable);
    await getEnrollments(item[1], 0, item[0], "parse", false);
  }
}

async function getForm(nameForm = "transaction") {
  async function transactPy (event) {
    event.preventDefault();
    const elem = formTransaction.dataForm();
    if (nameForm == "report") {
      const reader = new FileReader();
      const inputFile = elem.get('file');
      reader.readAsText(inputFile);
      const content = document.getElementById('content');
      reader.onload = () => {
            let lst = eel.get_transaction(reader.result, nameForm)();
            lst.then(
              result => dataTableReport(result), // Данные загружены
              error => console.log(error) // Выполнено не будет
            )
        }
    }
    else {
      await eel.get_transaction(Array.from(elem), nameForm)();
      alert("Информация успешно добавлена!");
    }
  }
  const formTransaction = new TransactionForm(nameForm);

  if (nameForm == "transaction") {
    formTransaction.addTransaction();
  }
  else if (nameForm == "enroll") {
    formTransaction.addEnroll();
  }
  else if (nameForm == "write-down") {
    formTransaction.addDownCash();
  }
  else if (nameForm == "report") {
    formTransaction.addReport();
  }
  formTransaction.form.addEventListener("submit", transactPy);
}

type_operation = {
  "purchase": "Покупка",
  "sales": "Продажа"
}

enroll = {
  'coupon': 'купон',
  'depreciation': 'амортизация',
  'repayment': 'погашение',
  'dividends': 'дивиденды'
}

downCash = {
  'Списание д/с': 'Списание д/с'
}

class TransactionForm extends FormMaker {

  async addTransaction () {
    this.select("Тип сделки:", "type_deal", type_operation);
    const papers = await eel.get_papers()();
    this.select("Бумага:", "name_paper", papers);
    this.generalInput("Дата:", "date_deal", "date", {typeInput: "date"});
    this.numberInput("Количество", "count_paper", "count_paper", {step: 1});
    this.numberInput("Цена, руб:", "price_paper", "price_paper", {step: 0.01});
    this.numberInput("НКД, руб:", "coupon_add_paper", "coupon_add_paper", {step: 0.01});
    this.numberInput("Комиссия брокера, %:", "broker_comission", "broker_comission", {step: 0.01, value: 0.03});
    this.numberInput("Комиссия биржи, %:", "market_comission", "market_comission", {step: 0.001, value: 0.014});
    this.button("Добавить сделку");
    this.integration(idName="content");
  }

  async addEnroll () {
    this.select("Тип дохода:", "type_operation", enroll);
    const papers = await eel.get_papers()();
    this.select("Бумага:    ", "name_paper", papers);
    this.generalInput("Дата:      ", "date_operation", "date", {typeInput:"date"});
    this.numberInput("Сумма:     ", "sum_enroll", "sum_enroll", {step: 0.01});
    this.button("Добавить доход");
    this.integration(idName="content");
  }

  addDownCash () {
    this.select("Тип списания:", "operation", downCash);
    this.generalInput("Дата:", "date_operation", "date", {typeInput:"date"});
    this.numberInput("Сумма:", "sum_enroll", "sum_enroll", {step: 0.01});
    this.button("Добавить операцию");
    this.integration(idName="content");
  }

  addReport () {
    this.file("Отчёт брокера: ", "file", "file_input", ".html");
    this.button("Анализ отчёта");
    this.integration(idName="content");
  }

}



const formNew = new FormMaker("transaction");
// formNew.

// formNew.generalInput("Pass:", "password", "password", "password");
// formNew.generalInput("Text:", "text", "text", "text");
// formNew.numberInput("Number:", "number", "num");
// formNew.checkbox("Data", "check");
// formNew.file("File", "file", "file_input", "image/jpg");
// formNew.button("Report");
formNew.integration(idName="formData");

// async function dataEventer (event) {
//   event.preventDefault();
//   // let text = document.createElement('a');
//   const elem = formNew.dataForm();
//   console.log(Array.from(elem.entries()));
//   const filesData = document.getElementById("file_input").files[0];
//   const reader = new FileReader();
//   reader.readAsArrayBuffer(filesData);
//   reader.onload = () => {
//         const arrayBuffer = reader.result;
//         const uint8Array = new Uint8Array(arrayBuffer);
//         const base64String = btoa(String.fromCharCode(...uint8Array));
//         eel.get_form(Array.from(elem), base64String)();
//     }
//   console.log(filesData);

  // Array.from(elem)
  //   .forEach((elem) => {
  //     eel.get_form(elem)()
  // })
  // document.body.appendChild(text);
// }

// formNew.form.addEventListener("submit", dataEventer);



// class CashFlowRoot {
//   constructor () {
//     this.content = document.getElementById("content");
//   }

//   transactions () {

//   }
// }