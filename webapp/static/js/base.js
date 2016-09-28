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
};

cw.initGlobalNav = function () {
    var $floaty = $('.floaty'),
        $logout = $('.svg-logout'),
        $feed = $('.svg-feed'),
        $account = $('.svg-account');

    $floaty.on('mouseover', function() {
        $floaty.addClass('is-active');
    });

    $floaty.on('mouseout', function() {
        $floaty.removeClass('is-active');
    });

    $logout.on('click', function () {
        window.location.href = '/auth/logout';
    });

    $feed.on('click', function () {
        window.location.href = '/';
    });

    $account.on('click', function () {
        window.location.href = '/profile/' + current_user; //TODO: username is not current loggedin user
    });
};
