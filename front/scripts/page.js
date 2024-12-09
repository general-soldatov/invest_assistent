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
        // data_coupon = await eel.brief_case()();
        // getEnrollments(data_coupon[0], data_coupon[1], tableName="briefcase");
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

async function getForm(nameForm = "transaction") {
  async function transactPy (event) {
    event.preventDefault();
    const elem = formTransaction.dataForm();
    await eel.get_transaction(Array.from(elem))();
  }
  const formTransaction = new TransactionForm (nameForm);

  if (nameForm == "transaction") {
    formTransaction.addTransaction();
  }
  else if (nameForm == "enroll") {
    formTransaction.addEnroll();
  }
  formTransaction.form.addEventListener("submit", transactPy);
}



selectData = {
  "engineer": "Инженер",
  "scientist": "Учёный",
  "psychologist": "Психолог",
  "other": "Другая"
}

class TransactionForm extends FormMaker {

  addTransaction () {
    this.select("Профессия:", "specialization", selectData);
    this.generalInput("Почта:", "email", "email", "email", "elon@musk.com");
    this.button("Report");
    this.integration(idName="content");
  }

  addEnroll () {
    this.select("Профессия:", "specialization", selectData);
    this.generalInput("Почта:", "email", "email", "email", "elon@musk.com");
    this.button("Report");
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

async function dataEventer (event) {
  event.preventDefault();
  // let text = document.createElement('a');
  const elem = formNew.dataForm();
  console.log(Array.from(elem.entries()));
  const filesData = document.getElementById("file_input").files[0];
  const reader = new FileReader();
  reader.readAsArrayBuffer(filesData);
  reader.onload = () => {
        const arrayBuffer = reader.result;
        const uint8Array = new Uint8Array(arrayBuffer);
        const base64String = btoa(String.fromCharCode(...uint8Array));
        eel.get_form(Array.from(elem), base64String)();
    }
  console.log(filesData);

  // Array.from(elem)
  //   .forEach((elem) => {
  //     eel.get_form(elem)()
  // })
  // document.body.appendChild(text);
}

// formNew.form.addEventListener("submit", dataEventer);



// class CashFlowRoot {
//   constructor () {
//     this.content = document.getElementById("content");
//   }

//   transactions () {

//   }
// }