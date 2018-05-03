/**
 * Created by tonnie on 15/10/25.
 */
(function($, document){
    $.fn.login = function(options) {
        var selector = "#" + $(this).attr("id");

        $(document).on("click", selector, function(ev) {
               $('.ui.modal').modal('show');
		return false;
           }
       );

        $("#lg_form").on({
            submit: function(ev) {
                ev.preventDefault();
                $.ajax({
                    url: "/users/login",
                    type: "POST",
                    data: $(this).serialize(),
                    beforeSend: function(xhr) {
                        $('.message').hide();
                    },
                    success: function(resp) {
                        if(resp.status == true) {
                            $("#success").html("<p>"+resp.reason+"</p>").show();
                            $("#sign_in").addClass("loading");
                            setTimeout(function(){
                                window.location.href = resp.redirect_url;
                            }, 1000);
                        } else {
                            $("#error").html("<p>"+resp.reason+"</p>").show();
                        }
                    },
                    error: function(xhr, error, exp) {

                    }
                })
            }
        });
    }
}(jQuery, document));
