document.querySelectorAll(".dropdown-item").forEach(x => {
    x.addEventListener('click', function () {
        let button = document.querySelector("#dropdownMenuButton");

        let oldSelection = button.innerHTML;
        button.innerHTML = x.innerHTML;
        x.innerHTML = oldSelection;
    })
})

$(".dropdown-item:not(.topic)").on('click', function() {
    $("#dropdownMenuButton").dropdown("toggle");
});

$("#ask").on('click', function () {
    $("#dropdownMenuButton").innerHTML
})

// Fix for dropdown not working bug
$(document).ready(function() {
    $(".dropdown-toggle").dropdown();
});