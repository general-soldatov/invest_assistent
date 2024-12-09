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
        data_coupon = await eel.brief_case()();
        getEnrollments(data_coupon[0], data_coupon[1], tableName="briefcase");
      },
      'Добавить доход': async function() {
        data_coupon = await eel.brief_case()();
        getEnrollments(data_coupon[0], data_coupon[1], tableName="briefcase");
      },
      'Добавить вывод со счёта': async function() {
        data_coupon = await eel.brief_case()();
        getEnrollments(data_coupon[0], data_coupon[1], tableName="briefcase");
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


selectData = {
  "engineer": "Инженер",
  "scientist": "Учёный",
  "psychologist": "Психолог",
  "other": "Другая"
}

const formNew = new FormMaker("transaction");
formNew.select("Профессия:", "specialization", selectData);
formNew.generalInput("Почта:", "email", "email", "email", "elon@musk.com");
formNew.generalInput("Pass:", "password", "password", "password");
formNew.generalInput("Text:", "text", "text", "text");
formNew.numberInput("Number:", "number", "num");
formNew.checkbox("Data", "check");
formNew.file("File", "file", "", "image/jpg");
formNew.button("Report");
formNew.integration(idName="formData");

async function dataEventer (event) {
  event.preventDefault();
  // let text = document.createElement('a');
  const elem = formNew.dataForm();
  await eel.get_form(Array.from(elem))();
  // Array.from(elem)
  //   .forEach((elem) => {
  //     eel.get_form(elem)()
  // })
  // document.body.appendChild(text);
}

formNew.form.addEventListener("submit", dataEventer);



// class CashFlowRoot {
//   constructor () {
//     this.content = document.getElementById("content");
//   }

//   transactions () {

//   }
// }