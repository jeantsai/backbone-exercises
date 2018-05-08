/*global Exercises, Backbone, JST*/

Exercises.Views = Exercises.Views || {};

(function () {
  'use strict';

  // Blog Index View
  Exercises.Views.Blog = Backbone.View.extend({

    template: JST['app/scripts/templates/blog-index.ejs'],

    el: $('#main'),

    initialize: function () {
      this.listenTo(this.collection, 'change', this.render);
      this.listenTo(this.collection, 'sync', this.render);
    },

    render: function () {
      console.log('Rending BlogIndex ...');
      this.$el.html(this.template({
        blogs: this.collection.toJSON()
      }));
      return this;
    }

  });

  // Blog Add View
  Exercises.Views.BlogAdd = Backbone.View.extend({
    // functions to fire on events
    // here we are blocking the submission of the form, and handling it ourself
    events: {
      "click button.save": "save",
      "keyup input": "validate",
      "keyup textarea": "validate"
    },

    template: JST['app/scripts/templates/blog-form.ejs'],

    initialize: function (options) {
      this.model.bind('invalid', Exercises.helpers.showErrors, Exercises.helpers);
    },

    save: function (event) {
      event.stopPropagation();
      event.preventDefault();

      // update our model with values from the form
      this.model.set({
        title: this.$el.find('input[name=title]').val(),
        description: this.$el.find('input[name=description]').val(),
        done: this.$el.find('input[name=done]').is(':checked')
      });

      if (this.model.isValid()) {
        // add it to the collection
        this.collection.add(this.model);
        // save it
        this.model.save();
        // redirect back to the index
        Backbone.history.navigate("blog/index", {trigger: true});
      }
    },

    // populate the html to the dom
    render: function () {
      this.$el.html(
        this.template(this.model.toJSON())
      );
      return this;
    }
  });


  Exercises.Views.BlogEdit = Backbone.View.extend({
    // functions to fire on events
    events: {
      "click button.save": "save"
    },

    // the template
    template: JST['app/scripts/templates/blog-form.ejs'],

    initialize: function (options) {
      this.model.bind('invalid', Exercises.helpers.showErrors, Exercises.helpers);
      this.model.bind('invalid', this.invalid, this);
    },

    invalid: function () {
      this.$el.find('a.cancel').hide();
    },

    save: function (event) {
      event.stopPropagation();
      event.preventDefault();

      // update our model with values from the form
      this.model.set({
        // id: this.$el.find('input[name=id]').val(),
        title: this.$el.find('input[name=title]').val(),
        description: this.$el.find('input[name=description]').val(),
        done: this.$el.find('input[name=done]').is(':checked')
      });

      if (this.model.isValid()) {
        this.model.save();
        Backbone.history.navigate("blog/index", {trigger: true});
      }
    },

    // populate the html to the dom
    render: function () {
      this.$el.html( this.template( this.model.toJSON() ) );
      return this;
    }
  });

})();
