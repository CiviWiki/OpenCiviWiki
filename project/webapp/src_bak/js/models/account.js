const AccountModel = Bb.Model.extend({
    defaults: function() {
        return {
            profile_image: "",
            username: "",
            first_name: "",
            last_name: "",
            about_me: "",
            location: "",
            history: [],
            followers: [],
            following: [],
            issues: [],
            representatives: []
        };
    },
    url: function () {
        if (! this.user ) {
            throw new Error("This is a race condition! and why we can't have nice things :(");
        }
        return '/api/account_profile/' + this.user + '/';
    },

    initialize: function (model, options) {
        options = options || {};
        this.user = options.user;
    }
});

export default AccountModel;