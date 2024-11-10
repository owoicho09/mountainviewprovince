const openNCloseIcon = document.querySelectorAll('.nav-icon');
const openNav = document.querySelector(".open-nav");
const scrollToTopBtn = document.querySelector(".scroll-to-top");
const scrollProgress = document.getElementById("scroll-progress");

document.addEventListener("DOMContentLoaded", () => {

    openNCloseIcon.forEach((icn) => icn.addEventListener("click", (e) => {
        e.preventDefault();
        openNav.classList.toggle("not-visible");
    }));

    document.addEventListener('click', (e) => {
        if (!openNav.contains(e.target) && !e.target.closest('.nav-icon')) {
            openNav.classList.add('not-visible');
        }
    });

    window.addEventListener('scroll', () => {

        if (window.scrollY > 500) {
            scrollToTopBtn.classList.add('show');
        } else {
            scrollToTopBtn.classList.remove('show');
        }
    });

    scrollToTopBtn.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});