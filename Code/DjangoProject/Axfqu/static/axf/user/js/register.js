$(function () {

    var $username = $("#username_input");
    var $email = $('#email_input')
    var $password_two = $("#password_confirm_input");

    $username.change(function () {
        var username = $username.val().trim();
        if (username.length) {
            $.getJSON('/one/checkuser/', {'username':username, }, function (data) {
                console.log(data);
                var $username_info = $('#username_info');
                $username_info.html(data["username_msg"]);

                if (data['username_status'] === 200){
                    $username_info.css("color",'green');
                    $('#username_div').removeClass('has-warning').addClass("has-success")
                }else if(data['username_status'] === 901){
                     $username_info.css("color",'red');
                    $('#username_div').removeClass('has-success').addClass("has-warning")
                }
            })
        }
    });

    $email.change(function () {
        var email = $email.val().trim();
        if (email.length){
            $.getJSON('/one/checkemail/', {'email': email}, function (data) {
                console.log(data);
                var $email_info = $("#email_info");
                $email_info.html(data['email_msg']);
                  if (data['email_status'] === 200){
                    $email_info.css("color",'green');
                    $('#email_div').removeClass('has-warning').addClass("has-success")
                }else if(data['email_status'] === 901){
                     $email_info.css("color",'red');
                    $('#email_div').removeClass('has-success').addClass("has-warning")
                }
            })
        }
    });

    $password_two.change(function () {
        var $password_two = $("#password_confirm_input");
        var $password = $('#password_input')
        var password_two = $password_two.val().trim();
        var password = $password.val().trim();
        var $password_two_info = $("#password_two_info");
        if(password===password_two) {
            $password_two_info.html('ok');
            $password_two_info.css('color', 'green');
            $('#password_two_div').removeClass('has-warning').addClass("has-success")
        }else{
            $password_two_info.html('wrong!');
            $password_two_info.css("color",'red');
            $('#password_two_div').removeClass('has-success').addClass("has-warning")
            }
    })

});

function check() {

    var $username = $("#username_input");
    var username = $username.val().trim();
    if(!username){
        return false
    }

    var $email = $("#email_input");
    var email = $email.val().trim();
    if(!email){
        return false
    }

    var passwd = $("#password_input").val();
    var passwd_two = $("#password_confirm_input").val()
    console.log(passwd)
    console.log(passwd_two)
    if (passwd_two !== passwd){
        return false
    }

    var name_info_color = $('#username_info').css('color');
    var email_info_color = $("#email_info").css('color');
    var password_two_info_color = $("#password_two_info").css('color')

    if(name_info_color == 'rgb(255, 0, 0)' || email_info_color == 'rgb(255, 0, 0)' || password_two_info_color == 'rgb(255, 0, 0)' ){
        return false
    }
    var $password_input = $("#password_input");
    var password = $password_input.val().trim();

    $password_input.val(md5(password));

    return true
}
