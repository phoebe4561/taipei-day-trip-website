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
async function loadAttractions() {
  const response = await fetch("/api/attractions?page=" + currentPage);
  const result = await response.json();
  data = result.data;
  nextpage = result.nextpage;

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

    let img = document.createElement("img");
    img.setAttribute("src", item["images"][0]);
    img.setAttribute("alt", item["name"]);

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
    img_container.appendChild(img);
    img_container.appendChild(attraction_title);
    img_container.appendChild(p_container);

    card.appendChild(img_container);
    cards.appendChild(card);
  }
}