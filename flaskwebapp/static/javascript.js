$(document).ready(function() {
    //UPDATE LIKES ON BUTTON CLICK
    $(".btn-like").on("click", function() {
        var $this = $(this)
        var endpoint = $this.attr("onclick");
        var post_id = $this.attr("post_id");

        req = $.ajax({
            url : endpoint,
            type : 'POST',
            data : {}
        });

        req.done(function(data) {
            $("#likesCount"+post_id).text(data.likes);
            $this.text(data.text);
        });
    });

    //REFRESH EVENTS LIST
    $('.refresh-events').on('click', function() {
        req = $.ajax({
            url : '/events/get/',
            type : 'GET'
        });

        req.done(function(data) {
            $('.event-list').html(data.events);
        });
    });

    //LOAD COMMENTS SECTION ON BUTTON CLICK
    $(".btn-comment").on("click", function() {
        var $this = $(this);
        var post_id = $this.attr("post_id");
        var comments = document.querySelector('.comments-section'+post_id);

        if(comments.style.display == 'none'){
            comments.style.display = 'inline'
        }else{
             comments.style.display = 'none'
        };
    });
});