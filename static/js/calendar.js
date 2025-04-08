document.addEventListener("DOMContentLoaded", function() {
    flatpickr("#start_date", {
        dateFormat: "Y-m-d",  // Specifies the format to be displayed as Year-Month-Day
    });
    flatpickr("#end_date", {
        dateFormat: "Y-m-d",
    });
});
