//signin popup右上角登入/註冊btn
function signin_popup() {
  let signin_button = document.querySelector("a.signin_button");
  signin_button.addEventListener("click", () => {
    if (signin_button.innerHTML === "登入/註冊") {
      document.querySelector(".popup").style.display = "flex";
      document.querySelector(".signup_popup").style.display = "none";

      document.querySelector(".close_button").addEventListener("click", () => {
        document.querySelector(".popup").style.display = "none";
      });
    }
  });
}
signin_popup();

//signup popup
function signup_popup() {
  let signup_button = document.querySelector("a.signup_button");
  signup_button.addEventListener("click", () => {
    document.querySelector(".signup_popup").style.display = "flex";
    document.querySelector("#signup_errorAlert").textContent = "";
    document.querySelector("#signup_successAlert").textContent = "";
  });

  document
    .querySelector(".signup_close_button")
    .addEventListener("click", () => {
      document.querySelector(".signup_popup").style.display = "none";
      document.querySelector(".popup").style.display = "none";
    });
}
signup_popup();

//signin popup form中下方登入btn
function form_signin_popup() {
  let form_signinBtn = document.querySelector(".form_signinBtn");
  form_signinBtn.addEventListener("click", () => {
    document.querySelector(".signup_popup").style.display = "none";
    document.querySelector(".popup").style.display = "flex";
    document.querySelector("#signin_errorAlert").textContent = "";
  });
}
form_signin_popup();

//註冊流程
let signup_popup_form = document.querySelector(".signup_popup_form");
signup_popup_form.addEventListener("submit", (e) => {
  e.preventDefault();

  async function signUp() {
    const name = document.querySelector("#name").value;
    const email = document.querySelector("#email").value;
    const password = document.querySelector("#password").value;
    let response = await fetch("/api/user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name,
        email: email,
        password: password,
      }),
    });
    let res = await response.json();
    // console.log(res);
    if (res["ok"]) {
      document.querySelector("#signup_successAlert").style.display = "block";
      document.querySelector("#signup_successAlert").textContent = "註冊成功";
      document.querySelector("#signup_errorAlert").style.display = "none";
      console.log(response);
    }
    if (res["error"]) {
      document.querySelector("#signup_successAlert").style.display = "none";
      document.querySelector("#signup_errorAlert").style.display = "block";
      document.querySelector("#signup_errorAlert").textContent =
        "註冊失敗,此信箱已被註冊";
    }
    document.querySelector("#name").value = "";
    document.querySelector("#email").value = "";
    document.querySelector("#password").value = "";
  }
  signUp();
});

//登入流程
let popup_form = document.querySelector(".popup_form");
popup_form = document.addEventListener("submit", (e) => {
  e.preventDefault();

  const em = document.querySelector("#em").value;
  const pw = document.querySelector("#pw").value;
  async function signIn() {
    let response = await fetch("/api/user", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: em,
        password: pw,
      }),
    });
    let res = await response.json();
    // console.log(res);
    if (res["ok"]) {
      window.location.reload();
    }
    if (res["error"]) {
      document.querySelector("#signin_errorAlert").textContent =
        "登入失敗,信箱或密碼錯誤";
    }
    document.querySelector("#em").value = "";
    document.querySelector("#pw").value = "";
    signinStatus();
  }
  signIn();
});

//檢視登入狀態
async function signinStatus() {
  let response = await fetch("/api/user");
  const result = await response.json();
  if (result.data === null) {
    document.querySelector(".signin_button").textContent = "登入/註冊";
  } else {
    document.querySelector(".signin_button").textContent = "登出系統";
    document.querySelector(".signin_button").addEventListener("click", () => {
      signOut();
    });
  }
}
signinStatus();

//登出
async function signOut() {
  let response = await fetch("/api/user", {
    method: "DELETE",
  });
  const res = await response.json();
  if (res["ok"]) {
    // window.location.reload();
    location.href = "/";
  }
}

async function reservedOrder() {
  let response = await fetch("/api/user");
  const result = await response.json();
  if (result.data) {
    window.location.href = "/booking";
  } else {
    document.querySelector(".popup").style.display = "flex";
    document.querySelector(".close_button").addEventListener("click", () => {
      document.querySelector(".popup").style.display = "none";
    });
  }
}

let reservedBtn = document.querySelector(".reservedBtn");
reservedBtn.addEventListener("click", (e) => {
  e.preventDefault();
  reservedOrder();
});
