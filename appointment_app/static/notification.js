document.addEventListener("DOMContentLoaded", function () {
  var deleteButtons = document.querySelectorAll('.delete-button');
  deleteButtons.forEach(function (button) {
    button.addEventListener('click', function (event) {
      event.preventDefault();

      var confirmation = confirm("Are you sure you want to delete?");

      if (confirmation) {
        window.location.href = button.getAttribute("href");
      }
    });
  });

});