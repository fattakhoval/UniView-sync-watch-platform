const inputField = document.getElementById('join_link');
const redirectButton = document.getElementById('redirectButton');

redirectButton.addEventListener('click', () => {
    const inputValue = inputField.value.trim();
    console.log(inputValue);
    if (inputValue) {
        window.location.href = inputValue;
    }
});