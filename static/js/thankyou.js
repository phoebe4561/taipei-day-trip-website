let url = window.location.href;
let order_numbr = url.split("=")[1];
let order_name = document.querySelector("#order_name");
let order_id = document.querySelector("#order_id");
let status = document.querySelector("#status");
let order_spot = document.querySelector("#order_spot");
let order_photo = document.querySelector("#order_photo");
let order_time = document.querySelector("#order_time");
let order_price = document.querySelector("#order_price");

async function getOrderInfo() {
  let response = await fetch(`/api/order/${order_numbr}`);
  const result = await response.json();
  data = result["data"];
  if (data === null) {
    document.querySelector(".wrong_order").textContent = "訂單編號錯誤";
    document.querySelector(".correct_order").style.display = "none";
  } else {
    order_id.textContent = order_numbr;
    order_spot.textContent = data.trip.attraction.name;
    order_photo.setAttribute("src", data.trip.attraction.image);
    order_time.textContent = data.trip.date + "-" + data.trip.time;
    order_price.textContent = `新台幣${data.price}元`;
    if (data["status"] === 0) {
      status.textContent = "付款成功";
    } else {
      status.textContent = "付款失敗";
    }
  }
}
getOrderInfo();
