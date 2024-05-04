document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("filter").addEventListener("change", function () {
        var filter = this.value;
        var searchInput = document.getElementById("search");

        if (filter === "slot") {
            var selectTime = document.createElement("select");
            selectTime.name = "search";
            selectTime.id = "search";
            var times = [
                { value: '10-11', label: '10am - 11am' },
                { value: '11-12', label: '11am - 12pm' },
                { value: '12-1', label: '12pm - 1pm' },
                { value: '1-2', label: '1pm - 2pm' },
                { value: '2-3', label: '2pm - 3pm' },
                { value: '3-4', label: '3pm - 4pm' }
            ];

            times.forEach(function(time) {
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
