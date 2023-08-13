const menu = document.querySelector(".sidebar");
const menuItems = document.querySelectorAll(".menuItem");
const hamburger= document.querySelector(".hamburger");
const closeIcon= document.querySelector(".closeIcon");
const menuIcon = document.querySelector(".menuIcon");

function collapseMenu() {
  menu.classList.remove("showMenu");
  closeIcon.style.display = "none";
  menuIcon.style.display = "block";
}

function toggleMenu() {
  if (menu.classList.contains("showMenu")) {
    menu.classList.remove("showMenu");
    closeIcon.style.display = "none";
    menuIcon.style.display = "block";
  } else {
    menu.classList.add("showMenu");
    closeIcon.style.display = "block";
    menuIcon.style.display = "none";
  }
}

hamburger.addEventListener("click", toggleMenu);

document.addEventListener("click", function (event) {
  if (!menu.contains(event.target) && !hamburger.contains(event.target)) {
    collapseMenu();
  }
});

menuItems.forEach(
  function(menuItem) {
    menuItem.addEventListener("click", toggleMenu);
  }
)