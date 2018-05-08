/*global exercises, $*/


window.Exercises = {
  Models: {},
  Collections: {},
  Views: {},
  Routers: {},
  init: function () {
    'use strict';

    var router = new Exercises.Routers.Blog();
    // start backbone watching url changes
    Backbone.history.start();
  }
};

$(document).ready(function () {
  'use strict';
  console.info('Starting Course Evaluation SPA ... ');
  Exercises.init();
});
