cw = cw || {};

var notifications_data = [];
cw.NotificationView =  BB.View.extend({
    el: '.notifications-list',
    template: _.template($('#notification-base-template').html()),

    initialize: function (options) {
        this.options = options || {};
        this.notifications_data=[];
        this.initialNotificationShown = false;
        this.render();
    },

    render: function () {
        var renderData = {
            notification: this.notifications_data
        };

        this.$el.empty().append(this.template(renderData));
    },

    events: {
        'click .test-button': 'dd',
    },



        // $.ajax({
        //     url: 'inbox/notifications/api/mark-all-as-read/',
        //     success: function (response) {
        //         console.log('success');
        //     },
        //     error: function(r){
        //         console.log('error');
        //     }
        // });

});
var notificationsView = new cw.NotificationView();

$('#item-notifications').on('click', function () {
    $.ajax({
        type: "GET",
        url: '/inbox/notifications/mark-all-as-read/',
        success: function (response) {
            $('#notify-count-wrapper').addClass('hide');
            $('#notify-icon').html('notifications_none').removeClass('active');
            console.log('success');
        },
        error: function(r){
            console.log('error');
        }
    });
});

var render_notifications = function(data) {
    var unreadCount = parseInt(data.unread_count);
    if (unreadCount === 0) {
        $('#notify-count-wrapper').addClass('hide');
        $('#notify-icon').html('notifications_none').removeClass('active');
    } else {
        $('#notify-count-wrapper').removeClass('hide');
        $('#notify-icon').html('notifications').addClass('active');

        this.new_notifications = [];
        var notified = false;
        if (data.unread_list.length > 5 && !notificationsView.initialNotificationShown) {
            Materialize.toast("You have " + data.unread_list.length +" new notifications", 5000);
            notificationsView.initialNotificationShown = true;
            notified = true;
        }
        _.each(data.unread_list, function(n) {
            console.log(data.unread_list);
            var old_notification = _.findWhere(notificationsView.notifications_data, {id: n.id});
            var json_Data = JSON.parse(n.data);
            if (!old_notification && !notified) {
                if (json_Data !== null){
                    Materialize.toast(json_Data.popup_string, 5000);
                } else {
                    Materialize.toast("You have a new notification", 5000);
                }
            }
            json_Data = json_Data || {};
            var date = new Date(n.timestamp);
            var date_string = date.toDateString();

            var saveData = {
                id: n.id,
                time: date_string,
                popup_string: json_Data.popup_string,
                link: json_Data.link
            }
            this.new_notifications.push(saveData);

        }, this);

        notificationsView.notifications_data = this.new_notifications;
        notificationsView.render();
    }
};
