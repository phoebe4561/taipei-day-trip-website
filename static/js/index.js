let nextpage;
let observer;

function new_observer() {
  let options = {
    root: null,
    rootMargin: "0px",
    threshold: 0.5,
  };
  observer = new IntersectionObserver(handleInternet, options);
  observer.observe(document.querySelector("footer"));
}
new_observer();

function handleInternet(entries) {
  if (entries[0].isIntersecting) {
    loadAttractions();
  }
}

let currentPage = 0;
let search_mode = false;
let keyword;
async function loadAttractions() {
  let response;
  if (!search_mode) {
    response = await fetch("/api/attractions?page=" + currentPage);
  } else {
    response = await fetch(
      "/api/attractions?page=" + currentPage + "&keyword=" + keyword
    );
  }
  const result = await response.json();
  data = result.data;
  nextpage = result.nextpage;

  if (data.length === 0 && search_mode) {
    document.querySelector(".cards").innerHTML = "查無資料";
    return;
  }

  getMain(data);

  if (nextpage !== null) {
    currentPage++;
  } else {
    observer.unobserve(document.querySelector("footer"));
  }
}

function getMain(data) {
  let cards = document.querySelector(".cards");
  for (let item of data) {
    let card = document.createElement("div");
    card.classList = "mycard";

    let a_tag = document.createElement("a");
    let img = document.createElement("img");
    img.setAttribute("src", item["images"][0]);
    img.setAttribute("alt", item["name"]);
    a_tag.appendChild(img);
    a_tag.href = "/attraction/" + item["id"];

    let attraction_title = document.createElement("h3");
    let title = document.createTextNode(item["name"]);
    attraction_title.appendChild(title);

    let attraction_mrt = document.createElement("p");
    let mrt = document.createTextNode(item["mrt"]);
    attraction_mrt.appendChild(mrt);

    let attraction_category = document.createElement("p");
    let category = document.createTextNode(item["category"]);
    attraction_category.appendChild(category);

    let p_container = document.createElement("div");
    p_container.classList = "pContainer";
    p_container.appendChild(attraction_mrt);
    p_container.appendChild(attraction_category);

    let img_container = document.createElement("div");
    img_container.classList = "imgContainer";
    img_container.appendChild(a_tag);
    img_container.appendChild(attraction_title);
    img_container.appendChild(p_container);

    card.appendChild(img_container);
    cards.appendChild(card);
  }
}

const search = document.querySelector(".search_spot");
search.addEventListener("submit", (e) => {
  e.preventDefault();
  currentPage = 0;
  document.querySelector(".cards").innerHTML = "";
  search_mode = true;

  keyword = e.target[0].value;

  observer.unobserve(document.querySelector("footer"));
  new_observer();
});
