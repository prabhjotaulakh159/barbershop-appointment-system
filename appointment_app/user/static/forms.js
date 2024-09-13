"use strict";

document.addEventListener('DOMContentLoaded', (e) => {
    const userTypeInput = document.getElementById('user-type');
    const payrateInput = document.getElementById('pay-rate');
    const specialityInput = document.getElementById('specialty-register');
    const specialityLabel = document.getElementById('specialityLabel');

    const renderProfessionalReservedFields = (e) => {
        if (e.target.value == 'Member') {
            payrateInput.style.display = 'none';
            specialityInput.style.display = 'none';
            specialityLabel.style.display = 'none';
        } else if (e.target.value == 'Professional') {
            payrateInput.style.display = 'block';
            specialityInput.style.display = 'block';
            specialityLabel.style.display = 'block';
        } else {
            throw new Error('Invalid value found for user type !');
        }
    };

    userTypeInput.addEventListener('click', renderProfessionalReservedFields);

    document.getElementById('user_form').addEventListener('submit', function (event) {
        var isValid = true;
        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;
        var confirmPassword = document.getElementById('confirm-password').value;
        var email = document.getElementById('email').value;
        var age = document.getElementById('age').value;
        var userType = document.getElementById('user-type').value;
        var phone = document.getElementById('phone').value;
        var address = document.getElementById('address').value;
        var payrateField = document.getElementById('pay-rate');

        // Username validation
        if (!username.trim()) {
            isValid = false;
            document.getElementById('username').classList.add('form-error');
            document.getElementById('username-error').innerText = 'Please enter a username';
        } else {
            document.getElementById('username').classList.remove('form-error');
            document.getElementById('username-error').innerText = '';
        }

        // Password validation
        if (!password.trim()) {
            isValid = false;
            document.getElementById('password').classList.add('form-error');
            document.getElementById('password-error').innerText = 'Please enter a password';
        } else if (password.length < 5) {
            isValid = false;
            document.getElementById('password').classList.add('form-error');
            document.getElementById('password-error').innerText = 'Password must be at least 5 characters long';
        } else {
            document.getElementById('password').classList.remove('form-error');
            document.getElementById('password-error').innerText = '';
        }

        // Confirm Password validation
        if (password !== confirmPassword) {
            isValid = false;
            document.getElementById('confirm-password').classList.add('form-error');
            document.getElementById('confirm-password-error').innerText = 'Passwords do not match';
        } else {
            document.getElementById('confirm-password').classList.remove('form-error');
            document.getElementById('confirm-password-error').innerText = '';
        }

        // Email validation
        if (!email.trim() || !/\S+@\S+\.\S+/.test(email)) {
            isValid = false;
            document.getElementById('email').classList.add('form-error');
            document.getElementById('email-error').innerText = 'Please enter a valid email';
        } else {
            document.getElementById('email').classList.remove('form-error');
            document.getElementById('email-error').innerText = '';
        }

        // Age validation
        if (!age.trim() || isNaN(age) || age < 0 || age > 100) {
            isValid = false;
            document.getElementById('age').classList.add('form-error');
            document.getElementById('age-error').innerText = 'Please enter a valid age';
        } else {
            document.getElementById('age').classList.remove('form-error');
            document.getElementById('age-error').innerText = '';
        }

        if (userType === "Professional" && age < 18) {
            isValid = false;
            document.getElementById('age').classList.add('form-error');
            document.getElementById('age-error').innerText = 'A professional must be at least 18 years old';
        } else {
            document.getElementById('age').classList.remove('form-error');
            document.getElementById('age-error').innerText = '';
        }

        // Phone validation
        if (!/^\d{3}-\d{3}-\d{4}$/.test(phone)) {
            isValid = false;
            document.getElementById('phone').classList.add('form-error');
            document.getElementById('phone-error').innerText = 'Please enter a valid phone in the correct formate';
        } else {
            document.getElementById('phone').classList.remove('form-error');
            document.getElementById('phone-error').innerText = '';
        }

        // address validation
        if (!address.trim()) {
            isValid = false;
            document.getElementById('address').classList.add('form-error');
            document.getElementById('address-error').innerText = 'Please enter an address';
        } else {
            document.getElementById('address').classList.remove('form-error');
            document.getElementById('address-error').innerText = '';
        }

        // payrate validation
        if (payrateField) {
            var payrate = payrateField.value;
            if (payrate.trim() && (isNaN(parseFloat(payrate)) || parseFloat(payrate) < 0)) {
                isValid = false;
                document.getElementById('pay-rate').classList.add('form-error');
                document.getElementById('payrate-error').innerText = 'Pay rate must be a valid number greater than or equal to 0';
            } else {
                document.getElementById('pay-rate').classList.remove('form-error');
                document.getElementById('payrate-error').innerText = '';
            }
        }

        if (!isValid) {
            event.preventDefault(); // Prevent form submission if validation fails
        }

    })
});



