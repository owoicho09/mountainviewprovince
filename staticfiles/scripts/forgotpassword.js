document.addEventListener('DOMContentLoaded', function () {
    const inputElem = document.querySelector('input[type="email"]');


    if (inputElem) {
      handleInputBackground(inputElem);

      inputElem.addEventListener('input', function () {
        handleInputBackground(inputElem);
      });
    }
});

function handleInputBackground(inputElement) {
    if (inputElement.value.trim() !== "") {
        inputElement.classList.add("input-has-value");
    } else {
        inputElement.classList.remove("input-has-value");
    }
}

document.getElementById('signInForm').addEventListener('submit', function(event) {
    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('email-error-msg');
    const emailSuccess = document.getElementById('success-msg');
    const emailValue = emailInput.value.trim();

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


    if (!emailPattern.test(emailValue)) {
      emailError.textContent = "Please enter a valid email address.";
    //   emailInput.classList.add('input-error');
      event.preventDefault();
    } else {
        emailSuccess.textContent = "Good email";
    }
});
