/*global Exercises, Backbone*/

Exercises.Routers = Exercises.Routers || {};

(function () {
  'use strict';

  Exercises.Routers.Blog = Backbone.Router.extend({
    routes: {
      "/": "index",
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
      var router = this;
      this.collection.fetch({
        ajaxSync: true,
        success: function() {
          console.log('Courses has been fetched successfully.')
          router.index();
        }
      });
      Exercises.helpers.debug(this.collection);

      this.usages = new Exercises.Models.Usage;
      this.usages.fetch({
        ajaxSync: true,
        success: function () {
          router.showUsages();
        }
      });

      // start backbone watching url changes
      Backbone.history.start();
    },

    create: function () {
      var view = new Exercises.Views.BlogAdd({
        collection: this.collection,
        model: new Exercises.Models.Blog()
      });
      this.$container.html(view.render().el);
      // $('.myid').val(_.random(0, 10000));
    },

    delete: function (id) {
      var blog = this.collection.get(id);
      blog.destroy();
      Backbone.history.navigate("blog/index", {trigger: true});
    },

    edit: function (id) {
      var view = new Exercises.Views.BlogEdit({model: this.collection.get(id)});
      this.$container.html(view.render().el);
    },

    index: function () {
      var view = new Exercises.Views.Blog({collection: this.collection});
      this.$container.html(view.render().el);
    },

    showUsages: function() {
      var view = new Exercises.Views.Usage({model: this.usages});
      this.$usagesContainer.html(view.render().el);
    }
  });

})();
