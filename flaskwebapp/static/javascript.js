$(document).ready(function() {
    //UPDATE LIKES ON BUTTON CLICK
    $(".btn-like").on("click", function() {
        var $this = $(this)
        var endpoint = $this.attr("onclick");
        var post_id = $this.attr("post_id");

        req = $.ajax({
            url : endpoint,
            type : 'GET',
            data : {}
        });

        req.done(function(data) {
            $("#likesCount"+post_id).text(data.likes);
            $this.text(data.text);
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