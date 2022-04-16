$('.cd-popup-yes').on('click', function () {
    $.ajax({
        type: "POST",
        url: '/api/deleteuser',
        data: {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        },
        success: function (response) {
            window.location.assign("/");
            console.log('success');
        },
        error: function (response) {
            console.log('error');
        }
    });
});
// Confirmation dialog (HTML/CSS/JS) from https://codyhouse.co/gem/simple-confirmation-popup
jQuery(document).ready(function ($) {
    //open popup
    $('.cd-popup-trigger').on('click', function (event) {
        event.preventDefault();
        $('.cd-popup').addClass('is-visible');
    });

    //close popup
    $('.cd-popup').on('click', function (event) {
        if ($(event.target).is('.cd-popup-close') || $(event.target).is('.cd-popup') || $(event.target).is('.cd-popup-no')) {
            event.preventDefault();
            $(this).removeClass('is-visible');
        }
    });
    //close popup when clicking the esc keyboard button
    $(document).keyup(function (event) {
        if (event.which == '27') {
            $('.cd-popup').removeClass('is-visible');
        }
    });
});