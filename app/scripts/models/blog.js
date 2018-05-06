/*global Exercises, Backbone*/

Exercises.Models = Exercises.Models || {};

(function () {
  'use strict';

  Exercises.Models.Blog = Backbone.Model.extend({

    initialize: function() {
    },

    defaults: {
      title: '',
      description: '',
      done: false
    },

    validate: function(attrs, options) {
    },

    // parse: function(response, options)  {
    //   return response;
    // }
  });

})();
