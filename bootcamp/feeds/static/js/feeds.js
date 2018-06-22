$(function () {
    var page_title = $(document).attr("title");
    var shared_post;

    // WebSocket connection management block.
    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/feeds/";
    var webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);

    // Helpful debugging
    webSocket.socket.onopen = function () {
        console.log("Connected to feeds stream");
    };

    webSocket.socket.onclose = function () {
        console.log("Disconnected from feeds stream");
    };

    webSocket.listen(function(event) {
        if (event.activity === "new_feed") {
            if (event.username != currentUser) {
                check_new_feeds();
            }
        } else if (event.activity === "liked") {
            console.log(event.username + " just " + event.activity);
            update_feeds();
        } else if (event.activity === "commented") {
            console.log(event.username + " just " + event.activity);
            track_comments();
            update_feeds();
        }
    });

    function hide_stream_update() {
        $(".stream-update").hide();
        $(".stream-update .new-posts").text("");
        $(document).attr("title", page_title);
    }

    $("ul.stream").on("click", ".like", function () {
        var post = $(this).closest(".post");
        var li = $(post).closest("li");
        var feed = $(li).attr("feed-id");
        var csrf = $(li).attr("csrf");
        $.ajax({
            url: '/feeds/like/',
            data: {
                'feed': feed,
                'csrfmiddlewaretoken': csrf
            },
            type: 'post',
            cache: false,
            success: function (data) {
                if ($(".like", li).hasClass("text-primary")) {
                    $(".like", li).removeClass("text-primary");
                    $(".like", li).removeClass("active");
                    // $(".like .material-icons", li).text("favorite_border");
                }
                else {
                    $(".like", li).addClass("active");
                    $(".like", li).addClass("text-primary");
                    // $(".like .material-icons", li).text("favorite");
                }
                $(".like .like-count", li).text(data);
            }
        });
        return false;
    });

    $("ul.stream").on("click", ".share", function () {
        var post = $(this).closest(".post");
        var li = $(post).closest("li");
        var feed = $(li).attr("feed-id");
        $("#share-form input[name='feed']").val(feed);
        shared_post = li;
    });


    $('#share-modal').on('shown.bs.modal', function() {
        textarea = $("#share-form textarea[name='post']");
        textarea.val("");
    });

    $("#share-modal").on("click", "#btn-share", function () {
        $.ajax({
            url: '/feeds/share/',
            data: $("#share-form").serialize(),
            type: 'post',
            cache: false,
            success: function (data) {
                $(".btn-cancel-share").click();
                $(".share .share-count", shared_post).text(data);
            }
        });
        return false;
    });

    $("ul.stream").on("click", ".comment", function () {
        var post = $(this).closest(".post");
        if ($(".comments", post).hasClass("tracking")) {
            $(".comments", post).slideUp();
            $(".comments", post).removeClass("tracking");
        }
        else {
            $(".comments", post).show();
            $(".comments", post).addClass("tracking");
            $(".comments input[name='post']", post).focus();
            var feed = $(post).closest("li").attr("feed-id");
            $.ajax({
                url: '/feeds/comment/',
                data: { 'feed': feed },
                cache: false,
                beforeSend: function () {
                    $("ol", post).html("<li class='loadcomment'><img src='/static/img/loading.gif'></li>");
                },
                success: function (data) {
                    $("ol", post).html(data);
                    $(".comment-count", post).text($("ol li", post).not(".empty").length);
                }
            });
        }
        return false;
    });

    $("ul.stream").on("keydown", ".comments input[name='post']", function (evt) {
        var keyCode = evt.which?evt.which:evt.keyCode;
        if (keyCode == 13) {
            var form = $(this).closest("form");
            var container = $(this).closest(".comments");
            var input = $(this);
            $.ajax({
                url: '/feeds/comment/',
                data: $(form).serialize(),
                type: 'post',
                cache: false,
                beforeSend: function () {
                    $(input).val("");
                },
                success: function (data) {
                    $("ol", container).html(data);
                    var post_container = $(container).closest(".post");
                    $(".comment-count", post_container).text($("ol li", container).length);
                }
            });
            return false;
        }
    });

    var load_feeds = function () {
        if (!$("#load_feed").hasClass("no-more-feeds")) {
            var page = $("#load_feed input[name='page']").val();
            var next_page = parseInt($("#load_feed input[name='page']").val()) + 1;
            $("#load_feed input[name='page']").val(next_page);
            $.ajax({
                url: '/feeds/load/',
                data: $("#load_feed").serialize(),
                cache: false,
                beforeSend: function () {
                    $(".load").show();
                },
                success: function (data) {
                    if (data.length > 0) {
                        $("ul.stream").append(data);
                        $(".feed_gallery").justifiedGallery({
                            rowHeight : 160,
                            lastRow : 'justify',
                            margins : 0
                        });
                    }
                    else {
                        $("#load_feed").addClass("no-more-feeds");
                    }
                },
                complete: function () {
                    $(".load").hide();
                }
            });
        }
    };

    $("#load_feed").bind("enterviewport", load_feeds).bullseye();

    $(".stream-update a").click(function () {
        var last_feed = $(".stream li:first-child").attr("feed-id");
        var feed_source = $("#feed_source").val();
        $.ajax({
            url: '/feeds/load_new/',
            data: {
                'last_feed': last_feed,
                'feed_source': feed_source
            },
            cache: false,
            success: function (data) {
                $("ul.stream").prepend(data);
                $(".feed_gallery").justifiedGallery({
                    rowHeight : 160,
                    lastRow : 'justify',
                    margins : 0
                });
            },
            complete: function () {
                hide_stream_update();
            }
        });
        return false;
    });

    $("input,textarea").attr("autocomplete", "off");

    $("ul.stream").on("click", ".remove-feed", function () {
        var li = $(this).closest("li");
        var feed = $(li).attr("feed-id");
        var csrf = $(li).attr("csrf");
        $.ajax({
            url: '/feeds/remove/',
            data: {
                'feed': feed,
                'csrfmiddlewaretoken': csrf
            },
            type: 'post',
            cache: false,
            success: function (data) {
                $(li).fadeOut(400, function () {
                    $(li).remove();
                });
            }
        });
    });

    function update_feeds () {
        var first_feed = $(".stream li:first-child").attr("feed-id");
        var last_feed = $(".stream li:last-child").attr("feed-id");
        var feed_source = $("#feed_source").val();

        if (first_feed != undefined && last_feed != undefined) {
            $.ajax({
                url: '/feeds/update/',
                data: {
                    'first_feed': first_feed,
                    'last_feed': last_feed,
                    'feed_source': feed_source
                },
                cache: false,
                success: function (data) {
                    $.each(data, function(id, feed) {
                            var li = $("li[feed-id='" + id + "']");
                            $(".like-count", li).text(feed.likes);
                            $(".comment-count", li).text(feed.comments);
                    });
                },
            });
        }
    };

    function track_comments () {
        $(".tracking").each(function () {
            var container = $(this);
            var feed = $(this).closest("li").attr("feed-id");
            $.ajax({
                url: '/feeds/track_comments/',
                data: {'feed': feed},
                cache: false,
                success: function (data) {
                    if (data != 0) {
                        $("ol", container).html(data);
                        var post_container = $(container).closest(".post");
                        $(".comment-count", post_container).text($("ol li", container).length);
                    }
                }
            });
        });
    };

    function check_new_feeds () {
        var last_feed = $(".stream li:first-child").attr("feed-id");
        var feed_source = $("#feed_source").val();
        if (last_feed != undefined) {
            $.ajax({
                url: '/feeds/check/',
                data: {
                    'last_feed': last_feed,
                    'feed_source': feed_source
                },
                cache: false,
                success: function (data) {
                    if (parseInt(data) > 0) {
                        $(".stream-update .new-posts").text(data);
                        $(".stream-update").show();
                        $(document).attr("title", "(" + data + ") " + page_title);
                    }
                },
            });
        }
    };
});
