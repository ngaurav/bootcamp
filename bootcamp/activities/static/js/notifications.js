$(function () {
    $('#notifications').on('show.bs.dropdown', function () {
        $.ajax({
            url: '/notifications/last/',
            beforeSend: function () {
            $("#notifications-content").html("<div class='tile'><div class='tile-inner text-black'><strong>Notifications</strong></div></div><div class='tile'><div class='tile-inner text-black text-center'><img src='/static/img/loading.gif'></div>");
            $("#notifications-badge").removeAttr("data-badge");
            },
            success: function (data) {
            $("#notifications-content").html(data);
            }
        });
    });

    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/notifications/";
    var webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);

    // Helpful debugging
    webSocket.socket.onopen = function () {
        console.log("Connected to notifications stream");
    };

    webSocket.socket.onclose = function () {
        console.log("Disconnected from notifications stream");
    };

    webSocket.listen(function(event) {
        if (event.activity_type === "notification") {
            $("#notifications").addClass("new-notifications");
        } else if (event.activity_type === "message") {
            if (currentUser == event.receiver) {
                $("#unread-count").show();
            }
        }
    });
});
