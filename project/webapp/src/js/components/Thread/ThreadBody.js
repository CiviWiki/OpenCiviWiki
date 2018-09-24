import { View } from 'backbone.marionette';
import threadBodyTemplate from 'Templates/components/Thread/thread_body.html';
import ThreadNavView from './ThreadNav';

const ThreadBodyView = View.extend({
  tagName: 'div',
  className: 'thread-body',
  template: threadBodyTemplate,

  regions: {
    threadNavHolder: '.thread-nav',
  },

  onRender() {
    this.threadNavRender();
  },
  // // Renders thread navbar element independently of main body.
  // // Useful for updating after thread edits are saved.
  threadNavRender() {
    // const view = this;
    // const navRenderData = {
    //   is_draft: this.is_draft,
    // };
    // view.$('.thread-nav').empty().append(this.navTemplate(navRenderData));
    // view.$('.main-thread').on('scroll', () => {
    //   view.processCiviScroll();
    // });
    this.showChildView('threadNavHolder', new ThreadNavView({ model: this.model }));
  },
});

export default ThreadBodyView;
