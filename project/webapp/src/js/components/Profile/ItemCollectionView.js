import { CollectionView } from 'backbone.marionette';
import ThreadCard from '../Feed/ThreadCard';

const ItemCollectionView = CollectionView.extend({
  tagName: 'div',
  className: 'ItemCollectionView',
  childView: ThreadCard,
});

export default ItemCollectionView;
