$(function () {
  $.fn.count = function (limit) {
    var length = limit - $(this).val().length;
    var form = $(this).closest("form");
    if (length <= 0) {
      $(".form-group", form).addClass("has-error");
    }
    else {
      $(".form-group", form).removeClass("has-error");
    }
    $(".help-count", form).text(length);
  };

  $(window).scroll(function() {
    if ($(window).scrollTop() > 0) {
      $(".toolbar-waterfall").addClass("waterfall");
    } else {
      $(".toolbar-waterfall").removeClass("waterfall");
    }
  });
});