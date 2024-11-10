// Function to toggle the background based on input value

function handleInputBackground(inputElement) {

  const formGroup = inputElement.closest('.form-group');

  if (inputElement.value.trim() !== "") {
    inputElement.classList.add("input-has-value");

  } else {
    inputElement.classList.remove("input-has-value");

  }
}



document.querySelectorAll('input[type="text"], input[type="password"]').forEach(function(inputElement) {
  handleInputBackground(inputElement);

  // Listen for changes in input fields
  inputElement.addEventListener('input', function() {
    handleInputBackground(inputElement);
  });
});

// Handle custom dropdowns for Institution and Gender
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

  element.setAttribute('aria-expanded', !isExpanded);
  selectItems.classList.toggle('select-hide');
  element.classList.toggle('active');
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





const passwordInput = document.getElementById('password');
const togglePassword = document.getElementById('toggle-password');
const eyeOpenIcon = document.getElementById('eye-open');
const eyeCloseIcon = document.getElementById('eye-close');


togglePassword.addEventListener('click', function () {

  const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
  passwordInput.setAttribute('type', type);


  if (type === 'password') {
    eyeOpenIcon.style.display = 'inline';
    eyeCloseIcon.style.display = 'none';
  } else {
    eyeOpenIcon.style.display = 'none';
    eyeCloseIcon.style.display = 'inline';
  }
});