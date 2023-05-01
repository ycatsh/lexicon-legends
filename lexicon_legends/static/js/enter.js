const wordInput = document.getElementById('wordInput');
const submitButton = document.getElementById('submitWord');

wordInput.addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); 
        submitButton.click(); 
    }
});