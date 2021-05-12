//signin popup
function signin_popup() {
  let signin_button = document.querySelectorAll("a.signin_button");
  for (i = 0; i < signin_button.length; i++) {
    signin_button[i].addEventListener("click", () => {
      document.querySelector(".popup").style.display = "flex";
      document.querySelector(".signup_popup").style.display = "none";
    });

    document.querySelector(".close_button").addEventListener("click", () => {
      document.querySelector(".popup").style.display = "none";
    });
  }
}
signin_popup();

//signup popup
function signup_popup() {
  let signup_button = document.querySelector("a.signup_button");
  signup_button.addEventListener("click", () => {
    document.querySelector(".signup_popup").style.display = "flex";
  });

  document
    .querySelector(".signup_close_button")
    .addEventListener("click", () => {
      document.querySelector(".signup_popup").style.display = "none";
      document.querySelector(".popup").style.display = "none";
    });
}
signup_popup();
