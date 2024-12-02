document.addEventListener('DOMContentLoaded', function() {
    const options = document.querySelectorAll('.option');

    options.forEach(option => {
      const headerInput = option.querySelector('.header-input');
      const subOption = option.querySelector('.sub-option');
      const caretUp = option.querySelector('#caret-up');
      const caretDown = option.querySelector('#caret-down');

      const toggleSubOption = () => {
        if (headerInput.checked) {
          subOption.style.display = 'block';
          caretUp.style.display = 'inline-block';
          caretDown.style.display = 'none';
        } else {
          subOption.style.display = 'none';
          caretUp.style.display = 'none';
          caretDown.style.display = 'inline-block';
        }
      };

      toggleSubOption();

      headerInput.addEventListener('change', () => {
      options.forEach(otherOption => {
        if (otherOption !== option) {
          const otherHeaderInput = otherOption.querySelector('.header-input');
          otherHeaderInput.checked = false;
          otherOption.querySelector('.sub-option').style.display = 'none';
          otherOption.querySelector('#caret-up').style.display = 'none';
          otherOption.querySelector('#caret-down').style.display = 'inline-block';
        }
        });

      toggleSubOption();
      });


    });
});


const roomNo = document.querySelectorAll(".r-no-box");
const roomNoInput = document.querySelector('input[name="room-number"]');

roomNo.forEach((room) => room.addEventListener("click",()=>{
  // console.log(room.innerHTML);
  roomNoInput.setAttribute("data-room", room.innerHTML);
  // console.log(roomNoInput.dataset.room);


  roomNo.forEach((r)=> r.classList.remove("bg-brown"));
  room.classList.add("bg-brown");

}));


//to do- to make sure a previously selected unrelevent checkbox isnt issued,
// if the user didnt uncheck it and selects another option.

let flexIsChecked;
// const roomNoInput = document.querySelector('input[name="room-number"]');
const flexiPlans = document.querySelectorAll('input[data-type="flex-plan"]');
flexiPlans.forEach((plan)=> {
  plan.addEventListener("click", (e) => {

    //making sure multiple checkboxes aren't selected
    if(e.target.checked){
      flexIsChecked = true;
      flexiPlans.forEach((select) => select !== e.target ? select.checked = false : select.checked = true);



      const parentContainer = e.target.closest(".sub-option");
      // const roomNumber = parentContainer.querySelector(".bg-brown");
      // roomNumber ? roomNoInput.setAttribute("data-roomNo", roomNumber.innerHTML) :
      // roomNoInput.setAttribute("data-roomNo", " ");

      if(parentContainer){
        const PriceForSemester = parentContainer.querySelector(".sem-price");
        const PriceForSession = parentContainer.querySelector(".ses-price");

        // const roomNumber = parentContainer?.querySelector(".bg-brown");
        // console.log(roomNumber.innerHTML);


        //selecting the appropiate option of the checked flex pay
        const semOption = parentContainer.querySelector(".sem-option input");
        const sesOption = parentContainer.querySelector(".ses-option input");

        //get the data price of each input
        const semPrice = parseFloat(semOption.dataset.price);
        const sesPrice = parseFloat(sesOption.dataset.price);

        //calculate the 30% flex-payment
        const flexSem = semPrice * 0.3;
        const flexSes = sesPrice * 0.3;

        //formatting the estimated price for semester
        const formattedSemPrice = formatCurrency(flexSem);

        //formatting the estimated price for session
        const formattedSesPrice = formatCurrency(flexSes);

        //updating the prices
        PriceForSemester.innerHTML = formattedSemPrice;
        if(semOption){
          semOption.setAttribute("data-price", flexSem.toFixed(2))
        }
        // console.log(semOption, sesOption);


        PriceForSession.innerHTML = formattedSesPrice;
        if(sesOption){
          sesOption.setAttribute("data-price", flexSes.toFixed(2))
        }

        // roomNoInput.setAttribute("data-room", roomNumber.innerHTML);

        // Store the original prices for later use
        PriceForSemester.dataset.originalPrice = semPrice;
        PriceForSession.dataset.originalPrice = sesPrice;



      }

    }else{
      flexIsChecked = false;
      // Reverting to the original prices
      const parentContainer = e.target.closest(".sub-option");

      if (parentContainer) {
        const PriceForSemester = parentContainer.querySelector(".sem-price");
        const PriceForSession = parentContainer.querySelector(".ses-price");

        const semPrice = parseFloat(PriceForSemester.dataset.originalPrice);
        const sesPrice = parseFloat(PriceForSession.dataset.originalPrice);

        const semOption = parentContainer.querySelector(".sem-option input");
        const sesOption = parentContainer.querySelector(".ses-option input");

        // const roomNumber = parentContainer.querySelector(".room-row .bg-brown");



        // console.log(semOption, sesOption);


        // Update the displayed prices to original price
        PriceForSemester.innerHTML = formatCurrency(semPrice);
        semOption.setAttribute("data-price", semPrice.toFixed(2));

        PriceForSession.innerHTML = formatCurrency(sesPrice);
        sesOption.setAttribute("data-price", sesPrice.toFixed(2));

        // roomNoInput.setAttribute("data-room", roomNumber.innerHTML);

      }
    }

  });

});

function formatCurrency(amount) {
  return new Intl.NumberFormat('en-NG', {
    style: 'currency',
    currency: 'NGN',
  }).format(amount);
};


 document.getElementById("select-room-form").addEventListener("submit",(e) =>{
   e.preventDefault();


   const rate_type = document.querySelector("input[name='hostel_rate']:checked").value;
   const rate_price = document.querySelector("input[name='hostel_rate']:checked").dataset.price;
   const room_number = document.querySelector("input[name='room-number']").dataset.room;


   console.log({ rate_type, rate_price, room_number, flexIsChecked});

 })


