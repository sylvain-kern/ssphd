var tables = document.querySelectorAll("table");
tables.forEach(insert);

function insert(table) {
    var wrapper = document.createElement('div');
    wrapper.classList.add("table-wrapper");
    table.parentNode.insertBefore(wrapper, table);
    wrapper.appendChild(table);
}
