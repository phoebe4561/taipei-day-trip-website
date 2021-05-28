async function deleteOrder() {
  let response = await fetch("/api/booking", {
    method: "DELETE",
  });
  let res = await response.json();
  if (res["ok"]) {
    ShowNoOrder();
  }
}

function clickDeleteBtn() {
  let trushBtn = document.querySelector(".trushBtn");
  trushBtn.addEventListener("click", () => {
    deleteOrder();
  });
}
clickDeleteBtn();

async function loadOrderInfo() {
  let response = await fetch("/api/booking");
  const result = await response.json();
  data = result["data"];
  console.log(data);
  if (data === null) {
    ShowNoOrder();
  } else {
    // console.log(data);
    getOrderData(data);
    clickPayBtn();
  }
}
loadOrderInfo();

async function loadUsername() {
  let response = await fetch("/api/user");
  const result = await response.json();
  nameData = result["data"];
  if (nameData === null) {
    location.href = "/";
  } else {
    console.log(nameData);
    getUsername(nameData);
  }
}
loadUsername();

function ShowNoOrder() {
  const no_order = document.querySelector("#no_order");
  const ok_order = document.querySelector(".ok_order");

  no_order.textContent = "您目前沒有任何待預定的行程";
  ok_order.style.display = "none";
}

function getOrderData(data) {
  const spotPic = document.querySelector("#spotPic");
  const spotName = document.querySelector("#spotName");
  const spotDate = document.querySelector("#spotDate");
  const spotTime = document.querySelector("#spotTime");
  const spotCost = document.querySelectorAll("#spotCost");
  const spotAddress = document.querySelector("#spotAddress");
  spotCost.forEach((price) => {
    price.textContent = "新台幣" + data.price + "元";
  });
  spotName.textContent = data.attraction.name;
  spotDate.textContent = data.date;
  spotAddress.textContent = data.attraction.address;
  spotPic.setAttribute("src", data.attraction.image);
  if (data.time === "morning") {
    spotTime.textContent = "上午9點至上午12點";
  } else {
    spotTime.textContent = "下午2點至下午5點";
  }
  attraction_order = {
    price: data.price,
    trip: {
      attraction: data.attraction,
      date: data.date,
      time: data.time,
    },
  };
}

function getUsername(nameData) {
  const username = document.querySelector(".username");
  username.textContent = nameData.name;
  pay_name.value = nameData.name;
  pay_email.value = nameData.email;
}

//tappay前端串接
TPDirect.setupSDK(
  20395,
  "app_RgcnRhOpeyThaxUl9Zwl9BiDoFaqpevTT7bogC0y4YaCdo0AWm8UBbpVbUsB",
  "sandbox"
);

TPDirect.card.setup({
  fields: {
    number: {
      element: "#card-number",
      placeholder: "**** **** **** ****",
    },
    expirationDate: {
      element: document.getElementById("card-expiration-date"),
      placeholder: "MM / YY",
    },
    ccv: {
      element: "#card-ccv",
      placeholder: "後三碼",
    },
  },
  styles: {
    input: {
      color: "gray",
    },
    "input.card-number": {
      // color: "black",
    },
    "input.ccv": {
      // color: "black",
    },
    "input.expiration-date": {
      // color: "black",
    },
    ":focus": {
      // 'color': 'black'
    },
    ".valid": {
      color: "green",
    },
    ".invalid": {
      color: "red",
    },
    "@media screen and (max-width: 400px)": {
      input: {
        color: "black",
      },
    },
  },
});

function clickPayBtn() {
  const payBtn = document.querySelector(".payBtn");
  payBtn.addEventListener("click", (e) => {
    e.preventDefault();

    // console.log(attraction_order);
    //get Prime
    TPDirect.card.getPrime(function (result) {
      if (result.status !== 0) {
        console.log("getPrime error");
        document.querySelector(".pay_error_msg").textContent =
          "請填入正確信用卡付款資訊";
        return;
      }

      let prime = result.card.prime;
      let order_data = {
        prime: prime,
        order: {
          price: attraction_order.price,
          trip: attraction_order.trip,
          contact: {
            name: document.querySelector("#pay_name").value,
            email: document.querySelector("#pay_email").value,
            phone: document.querySelector("#pay_phone").value,
          },
        },
      };
      fetch("/api/orders", {
        body: JSON.stringify(order_data),
        headers: {
          "content-type": "application/json",
        },
        method: "POST",
      })
        .then((response) => {
          return response.json();
        })
        .then((res) => {
          // console.log(res.data.number);
          if (res["error"]) {
            document.querySelector(".pay_error_msg").textContent =
              res["message"];
          } else {
            window.location.href = `/thankyou?number=${res.data.number}`;
          }
        });
    });
  });
}
