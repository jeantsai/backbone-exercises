/*global Exercises, Backbone*/

Exercises.Collections = Exercises.Collections || {};

(function () {
  'use strict';

  Exercises.Collections.Blog = Backbone.Collection.extend({

    model: Exercises.Models.Blog,

    url: 'http://localhost:5000/ce/api/v1.0/courses',

    parse: function (data) {
      return data['courses'];
    }

  });

})();
