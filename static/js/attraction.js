let id = location.href.split("/")[4];
let index = 1;
async function loadAttractionId() {
  let response = await fetch("/api/attraction/" + id);
  let result = await response.json();
  data = result["data"];
  let imgArr = data.images;

  getImages(imgArr);
  getData();
  showImage();

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
      index = parseInt(index);
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
  }
  for (i = 0; i < dot.length; i++) {
    dot[i].style.background = "black";
  }
  slides[index - 1].style.display = "flex";
  dot[index - 1].style.background = "white";
}
