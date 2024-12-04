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

// const caretUp = document.getElementById("caret-up");
// const caretDown= document.getElementById("caret-down");
// const dropdownContent = document.getElementById("other-content");
// caretUp.addEventListener("click", function(){
//     caretUp.classList.add("not-expanded");
//     caretDown.classList.remove("not-expanded");
//     dropdownContent.style.height = '0';
//     dropdownContent.style.opacity = '0';

// })
// caretDown.addEventListener("click", function(){
//     caretDown.classList.toggle("not-expanded");
//     caretUp.classList.toggle("not-expanded");
//     dropdownContent.style.height = dropdownContent.scrollHeight + 'px';
//     dropdownContent.style.opacity = '1';

// });

// const dropdownContainers = document.querySelectorAll(".drop-container");
const caretDown = document.querySelectorAll(".c-down");
const caretUp = document.querySelectorAll(".c-up");
// const dropdownContent = document.querySelectorAll(".dropdown-content");

caretUp.forEach((icon)=> icon.addEventListener("click",()=>{
    const dropdownContent = icon.closest(".drop-container").querySelector(".dropdown-content");
    const nextIcon = icon.closest(".icons-holder").querySelector(".c-down");
    icon.classList.add("not-expanded");
    nextIcon.classList.remove("not-expanded");
    dropdownContent.classList.toggle('no-h');
}));

caretDown.forEach((icon)=> icon.addEventListener("click",()=>{
    const dropdownContent = icon.closest(".drop-container").querySelector(".dropdown-content");
    const nextIcon = icon.closest(".icons-holder").querySelector(".c-up");
    icon.classList.add("not-expanded");
    nextIcon.classList.remove("not-expanded");
    dropdownContent.classList.toggle('no-h');
}));



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

    //    if(block.classList.contains("b-select")){
    //     const blockNameInput = block.querySelector('input[name="block-name"]');
    //     const roomAvailInput = block.querySelector('input[name="available-rooms"]');
    //     const blockName = block.querySelector(".block-name").innerHTML;
    //     const blockRoomsAvailable = block.querySelector(".no-rooms").innerHTML;

    //     blockNameInput.setAttribute('data-name', blockName);
    //     roomAvailInput.setAttribute('data-room', blockRoomsAvailable);

    //    }else{
    //     const blockNameInput = block.querySelector('input[name="block-name"]');
    //     const roomAvailInput = block.querySelector('input[name="available-rooms"]');

    //     blockNameInput.setAttribute('data-name', " ");
    //     roomAvailInput.setAttribute('data-room', " ");
    //    }

}));

// document.getElementById("block-list").addEventListener("submit", () =>{
//     const firstData = document.querySelector('input[name="block-name"]').dataset.name;
//     const secondData = document.querySelector('input[name="no-rooms "]').dataset.room;
//     console.log(firstData, secondData);

// })