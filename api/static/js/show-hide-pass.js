const show = document.querySelector(".fa-eye");
const hide = document.querySelector(".fa-eye-slash");
const pass = document.getElementById("password");

show.addEventListener("click", function () {
    show.style.visibility = "hidden";
    hide.style.visibility = "visible";
    pass.type = "text";
    console.log("showed");
});

hide.addEventListener("click", function () {
    hide.style.visibility = "hidden";
    show.style.visibility = "visible";
    pass.type = "password";
    console.log("hidden");
});
