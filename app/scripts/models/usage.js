/*global Exercises, Backbone*/

Exercises.Models = Exercises.Models || {};

(function () {
  'use strict';

  Exercises.Models.Usage = Backbone.Model.extend({

    urlRoot: 'http://localhost:5000/ce/api/v1.0/usages',

    initialize: function() {
    },

    defaults: {
    }

  });

})();
