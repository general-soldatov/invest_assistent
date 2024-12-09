class FormMaker {
    constructor (idForm, classNameForm="form") {
      this.form = document.createElement('form');
      this.form.className = classNameForm;
      this.form.id = idForm;
    }

    integration (idName = 'content') {
      const vision = document.getElementById(idName);
      vision.innerHTML = '';
      vision.appendChild(this.form);
    }

    dataForm () {
      return new FormData(this.form);
    }

    generalInput (labelName, nameInput, idInput,
                  typeInput="text", placeInput="", elem=null) {
      let label = document.createElement('label');
      label.textContent = labelName + " ";
      let input = document.createElement('input');
      input.name = nameInput;
      input.id = idInput;
      input.type = typeInput;
      input.placeholder = placeInput;
      label.appendChild(input);
      if (elem) {
        elem.appendChild(label);
      }
      else {
        this.form.appendChild(label);
      }
    }

    numberInput (labelName, nameInput, idInput, elem=null) {
      let label = document.createElement('label');
      label.textContent = labelName + " ";
      let input = document.createElement('input');
      input.name = nameInput;
      input.id = idInput;
      input.type = "number";
      label.appendChild(input);
      if (elem) {
        elem.appendChild(label);
      }
      else {
        this.form.appendChild(label);
      }
    }

    checkbox (labelName, nameInput, idInput, elem=null) {
      let label = document.createElement('label');
      label.textContent = labelName + " ";
      let input = document.createElement('input');
      input.name = nameInput;
      input.id = idInput;
      input.value = 1;
      input.type = "checkbox";
      label.appendChild(input);
      if (elem) {
        elem.appendChild(label);
      }
      else {
        this.form.appendChild(label);
      }
    }

    file (labelName, nameInput, idInput,
           acceptInput, elem=null) {
      let label = document.createElement('label');
      label.textContent = labelName + " ";
      let input = document.createElement('input');
      input.name = nameInput;
      input.id = idInput;
      input.accept = acceptInput;
      input.type = "file";
      label.appendChild(input);
      if (elem) {
        elem.appendChild(label);
      }
      else {
        this.form.appendChild(label);
      }
    }

    select (labelName, nameSelect, data, elem = null) {
      let label = document.createElement('label');
      label.textContent = labelName + " ";
      let select = document.createElement('select');
      select.name = nameSelect;
      for (let key in data) {
        const option = document.createElement('option');
        option.value = key;
        option.textContent = data[key];
        select.appendChild(option);
      }
      label.appendChild(select);
      if (elem) {
        elem.appendChild(label);
      }
      else {
        this.form.appendChild(label);
      }
    }

    button (nameButton, funcButton=null, elem=null) {
      let button = document.createElement('input');
      button.type = "submit";
      button.textContent = nameButton;
      if (funcButton) {
        button.addEventListener("click", funcButton);
      }
      if (elem) {
        elem.appendChild(button);
      }
      else {
        this.form.appendChild(button);
      }
    }

  }
