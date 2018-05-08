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
      var usagesModel = this.model;
      this.listenTo(this.model, 'change', this.render);
      $(document).on('click', '[data-target="#myApiUsage"]', function(e) {
        usagesModel.fetch({
          ajaxSync: true,
          success: function() {
            console.info("Fetched usages for showing in a modal window");
          }
        });
      });
    },

    render: function () {
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    }

  });

})();
