import { View } from 'backbone.marionette';
import baseTemplate from 'Templates/components/Settings/personal.html';
import LocationLabel from './LocationLabel';

const Personal = View.extend({
  tagName: 'div',
  className: 'Personal',
  template: baseTemplate,

  regions: {
    locationLabel: '#location-label-container',
  },

  onRender() {
    this.showChildView('locationLabel', new LocationLabel({ model: this.model }));
  },
});

export default Personal;
