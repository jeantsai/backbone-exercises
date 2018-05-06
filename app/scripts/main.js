/*global exercises, $*/


window.Exercises = {
  Models: {},
  Collections: {},
  Views: {},
  Routers: {},
  init: function () {
    'use strict';

    var router = new Exercises.Routers.Blog();
  }
};

$(document).ready(function () {
  'use strict';
  Exercises.init();
});
