// language name + copy button

const delay = ms => new Promise(res => setTimeout(res, ms));

var pres = document.querySelectorAll('pre');

// code headings

var codeDivs = document.querySelectorAll("div.sourceCode");

codeDivs.forEach(sourceCodeDiv => {

    startfrom = sourceCodeDiv.getAttribute("data-startfrom")

    pre = sourceCodeDiv.querySelector("pre");

    if (startfrom != null) {
        sourceCodeDiv.style["counter-set"] = "code-numberlines calc(" + startfrom + " - 1)";
    } else {
        sourceCodeDiv.style["counter-set"] = "code-numberlines 0";
    };

    code = pre.querySelector("code");
    languageName = code.classList[code.classList.length - 1];

    langCopy = document.createElement("div");
    langCopy.classList.add("lang-copy");

    if (languageName != "sourceCode") {
        languageSpan = document.createElement("span");
        languageSpan.classList.add("lang");
        languageSpan.innerHTML = languageName;
        langCopy.appendChild(languageSpan);
    }

    if (navigator.clipboard) {
        let copybutton = document.createElement("button");

        copybutton.classList="copy";

        copybutton.codeToCopy = code.innerText;

        copybutton.innerHTML = 'copy';
        copybutton.setAttribute("title", "Copy to clipboard")
        langCopy.appendChild(copybutton);

        copybutton.addEventListener("click", async () => {
            await navigator.clipboard.writeText(copybutton.codeToCopy);
            copybutton.innerHTML = 'copied!';
            await delay(2500);
            copybutton.innerHTML = 'copy';
        });
    };

    codeBlockHeader = document.createElement("div");

    if (sourceCodeDiv.hasAttribute("data-filename")) {
        filename = sourceCodeDiv.getAttribute("data-filename");
        codeBlockHeader.classList.add("code-header");
        codeBlockTitle = document.createElement("span");
        codeBlockTitle.innerHTML = filename;
        codeBlockHeader.appendChild(codeBlockTitle);
        codeBlockHeader.appendChild(langCopy);
        pre.insertBefore(codeBlockHeader, pre.firstChild);
    } else {
        codeBlockHeader.classList.add("lang-copy-container");
        codeBlockHeader.appendChild(langCopy);
        pre.insertBefore(codeBlockHeader, pre.firstChild);
    }
});

var lonelyPres = document.querySelectorAll(":not(div.sourceCode) > pre");

lonelyPres.forEach(pre => {

    code = pre.querySelector("code");

    langCopy = document.createElement("div");
    langCopy.classList.add("lang-copy");

    codeBlockHeader = document.createElement("div");
    codeBlockHeader.classList.add("lang-copy-container");
    codeBlockHeader.appendChild(langCopy)

    if (navigator.clipboard) {
        let copybutton = document.createElement("button");

        copybutton.classList="copy";

        copybutton.codeToCopy = code.innerText;

        copybutton.innerHTML = 'copy';
        copybutton.setAttribute("title", "Copy code")
        langCopy.appendChild(copybutton);

        copybutton.addEventListener("click", async () => {
            await navigator.clipboard.writeText(copybutton.codeToCopy);
            copybutton.innerHTML = 'copied!';
            await delay(2500);
            copybutton.innerHTML = 'copy';
        });
    };

    pre.insertBefore(codeBlockHeader, pre.firstChild);

});