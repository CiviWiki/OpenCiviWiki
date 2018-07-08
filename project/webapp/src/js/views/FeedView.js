import { View } from "backbone.marionette";
import feedTemplate from "templates/layouts/feed.html";

import "styles/feed.less";

const FeedView = View.extend({
  template: feedTemplate,

  regions: {
    categoryModal: "categories-modal-holder",
    newThreadModal: "new-thread-modal-holder",
    trending: "#trending-list",
    feed: "#feed-list",
    drafts: "#drafts-list"
  },

  showIndex() {
    this.showChildView("main", new IndexView());
    Bb.history.navigate(""); // Update the location bar
  },

  showNoteList() {
    this.showChildView(
      "main",
      new NoteListView({
        collection: this.collection
      })
    );
    Bb.history.navigate("notes"); // Update the location bar
  }

  // showNote(noteId) {
  //   const model = new NoteModel({ id: noteId });
  //   this.showChildView('main', new NoteDetailView({
  //     model: model
  //   }));
  //   model.fetch();
  //   Bb.history.navigate(`notes/${noteid}`);  // Update the location bar
  // },

  // showEditNote(noteId) {
  //   const model = new NoteModel({ id: noteId });
  //   this.showChildView('main', new NoteEditView({
  //     model: model
  //   }));
  //   model.fetch();
  //   Bb.history.navigate(`notes/${noteId}/edit`);  // Update the location bar
  // }
});

export default FeedView