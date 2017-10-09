cw = {};
BB = Backbone;

_.templateSettings = {
    evaluate: /\{\{#(.+?)\}\}/g,
    interpolate: /\{\{=(.+?)\}\}/g,
    escape: /\{\{(?!#|=)(.+?)\}\}/g
};

cw.underscorePartial = function (templateSelector, data) {
    return _.template($('#' + templateSelector).html())(data);
};

cw.checkForEnter = function (e) {
    if (e.which == 13 && !e.shiftKey) {
        e.preventDefault();
        $(e.target).blur();
    }
};

cw.materializeShit = function () {
    Materialize.updateTextFields();
    $('ul.tabs').tabs();
    $('select').material_select();
};

cw.initGlobalNav = function () {
    var $floaty = $('.floaty'),
        $logout = $('#item-logout'),
        $feed = $('#item-feed'),
        $notifications = $('#item-notifications'),
        $account = $('#item-account');

    $floaty.on('mouseover', function() {
        $floaty.addClass('is-active');
    });

    $floaty.on('mouseout', function() {
        $floaty.removeClass('is-active');
    });

    $logout.on('click', function () {
        window.location.href = '/auth/logout';
    });

    $notifications.on('click', function () {
        $('.notifications-modal').openModal();
    });

    $feed.on('click', function () {
        window.location.href = '/';
    });


    $account.on('click', function () {
        window.location.href = '/profile/';
    });

};

//CSRF Setup
cw.csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", cw.csrftoken);
        }
    }
});
