$(function () {
  var page_title = $(document).attr("title");
  
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

  $("body").keydown(function (evt) {
    var keyCode = evt.which?evt.which:evt.keyCode;
    if (evt.ctrlKey && keyCode == 80) {
        $(".btn-compose").click();
        return false;
    }
  });

  $("#compose-form textarea[name='post']").keydown(function (evt) {
    var keyCode = evt.which?evt.which:evt.keyCode;
    if (evt.ctrlKey && (keyCode == 10 || keyCode == 13)) {
        $(".btn-post").click();
    }
  });

  $("#compose-form textarea[name='post']").keyup(function () {
    $(this).count(255);
  });

  $('#compose-modal').on('shown.bs.modal', function() {
    $("#compose-form textarea[name='post']").focus();
  })

  $("#btn-post").click(function () {
    var last_feed = $(".stream li:first-child").attr("feed-id");
    if (last_feed == undefined) {
        last_feed = "0";
    }
    $("#compose-form input[name='last_feed']").val(last_feed);
    $.ajax({
        url: '/feeds/post/',
        data: $("#compose-form").serialize(),
        type: 'post',
        cache: false,
        success: function (data) {
            $("ul.stream").prepend(data);
            $("#compose-form .qq-upload-list-selector").remove();
            $(".btn-cancel-compose").click();
            $(".feed_gallery").justifiedGallery({
                rowHeight : 160,
                lastRow : 'justify',
                margins : 0
            });
            $(".stream-update").hide();
            $(".stream-update .new-posts").text("");
            $(document).attr("title", page_title);
        }
    });
  });

  $(".btn-cancel-compose").click(function () {
    $("#compose-form textarea[name='post']").val("");
  });
});