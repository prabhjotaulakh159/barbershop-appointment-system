document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("switch").addEventListener("change", function () {
        var checked = this.checked;
        var users = document.getElementsByClassName("users");
        var appointments = document.getElementsByClassName("appointments");

        for (var i = 0; i < users.length; i++) {
            if (checked) {
                users[i].style.display = "none";
            } else {
                users[i].style.display = "block";
            }
        }

        for (var i = 0; i < appointments.length; i++) {
            if (checked) {
                appointments[i].style.display = "block";
            } else {
                appointments[i].style.display = "none";
            }
        }

    });
});
