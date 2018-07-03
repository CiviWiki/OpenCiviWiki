import { View } from "backbone.marionette";
import feedTemplate from 'templates/views/feed.html'

const FeedView = View.extend ({
    tagName: "feed",
    template: _.template(feedTemplate),

})

export default FeedView;
