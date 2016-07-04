cw = {};
BB = Backbone;

_.templateSettings = {
    evaluate: /\{\{#(.+?)\}\}/g,
    interpolate: /\{\{=(.+?)\}\}/g,
    escape: /\{\{(?!#|=)(.+?)\}\}/g
};

// cw.underscorePartial = function (templateString, data) {
//     return _.template()
// }
