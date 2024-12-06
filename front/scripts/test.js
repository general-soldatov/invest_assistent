class Dashboard {
    constructor() {
      this.dashboard = {
        'my_cash': "Динамика использования собственных средств",
        'transactions': "Динамика транзакций по годам",
        // 'coupons': "Динамика прихода купонов"
      };
    }
    // async init() {
    //   this.data = await eel.get_image()();
    // }

    image(base64str, elem) {
      const imageSrc = `data:image/png;base64,${base64str}`;
      const img = document.createElement('img');
      img.src = imageSrc;
      img.style = `width: ${width}`;
      elem.appendChild(img);
    };

    async dataFill(elem) {
      // await this.init();
      // let tab_graph = document.createElement("table");
      const dashboardKey = Object.keys(this.dashboard);
    //   console.log(dashboardKey);
      let count = 0;
      while (count < dashboardKey.length) {
      //   let trImg = document.createElement("tr");
      //   let trStr = document.createElement("tr");
      //   for (let j = 0; j < 2; j++) {
      //     const tdImg = document.createElement("td");
      //     const tdStr = document.createElement("td");
          // let dk = dashboardKey[count];
      //     this.image(this.data[dk], tdImg);
      //     tdStr.textContent = this.dashboard[dk];
      //     trImg.appendChild(tdImg);
      //     trStr.appendChild(tdStr);
            console.log(count);
          count++;
      //   };
      //   tab_graph.appendChild(trImg);
      //   tab_graph.appendChild(trStr);
      }

    //   elem.innerHTML = dashboardKey[0];
      // elem.appendChild(tab_graph);
    }
  }

  const db = new Dashboard();
  db.dataFill()