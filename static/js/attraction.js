let id = location.href.split("/")[4];
async function loadAttractionId() {
  let response = await fetch("/api/attraction/" + id);
  let result = await response.json();
  data = result["data"];
  let imgArr = data.images;

  getImages(imgArr);
  getData();
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
