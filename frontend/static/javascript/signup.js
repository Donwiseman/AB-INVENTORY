$(document).ready(function(){
    $("#signup").submit(function(event){
        var fname = $("#f-name").val()
        var lname = $("#l-name").val()
        var email = $("#e-mail").val()
        var rq = $("#r-q").val()
        var ra = $("#r-a").val()
        var pword = $("#p-word").val()
        var rpword = $("#r-pword").val()

        if (fname.length < 2 ) {
            $("#nameErr").text('Name should be atleast 2 characters')
            event.preventDefault()
        } else {
            $("#nameErr").text('')
        }

        if (lname.length < 2 ) {
            $("#lnameErr").text('Name should be atleast 2 characters')
            event.preventDefault()
        } else {
            $("#lnameErr").text('')
        }

        var emailRegex = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
        if (!email.match(emailRegex)) {
        $('#emailErr').text('Invalid email address');
        event.preventDefault();
        } else {
        $('#emailErr').text('');
        }

        if (rq.length < 11) {
            $('#quesErr').text('Question should be atleast 10 characters')
            event.preventDefault()
        } else {
            $('#quesErr').text('')
        }

        if (ra.length < 1) {
            $('#quasErr').text('Answer should be atleast a character')
            event.preventDefault()
        } else {
            $('#quasErr').text('')
        }

        if (pword.length < 8) {
            $('#pwErr').text("Password should be atleast 7 characters")
            event.preventDefault()
        } else {
            $('#pwErr').text('')
        }

        if (rpword !== pword) {
            $('rpwErr').text('Password does not match!')
            event.preventDefault()
        } else {
            $('rpwErr').text('')
        }
    })
})