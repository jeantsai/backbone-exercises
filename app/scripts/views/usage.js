/*global Exercises, Backbone, JST*/

Exercises.Views = Exercises.Views || {};

(function () {
  'use strict';

  Exercises.Views.Usage = Backbone.View.extend({

    template: JST['app/scripts/templates/usage.ejs'],

    tagName: 'div',

    id: '',

    className: '',

    events: {},

    initialize: function () {
      this.listenTo(this.model, 'change', this.render);
    },

    render: function () {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    }

  });

})();
