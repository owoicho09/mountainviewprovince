// Function to toggle the background based on input value
function handleInputBackground(inputElement) {

    const formGroup = inputElement.closest('.form-group').querySelector(".select-selected");
    // const selectText = inputElement

    if (inputElement.value.trim() !== "") {
      inputElement.classList.add("input-has-value");
    //   inputElement.closest(".custom-select").querySelector(".select-selected").classList.add(".select-has-value")
    } else {
      inputElement.classList.remove("input-has-value");
    //   inputElement.closest(".custom-select").querySelector(".select-selected").classList.remove(".select-has-value");
    }
}



  document.querySelectorAll('input[type="text"], input[type="password"]').forEach(function(inputElement) {
    handleInputBackground(inputElement);


    inputElement.addEventListener('input', function() {
      handleInputBackground(inputElement);
    });
  });




  document.querySelectorAll('.select-selected').forEach(function(dropdown) {
    dropdown.addEventListener('click', function() {
      toggleDropdown(this);
    });

    dropdown.addEventListener('keydown', function(event) {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        toggleDropdown(this);
      }
    });
  });


  function toggleDropdown(element) {
    const selectItems = element.nextElementSibling;
    const isExpanded = element.getAttribute('aria-expanded') === 'true';
    const carets = element.querySelectorAll('.switch-icons');
    carets.forEach((icon) =>{
        icon.classList.toggle('not-expanded');
    })


    element.setAttribute('aria-expanded', !isExpanded);
    selectItems.classList.toggle('select-hide');
    element.classList.toggle('active');
    element.querySelector("#caret-up")
  }

  //to Capture the selected value from the custom dropdown and update hidden input
  document.querySelectorAll('.select-items div').forEach(function(option) {
    option.addEventListener('click', function() {
      selectOption(this);
    });

    option.addEventListener('keydown', function(event) {
      const key = event.key;

      if (key === 'Enter' || key === ' ') {
        event.preventDefault();
        selectOption(this);
      }
    });
  });


  function selectOption(option) {
    const selectedValue = option.getAttribute('data-value');
    const selectBox = option.closest('.custom-select').querySelector('.select-selected p');
    const hiddenInput = option.closest('.custom-select').nextElementSibling;


    selectBox.textContent = selectedValue;
    hiddenInput.value = selectedValue;


    const customSelect = option.closest('.custom-select').querySelector('.select-selected');
    if (selectedValue) {
      customSelect.classList.add("select-has-value");
    }


    const selectItems = option.parentElement;
    selectItems.classList.add('select-hide');
    const selectSelected = option.closest('.custom-select').querySelector('.select-selected');
    selectSelected.classList.remove('active');
    selectSelected.setAttribute('aria-expanded', 'false');
  }


const payAmount = document.querySelector(".price").innerHTML;
const serviceCharge = document.querySelector(".service-charge").innerHTML;

// console.log(payAmount);
const calcService = (formatCurrency(serviceCharge));
const calcAmount = (formatCurrency(payAmount));


const getGrandTotal  = (price, charge) =>{
    const cleanedPrice = price.replace(/[^0-9.-]+/g, '');
    const cleanedCharge = charge.replace(/[^0-9.-]+/g, '');

    const addOnPrice = parseFloat(Number(cleanedPrice));
    const addOnCharge = parseFloat(Number(cleanedCharge));

    document.querySelector(".price").innerHTML = calcAmount;
    document.querySelector(".service-charge").innerHTML = calcService;
    return new Intl.NumberFormat('en-NG', {
        style: 'currency',
        currency: 'NGN',
    }).format(addOnCharge + addOnPrice);
};
const totalBookingPrice = (getGrandTotal(payAmount,serviceCharge));
// serviceCharge = (formatCurrency(serviceCharge));
document.querySelector(".result").innerHTML = totalBookingPrice;


function formatCurrency(amount) {
    return new Intl.NumberFormat('en-NG', {
      style: 'currency',
      currency: 'NGN',
    }).format(amount);
};



//   const passwordInputs = document.querySelectorAll(".p-input");

//   passwordInputs.forEach((input)=> {
//     const togglePassword = input.parentNode.querySelector(".toggle-password");
//     const eyeOpenIcon = input.parentNode.querySelector(".eye-open");
//     const eyeCloseIcon = input.parentNode.querySelector(".eye-close");

//     togglePassword.addEventListener("click", () => {
//     const type = input.getAttribute("type") === "password" ? "text" : "password";
//     input.setAttribute("type", type);

//     if (type === "password") {
//       eyeOpenIcon.style.display = "inline";
//       eyeCloseIcon.style.display = "none";
//     } else {
//       eyeOpenIcon.style.display = "none";
//       eyeCloseIcon.style.display = "inline";
//     }
//     });

//   })


