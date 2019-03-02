$(document).ready(function() {

    function flash(data) {
        if ( $('.alert').length) {
            $('.alert').remove();
        }
        $('.main-content').prepend("<div class='alert alert-"+data.category+"'>"+data.message+"</div>");
    }

    //UPDATE LIKES ON BUTTON CLICK
    $(".btn-like").on("click", function() {
        var $this = $(this);
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

    //SEND EVENT REQUEST
    $(".btn-send-request").on("click", function() {
        var $this = $(this);
        var endpoint = $this.attr("onclick");
        var event_id = $this.attr("event_id");

        req = $.ajax({
            url : endpoint,
            type : 'POST',
            data : {}
        });

        req.done(function(data) {
            if (data.category == 'success') {
                $this.replaceWith('<small class="text-muted">Sent</small>');
            }
            flash(data)
        });
    });

    //ACCEPT EVENT REQUEST
    $(".btn-accept-request").on("click", function() {
        var $this = $(this);
        var endpoint = $this.attr("onclick");
        var event_id = $this.attr("event_id");

        req = $.ajax({
            url : endpoint,
            type : 'POST',
            data : {}
        });

        req.done(function(data) {
            $('#request'+event_id).remove()
            flash(data)
        });
    });

    //REFUSE EVENT REQUEST
    $(".btn-refuse-request").on("click", function() {
        var $this = $(this);
        var endpoint = $this.attr("onclick");
        var event_id = $this.attr("event_id");

        req = $.ajax({
            url : endpoint,
            type : 'POST',
            data : {}
        });

        req.done(function(data) {
            $('#request'+event_id).remove()
            flash(data)
        });
    });

    //REMOVE EVENT ATTENDANT
    $(".btn-remove-attendant").on("click", function() {
        var $this = $(this);
        var endpoint = $this.attr("onclick");
        var attendant_id = $this.attr("attendant_id");

        req = $.ajax({
            url : endpoint,
            type : 'POST',
            data : {},
            success: function(data) {
                if (data.category == 'success') {
                    $('.attendant'+attendant_id).remove();
                }
                flash(data);
            }
        });
    });

    //SEND INVITE
    $(".btn-send-invite").on("click", function() {
        var $this = $(this);
        var endpoint = $this.attr("onclick");
        var user_id = $this.attr("user_id");

        req = $.ajax({
            url : endpoint,
            type : 'POST',
            data : {}
        });

        req.done(function(data) {
            if (data.category == 'success') {
                $this.replaceWith('<small class="text-muted">Sent</small>')
            }
            flash(data)
        });
    });

    //ACCEPT INVITE
    $(".btn-accept-invite").on("click", function() {
        var $this = $(this);
        var endpoint = $this.attr("onclick");
        var event_id = $this.attr('event_id');

        req = $.ajax({
            url : endpoint,
            type : 'POST',
            data : {}
        });

        req.done(function(data) {
            if (data.category != 'danger') {
                $('#invite'+event_id).remove()
            }
            flash(data)
        });
    });

    //REFUSE INVITE
    $(".btn-refuse-invite").on("click", function() {
        var $this = $(this);
        var endpoint = $this.attr("onclick");
        var event_id = $this.attr('event_id');

        req = $.ajax({
            url : endpoint,
            type : 'POST',
            data : {}
        });

        req.done(function(data) {
            $('#invite'+event_id).remove()
            flash(data)
        });
    });
});