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
}

function getUsername(nameData) {
  const username = document.querySelector(".username");
  username.textContent = nameData.name;
}
