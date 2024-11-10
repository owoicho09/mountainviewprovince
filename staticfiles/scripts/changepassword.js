const form = document.getElementById('change-password-form');
const feedbackMessage = document.getElementById('feedback-message');

form.addEventListener("submit", (event) => {
    // Get the new password values
    const newPassword = form.new_password1.value;
    const confirmPassword = form.new_password2.value;

    // Check if passwords match
    if (newPassword !== confirmPassword) {
        event.preventDefault();  // Prevent submission if passwords don't match
        feedbackMessage.textContent = "New passwords do not match!";
        feedbackMessage.style.color = "red";  // Optionally style the message
    } else {
        feedbackMessage.textContent = "New password saved!";
        feedbackMessage.style.color = "green";
        // Do not preventDefault here, so the form will submit
    }
});
