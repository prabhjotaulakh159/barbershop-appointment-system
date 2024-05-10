// formValidation.js
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('myForm').addEventListener('submit', function (event) {
        var isValid = true;
        var username = document.getElementById('username').value;
        var email = document.getElementById('email').value;
        var age = document.getElementById('age').value;
        var phone = document.getElementById('phone').value;

        // Username validation
        if (!username.trim()) {
            isValid = false;
            document.getElementById('username').classList.add('error');
        } else {
            document.getElementById('username').classList.remove('error');
        }

        // Email validation
        if (!email.trim() || !/\S+@\S+\.\S+/.test(email)) {
            isValid = false;
            document.getElementById('email').classList.add('error');
        } else {
            document.getElementById('email').classList.remove('error');
        }

        // Age validation
        if (!age.trim() || isNaN(age) || age < 0 || age > 100) {
            isValid = false;
            document.getElementById('age').classList.add('error');
        } else {
            document.getElementById('age').classList.remove('error');
        }

        // Phone validation
        if (!/^\d{3}-\d{3}-\d{4}$/.test(phone)) {
            isValid = false;
            document.getElementById('phone').classList.add('error');
        } else {
            document.getElementById('phone').classList.remove('error');
        }

        if (!isValid) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    })
});
