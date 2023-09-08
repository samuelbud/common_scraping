document.getElementById("searchInput").addEventListener("input", function() {
    let query = this.value.toLowerCase();
    let rows = document.querySelectorAll("tbody tr");
    rows.forEach(row => {
        let initiativeName = row.querySelector("td:nth-child(3)").textContent.toLowerCase();
        if (initiativeName.includes(query)) {
            row.querySelector("td:nth-child(3)").classList.add("highlight");
        } else {
            row.querySelector("td:nth-child(3)").classList.remove("highlight");
        }
    });
});
