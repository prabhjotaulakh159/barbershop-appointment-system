document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("search-user").addEventListener("click", (e) => {
        e.preventDefault();
        const user = Array
            .from(document.getElementsByTagName("td"))
            .filter(u => u.getAttribute("data-title") === 'Name') 
            .filter(e => e.textContent === document.getElementById('search-name').value)
            [0];
        if (!user) return;
        const firstRow = document.getElementsByTagName("tbody")[0].children[0];
        firstRow.style.backgroundColor = "white";
        document.getElementsByTagName("tbody")[0].insertBefore(user.parentElement, firstRow);
        user.parentElement.style.backgroundColor = "orange";
    });
});
