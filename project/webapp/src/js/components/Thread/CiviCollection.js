import { CollectionView } from 'backbone.marionette';
import CiviView from './Civi';

const CiviCollectionView = CollectionView.extend({
  tagName: 'div',
  className: 'CiviCollection',
  childView: CiviView,

  childViewOptions() {
    return { templateContext: this.getOption('templateContext') };
  },
});

export default CiviCollectionView;
