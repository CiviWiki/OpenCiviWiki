import { View } from 'backbone.marionette';
import baseTemplate from 'Templates/components/Settings/location_label.html';

const LocationLabel = View.extend({
  tagName: 'div',
  className: 'LocationLabel section',
  template: baseTemplate,
});

export default LocationLabel;
