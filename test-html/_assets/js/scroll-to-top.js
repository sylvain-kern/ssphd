// document.addEventListener('click', function(event) {
//     if (event.target.classList.contains('scroll-link')) {
//         event.preventDefault();
//         const targetId = event.target.getAttribute('href');
//         const targetElement = document.querySelector(targetId);
//         if (targetElement) {
//             targetElement.scrollIntoView({ behavior: 'smooth' });
//         }
//     }
// });

// Modify href attributes of links with class "scroll-link" to use relative paths
document.addEventListener('DOMContentLoaded', function() {
    const scrollLinks = document.querySelectorAll('.relative-link');
    scrollLinks.forEach(link => {
        const originalHref = link.getAttribute('href');
        link.setAttribute('href', window.location.pathname + originalHref);
    });
});