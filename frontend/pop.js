$(document).ready(function() {
    $("#open-popup").click(function() {
        $("#overlay").fadeIn();
        $("#popup").fadeIn();
    });

    $("#close-popup, #overlay").click(function() {
        $("#overlay").fadeOut();
        $("#popup").fadeOut();
    });
});
