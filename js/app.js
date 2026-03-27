/* Daily Papers - Client-side filtering and language toggle */

(function () {
    "use strict";

    let currentLang = "en";

    // --- Language Toggle ---
    const langBtn = document.getElementById("lang-toggle");
    if (langBtn) {
        langBtn.addEventListener("click", function () {
            currentLang = currentLang === "en" ? "ko" : "en";
            langBtn.textContent = currentLang === "en" ? "KO/EN" : "EN/KO";
            document.querySelectorAll(".summary-en").forEach(function (el) {
                el.style.display = currentLang === "en" ? "" : "none";
            });
            document.querySelectorAll(".summary-ko").forEach(function (el) {
                el.style.display = currentLang === "ko" ? "" : "none";
            });
        });
    }

    // --- Category Filters ---
    const chips = document.querySelectorAll(".chip[data-category]");
    let activeCategory = "all";

    chips.forEach(function (chip) {
        chip.addEventListener("click", function () {
            chips.forEach(function (c) { c.classList.remove("active"); });
            chip.classList.add("active");
            activeCategory = chip.dataset.category;
            applyFilters();
        });
    });

    // --- Search ---
    const searchInput = document.getElementById("search-input");
    let searchQuery = "";

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            searchQuery = searchInput.value.toLowerCase().trim();
            applyFilters();
        });
    }

    // --- Apply Filters ---
    function applyFilters() {
        var cards = document.querySelectorAll(".paper-card");
        cards.forEach(function (card) {
            var cats = (card.dataset.categories || "").split(",");
            var matchCategory = activeCategory === "all" || cats.indexOf(activeCategory) !== -1;

            var matchSearch = true;
            if (searchQuery) {
                var title = (card.querySelector(".card-title") || {}).textContent || "";
                var authors = (card.querySelector(".card-authors") || {}).textContent || "";
                var summary = (card.querySelector(".card-summary") || {}).textContent || "";
                var text = (title + " " + authors + " " + summary).toLowerCase();
                matchSearch = text.indexOf(searchQuery) !== -1;
            }

            card.classList.toggle("hidden", !(matchCategory && matchSearch));
        });
    }
})();
