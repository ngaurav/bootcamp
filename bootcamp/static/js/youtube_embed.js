// Call this function at the end of the closing </body> tag.
function optimizeYouTubeEmbeds() {
    var frames = document.getElementsByTagName('iframe'); // Get all iframes

    // Loop through each iframe in the page.
    for (var i = 0; i < frames.length; i++) {
        // Find out youtube embed iframes.
        if (frames[i].src && frames[i].src.length > 0 && frames[i].src.match(/http(s)?:\/\/www\.youtube\.com/)) {
            // For Youtube iframe, extract src and id.
            var src = frames[i].src;
            var p = /^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/;
            var id = (src.match(p) ? RegExp.$1 : false);
            if (id == false) {
                continue
            }

            // Get width and height.
            var w = frames[i].offsetWidth;
            var h = w*0.5625;
            if (src == '' || w == '' || h == '') {
                continue;
            }

            // Thease are to position the play button centrally.
            var pw = Math.ceil(w / 2 - 38.5);
            var ph = Math.ceil(h / 2 - 38.5);

            // The image+button overlay code.
            var code = '<a href="#"  onclick="LoadYoutubeVidOnPreviewClick(\'' + id + '\',' + w + ',' + h + ');return false;" id="skipser-youtubevid-' + id + '"><div class="card-img-top" style="width:' + w + 'px; height:' + h + 'px; margin:0; background:url(http://i.ytimg.com/vi/' + id + '/hqdefault.jpg) center center; background-size:cover;">' +
            '<img src="/static/img/play.svg" style="height: 77px;width: 77px; position:relative; margin-left:' + pw + 'px; margin-top:' + ph + 'px;"></div></div></a>';

            // Replace the iframe with a the image+button code
            var div = document.createElement('div');
            div.innerHTML = code;
            div = div.firstChild;
            frames[i].parentNode.replaceChild(div, frames[i]);
            i--;
        }
    }
}
// Replace preview image of a video with it's iframe.
function LoadYoutubeVidOnPreviewClick(id, w, h) {
    var code = '<iframe src="https://www.youtube.com/embed/' + id + '/?autoplay=1&autohide=1&border=0&wmode=opaque&enablejsapi=1" width="' + w + '" height="' + h + '" frameborder=0 allowfullscreen style="border:1px solid #ccc;" ></iframe>';
    var iframe = document.createElement('div');
    iframe.innerHTML = code;
    iframe = iframe.firstChild;
    var div = document.getElementById("skipser-youtubevid-" + id);
    div.parentNode.replaceChild(iframe, div)
}

$(document).ready(function() {
    optimizeYouTubeEmbeds();
});