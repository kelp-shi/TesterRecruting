const sign_in_btn = document.querySelector("#login-btn");
const sign_up_btn = document.querySelector("#logon-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("logon-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("logon-mode");
});