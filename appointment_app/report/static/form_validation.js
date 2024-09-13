"use strict";

document.addEventListener('DOMContentLoaded', (e) => {
    document.getElementById('report_form').addEventListener('submit', function (event) {
        var isValid = true;
        var date = document.getElementById('report').value;

        // date validation
        if (!date) {
            isValid = false;
            document.getElementById('report').style.backgroundColor='lightcoral';
            document.getElementById('report-error').innerText = 'Please enter a report';
            document.getElementById('report-error').style.color='red';
        } else {
            document.getElementById('report').style.backgroundColor='';
            document.getElementById('report-error').innerText = '';
        }

        if (!isValid) {
            event.preventDefault(); // Prevent form submission if validation fails
        }

    })
});



