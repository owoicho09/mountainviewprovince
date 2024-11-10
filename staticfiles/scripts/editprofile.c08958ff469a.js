

//image upload logic
const fileInput = document.getElementById('file-upload');
const profileImage = document.getElementById('profile-img');

fileInput.addEventListener('change', handleImageUpload);

function handleImageUpload(event) {
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            profileImage.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
};

