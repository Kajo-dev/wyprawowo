const avatarInput = document.querySelector('.file-input');
const avatarPreview = document.querySelector('.avatar-image')

avatarInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            avatarPreview.src = e.target.result;
            avatarPreview.style = 'height: 100%;'
        }
        reader.readAsDataURL(file);
    }
})