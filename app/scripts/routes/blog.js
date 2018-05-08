/*global Exercises, Backbone*/

Exercises.Routers = Exercises.Routers || {};

(function () {
  'use strict';

  Exercises.Routers.Blog = Backbone.Router.extend({
    routes: {
      "blog/new": "create",
      "blog/index": "index",
      "blog/:id/edit": "edit",
      "blog/:id/delete": "delete",
      "usages": "showUsages"
    },

    $container: $('#main'),

    $usagesContainer: $('#usages'),

    initialize: function () {
      this.collection = new Exercises.Collections.Blog();
      this.blogIndexView = new Exercises.Views.Blog({collection: this.collection});
      console.log('Fetching courses ...');
      this.collection.fetch({
        ajaxSync: true,
        success: function() {
          console.log('Courses has been fetched successfully.');
        }
      });
      Exercises.helpers.debug(this.collection);

      this.usages = new Exercises.Models.Usage;
      this.usagesView = new Exercises.Views.Usage({model: this.usages, el: this.$usagesContainer});
      console.log('Fetching usages ...');
      this.usages.fetch({
        ajaxSync: true,
        success: function () {
          console.log('Usage has been fetched successfully.');
          // router.showUsages();
        }
      });
    },

    create: function () {
      var view = new Exercises.Views.BlogAdd({
        collection: this.collection,
        model: new Exercises.Models.Blog()
      });
      this.$container.html(view.render().el);
    },

    delete: function (id) {
      var blog = this.collection.get(id);
      blog.destroy();
      this.index();
    },

    edit: function (id) {
      var view = new Exercises.Views.BlogEdit({model: this.collection.get(id)});
      this.$container.html(view.render().el);
    },

    index: function () {
      this.blogIndexView.render();
    },

    showUsages: function() {
      this.$usagesContainer.html(this.usagesView.render().el);
    }
  });

})();
