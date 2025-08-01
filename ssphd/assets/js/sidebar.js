const menu = document.querySelector(".sidebar");
const menuItems = document.querySelectorAll(".menuItem");
const burger = document.querySelector(".burger");
const showIcon= document.querySelector(".burger > .show");
const hideIcon = document.querySelector(".burger > .hide");

function collapseMenu() {
  menu.classList.remove("show");
  hideIcon.style.display = "none";
  showIcon.style.display = "block";
}

function toggleMenu() {
  if (menu.classList.contains("show")) {
    menu.classList.remove("show");
    hideIcon.style.display = "none";
    showIcon.style.display = "block";
  } else {
    menu.classList.add("show");
    hideIcon.style.display = "block";
    showIcon.style.display = "none";
  }
}

burger.addEventListener("click", toggleMenu);

document.addEventListener("click", function (event) {
  if (!menu.contains(event.target) && !burger.contains(event.target)) {
    collapseMenu();
  }
});

menuItems.forEach(
  function(menuItem) {
    menuItem.addEventListener("click", toggleMenu);
  }
)

// expand/hide buttons
const sublists = document.querySelectorAll('nav > ul > li > ul > li > ul');

sublists.forEach(sublist => {
  const parentheader = sublist.parentElement.querySelector('a');
  const expandbtn = document.createElement('button');
  expandbtn.classList.add('expand');
  const buttonicon = document.createElement('i');
  buttonicon.classList.add('bx');
  buttonicon.classList.add('bx-chevron-right');
  expandbtn.appendChild(buttonicon);
  parentheader.appendChild(expandbtn);

  buttonicon.setAttribute("aria-expanded", "false");
  buttonicon.style.cursor = "pointer";

  // Hide sublist initially (optional)
  sublist.style.display = "none";

  buttonicon.addEventListener("click", () => {
    const isExpanded = sublist.style.display === "block";
    sublist.style.display = isExpanded ? "none" : "block";
    buttonicon.setAttribute("aria-expanded", String(!isExpanded));

    // Update icon class
    buttonicon.classList.toggle("bx-chevron-right", isExpanded);
    buttonicon.classList.toggle("bx-chevron-down", !isExpanded);
    event.stopPropagation();
    event.preventDefault();
  });
});

collapseMenu();