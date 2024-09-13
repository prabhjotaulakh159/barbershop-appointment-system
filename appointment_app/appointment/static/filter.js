document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("filter").addEventListener("change", function () {
        var filter = this.value;
        var searchInput = document.getElementById("search");

        if (filter === "slot") {
            var selectTime = document.createElement("select");
            selectTime.name = "search";
            selectTime.id = "search";
            var times = [
                { value: '10:00 - 11:00', label: '10am - 11am' },
                { value: '11:00 - 12:00', label: '11am - 12pm' },
                { value: '12:00 - 13:00', label: '12pm - 1pm' },
                { value: '13:00 - 14:00', label: '1pm - 2pm' },
                { value: '14:00 - 15:00', label: '2pm - 3pm' },
                { value: '15:00 - 16:00', label: '3pm - 4pm' }
            ];

            times.forEach(function (time) {
                var option = document.createElement("option");
                option.value = time.value;
                option.text = time.label;
                selectTime.appendChild(option);
            });

            searchInput.parentNode.replaceChild(selectTime, searchInput);

        } else {
            var inputText = document.createElement("input");
            inputText.type = "number";
            inputText.name = "search";
            inputText.id = "search";
            inputText.placeholder = "Enter ID";

            searchInput.parentNode.replaceChild(inputText, searchInput);
        }
    });
});
