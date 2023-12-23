const delay = ms => new Promise(res => setTimeout(res, ms));

// use a class selector if available
let blocks = document.querySelectorAll("pre");

blocks.forEach((block) => {
  // only add button if browser supports Clipboard API
  if (navigator.clipboard) {
    let button = document.createElement("button");

    button.innerHTML = '<i class="menuIcon material-symbols-rounded">content_paste</i>';
    block.appendChild(button);

    button.addEventListener("click", async () => {
      await copyCode(block);
      button.innerHTML = '<i class="menuIcon material-symbols-rounded">inventory</i>';
      await delay(2500);
      button.innerHTML = '<i class="menuIcon material-symbols-rounded">content_paste</i>';
    });
  }
});

async function copyCode(block) {
  let code = block.querySelector("code");
  let text = code.innerText;

  await navigator.clipboard.writeText(text);
}