"use strict";

document.addEventListener('DOMContentLoaded', (e) => {
    const userTypeInput = document.getElementById('user-type');
    const payrateInput = document.getElementById('pay-rate');
    const specialityInput = document.getElementById('specialty');

    const renderProfessionalReservedFields = (e) => {
        if (e.target.value == 'Member') {
            payrateInput.style.display = 'none';
            specialityInput.style.display = 'none';
        } else if (e.target.value == 'Professional') {
            payrateInput.style.display = 'block';
            specialityInput.style.display = 'block';
        } else {
            throw new Error('Invalid value found for user type !');
        }
    };

    userTypeInput.addEventListener('click', renderProfessionalReservedFields);

});