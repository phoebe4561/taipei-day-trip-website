let url = location.href.split("/");
let id = url[url.length - 1];
let error_message = document.querySelector(".error_message");

let index = 1;
async function loadAttractionId() {
  let response = await fetch("/api/attraction/" + id);
  let result = await response.json();
  data = result["data"];
  let imgArr = data.images;

  getImages(imgArr);
  getData();
  showImage();
  changeMoney();

  let leftBtn = document.querySelector(".leftBtn");
  leftBtn.addEventListener("click", () => {
    changeImage(-1);
  });

  let rightBtn = document.querySelector(".rightBtn");
  rightBtn.addEventListener("click", () => {
    changeImage(1);
  });

  let dot = document.querySelectorAll(".dot");
  // console.log(dot);
  for (i = 0; i < dot.length; i++) {
    dot[i].addEventListener("click", (e) => {
      let index = e.target.getAttribute("data-attr");
      index = parseInt(index); //記得把string"data-attr"轉成int
      changeDot(index);
      // console.log(index);
    });
  }
}
loadAttractionId();

function getImages() {
  let fragment = document.createDocumentFragment();
  let dots = document.querySelector(".dots");
  let imgContainer = document.querySelector(".imgContainer");
  let imgArr = data.images;
  for (var i = 0; i < imgArr.length; i++) {
    let img = document.createElement("img");
    img.src = imgArr[i];
    img.className = "slides";
    fragment.appendChild(img);
    let dot = document.createElement("li");
    dot.className = "dot";
    dot.setAttribute("data-attr", i + 1);
    dots.appendChild(dot);
  }
  imgContainer.appendChild(fragment);
}

function getData() {
  let spotTitle = document.querySelector(".spotTitle");
  let spotMrt = document.querySelector(".spotMrt");
  let spotDesc = document.querySelector(".spotDesc");
  let spotAdd = document.querySelector(".spotAdd");
  let spotTrans = document.querySelector(".spotTrans");
  spotTitle.textContent = data.name;
  spotMrt.textContent = data.category + " at " + data.mrt;
  spotDesc.textContent = data.description;
  spotAdd.textContent = data.address;
  spotTrans.textContent = data.transport;
}

function changeDot(n) {
  showImage((index = n));
}

function changeImage(n) {
  showImage((index += n));
}

function showImage(n) {
  let slides = document.querySelectorAll(".slides");
  let dot = document.querySelectorAll(".dot");
  if (n > slides.length) {
    index = 1;
  }
  if (n < 1) {
    index = slides.length;
  }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
    slides[i].style.animation = "fade 0.5s forwards";
  }
  slides[index - 1].style.display = "flex";
  for (i = 0; i < dot.length; i++) {
    dot[i].className = dot[i].className.replace(" active", "");
    // dot[i].style.background = "black";
  }
  dot[index - 1].className += " active";
  // dot[index - 1].style.background = "white";
}

let order_time = "morning";
let order_price = 2000;

//form changeMoney button
function changeMoney() {
  let morning = document.querySelector("#morning");
  let afternoon = document.querySelector("#afternoon");
  let money = document.querySelector(".money");
  morning.addEventListener("click", () => {
    money.textContent = "新台幣2000元";
    order_time = "morning";
    order_price = 2000;
  });
  afternoon.addEventListener("click", () => {
    money.textContent = "新台幣2500元";
    order_time = "afternoon";
    order_price = 2500;
  });
}

// 預定行程button
let reserved_button = document.querySelector(".reserved_button");
console.log(reserved_button);
reserved_button.addEventListener("click", (e) => {
  e.preventDefault();

  async function checkLogin() {
    let response = await fetch("/api/user");
    const result = await response.json();
    if (result.data === null) {
      document.querySelector(".popup").style.display = "flex";
      document.querySelector(".close_button").addEventListener("click", () => {
        document.querySelector(".popup").style.display = "none";
      });
    } else {
      getOrder();
    }
  }
  checkLogin();
});

async function getOrder() {
  let order_date = document.querySelector("#order_date").value;
  let order_info = {
    attractionId: id,
    date: order_date,
    time: order_time,
    price: order_price,
  };
  console.log(order_info);
  let response = await fetch("/api/booking", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(order_info),
  });
  let res = await response.json();
  console.log(res);
  if (res["ok"]) {
    window.location.href = "/booking";
  }
  if (res["error"]) {
    error_message.textContent = "有資料未輸入";
  }
}
