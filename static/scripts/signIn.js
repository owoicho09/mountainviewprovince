  const passwordInput = document.getElementById('password');
  const togglePassword = document.getElementById('toggle-password');
  const eyeOpenIcon = document.getElementById('eye-open');
  const eyeCloseIcon = document.getElementById('eye-close');

  // Add click event listener to toggle password visibility
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

document.getElementById('signInForm').addEventListener('submit', function(event) {
    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('email-error-msg');
    const emailValue = emailInput.value.trim();

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


    if (!emailPattern.test(emailValue)) {
      emailError.textContent = "Please enter a valid email address.";
      emailInput.classList.add('input-error');
      event.preventDefault();
    } else {
      emailError.textContent = "good email";
    }
});


function handleInputBackground(inputElement) {

    // const formGroup = inputElement.closest('.form-group');

    if (inputElement.value.trim() !== "") {
      inputElement.classList.add("input-has-value");

    } else {
      inputElement.classList.remove("input-has-value");

    }
  }

document.querySelectorAll('input[type="email"], input[type="password"]').forEach(function(inputElement) {
    handleInputBackground(inputElement);

    // Listen for changes in input fields
    inputElement.addEventListener('input', function() {
      handleInputBackground(inputElement);
    });
  });
