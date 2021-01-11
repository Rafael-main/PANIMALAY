$(document).ready(function(){
    $('#username').on("keyup",function(){
      $('#username').attr("class","form-control");
      $("#error2").hide();

    })
    $('#password').on("keyup",function(){
      $('#password').attr("class","form-control");
       $("#error1").hide();
    })

  });