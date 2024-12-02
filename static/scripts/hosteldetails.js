document.addEventListener('DOMContentLoaded', function() {
    const descriptions = document.querySelectorAll('.description-box');

    descriptions.forEach(function(description) {
        const toggleLink = description.querySelector('.toggle-link');
        const shortDesc = description.querySelector('.short-description');
        const fullDesc = description.querySelector('.full-description');


        toggleLink.addEventListener('click', function(e) {
            e.preventDefault();
            const isExpanded = toggleLink.getAttribute('aria-expanded') === 'true';

            if (!isExpanded) {
                fullDesc.classList.add('expanded');
                toggleLink.setAttribute('aria-expanded', 'true');
                toggleLink.textContent = 'Read Less';


                fullDesc.appendChild(toggleLink);
            } else {
                fullDesc.classList.remove('expanded');
                toggleLink.setAttribute('aria-expanded', 'false');
                toggleLink.textContent = 'Read More...';


                shortDesc.appendChild(toggleLink);
            }
        });
    });
});

const caretUp = document.getElementById("caret-up");
const caretDown= document.getElementById("caret-down");
const dropdownContent = document.getElementById("other-content");
caretUp.addEventListener("click", function(){
    // e.preventDefault();
    caretUp.classList.add("not-expanded");
    caretDown.classList.remove("not-expanded");
    dropdownContent.style.height = '0';
    dropdownContent.style.opacity = '0';

})
caretDown.addEventListener("click", function(){
    caretDown.classList.toggle("not-expanded");
    caretUp.classList.toggle("not-expanded");
    dropdownContent.style.height = dropdownContent.scrollHeight + 'px';
    dropdownContent.style.opacity = '1';

});



const mainImage = document.querySelector(".m-image");
const carouselImages = document.querySelectorAll(".carousel-img");
const carouselImagesBoxes = document.querySelectorAll(".t-img");

carouselImagesBoxes.forEach((box) => box.addEventListener("click",()=>{
    carouselImagesBoxes.forEach((i)=> i.classList.remove("m-select"));
    box.classList.add("m-select");
}))

carouselImages.forEach((image) => {
    image.addEventListener("click", () => {
        mainImage.classList.add("hidden");
        setTimeout(() => {
            mainImage.src = image.src;
            mainImage.classList.remove("hidden");
        }, 500);
    });
});


const blocks = document.querySelectorAll(".form-group");
blocks.forEach((block) => block.addEventListener("click", () =>{
   blocks.forEach((b) => b.classList.remove("b-select"));

   block.classList.add("b-select");
}));