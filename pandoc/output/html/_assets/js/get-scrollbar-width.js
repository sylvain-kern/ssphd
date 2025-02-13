function getScrollBarWidth() {
    let el = document.createElement("div");
    el.style.cssText = "overflow:scroll; visibility:hidden; position:absolute;";
    document.body.appendChild(el);
    let width = el.offsetWidth - el.clientWidth;
    el.remove();
    return width;
}
document.documentElement.style.setProperty(
    '--scrollbar-width',
    getScrollBarWidth().toString() + 'px'
);