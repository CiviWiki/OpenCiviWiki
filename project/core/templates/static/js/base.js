cw = {};

Materialize = M


BB = Backbone;

_.templateSettings = {
    evaluate: /\{\{#(.+?)\}\}/g,
    interpolate: /\{\{=(.+?)\}\}/g,
    escape: /\{\{(?!#|=)(.+?)\}\}/g
};

$( document ).ready(function() {
    Materialize.AutoInit()
});

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
    $( document ).ready(function() {
        Materialize.AutoInit()
        Materialize.updateTextFields();
      /*replaced with AutoInit()
        //$('ul.tabs').tabs();
        //$('select').formSelect();    
      */  
    });
};

cw.initGlobalNav = function () {

    var $notifications = $('#item-notifications');

    /* //replaced with trigger-button
    $notifications.on('click', function () {
        $('.notifications-modal').modal('open');
    });
    */

    var $navMenuButton = $('#js-toggle-menu');
    $navMenuButton.on('click', function (event) {
        event.stopPropagation()
        $('#js-dropdown-menu').toggleClass('hide');
        $('.js-dropdown-icon').toggleClass('hide');

        $(document).on('click', function(event){
            $target = $(event.target);

            if ($target.parents('#js-dropdown-menu').length==0){
                $('#js-dropdown-menu').addClass('hide');
                $('.js-dropdown-icon').toggleClass('hide');
                $(this).unbind(event);
            }
        })


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
