
let scrollPosition = 0;

let dict = {};

h3headings = document.querySelectorAll('section .level3');

h3headings.forEach( function(item, index) {
    dict[item.id] = item.offsetTop;
});

let currenth3_index = 0;

scrolloffset = 50;

window.addEventListener('scroll', (event) => {
    scrollPosition = window.scrollY;
    let currenth3 = '';
    for (const [key, value] of Object.entries(dict)) {
        if (value <= scrollPosition + scrolloffset) {
            currenth3 = key;
        }
        else {
            break;
        }
    }

    document.links[currenth3_index].classList.remove('current');

    for (var j = 0; j < document.links.length; j++) {

        if (document.links[j].href === window.location.origin+window.location.pathname+'#'+currenth3 || document.links[j].href === window.location.origin+window.location.pathname+'/#'+currenth3) {
            currenth3_index = j;
            break;
        }
        currenth3_index = 0;
    }
    document.links[currenth3_index].classList.add('current');
})

let current_index = 0;

// Get the current page URL without hash
const currentPageUrl = window.location.origin + window.location.pathname;
const currentPageUrlWithSlash = currentPageUrl.endsWith('/') ? currentPageUrl : currentPageUrl + '/';
const currentPageUrlWithoutSlash = currentPageUrl.endsWith('/') ? currentPageUrl.slice(0, -1) : currentPageUrl;

for (var i = 0; i < document.links.length; i++) {
    // Get link URL without hash
    const linkUrl = new URL(document.links[i].href);
    const linkPageUrl = linkUrl.origin + linkUrl.pathname;
    
    if (linkPageUrl === currentPageUrlWithoutSlash || linkPageUrl === currentPageUrlWithSlash) {
        current_index = i;
        break;
    }
}
document.links[current_index].classList.add('current');
document.links[current_index].querySelector('.expand > i').setAttribute("aria-expanded", "true");
document.links[current_index].querySelector('.expand > i').classList.toggle("bx-chevron-right");
document.links[current_index].querySelector('.expand > i').classList.toggle("bx-chevron-down");
document.links[current_index].parentElement.querySelector('ul').style.display = "block";