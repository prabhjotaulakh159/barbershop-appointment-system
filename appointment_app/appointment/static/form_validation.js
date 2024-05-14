"use strict";

document.addEventListener('DOMContentLoaded', (e) => {
    var date = document.getElementById('date');
    var today = new Date().toISOString().split('T')[0];
    date.min = today;


    document.getElementById('appointment_form').addEventListener('submit', function (event) {
        var isValid = true;
        var date = document.getElementById('date').value;

        // date validation
        if (!date) {
            isValid = false;
            document.getElementById('date').style.backgroundColor='lightcoral';
            document.getElementById('date-error').innerText = 'Please enter a date';
            document.getElementById('date-error').style.color='red';
        } else {
            document.getElementById('date').style.backgroundColor='';
            document.getElementById('date-error').innerText = '';
        }

        if (!isValid) {
            event.preventDefault(); // Prevent form submission if validation fails
        }

    })
});



