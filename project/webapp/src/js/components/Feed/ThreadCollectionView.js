import { CollectionView } from "backbone.marionette";
import ThreadCard from "../Thread/Card";

const ThreadCollectionView = CollectionView.extend({
  tagName: "div",
  className: "ThreadCollectionView",
  childView: ThreadCard,
});

export default ThreadCollectionView;
