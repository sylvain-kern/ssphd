document.addEventListener("DOMContentLoaded", function () {
    const tableWrapper = document.querySelector(".table-wrapper");
    const table = tableWrapper.querySelector("table");
    const thead = table.querySelector("thead");
    const headerCells = thead.querySelectorAll("th");
    const firstRowCells = table.querySelector("tbody tr:first-child").children;

    function updateHeaderWidths() {
        thead.style.width = table.offsetWidth + "px"; // Match table width
        for (let i = 0; i < headerCells.length; i++) {
            headerCells[i].style.width = firstRowCells[i].offsetWidth + "px";
        }
    }

    function handleScroll() {
        const offsetTop = tableWrapper.offsetTop;
        if (window.scrollY >= offsetTop) {
            thead.style.position = "fixed";
            thead.style.top = "0px";
            thead.style.backgroundColor = "white";
            thead.style.zIndex = "1000";
        } else {
            thead.style.position = "static";
        }
    }

    function syncHorizontalScroll() {
        thead.style.transform = `translateX(-${tableWrapper.scrollLeft}px)`;
    }

    // Initialize header widths
    updateHeaderWidths();

    // Scroll event listeners
    window.addEventListener("scroll", handleScroll);
    tableWrapper.addEventListener("scroll", syncHorizontalScroll);
    window.addEventListener("resize", updateHeaderWidths);
});
