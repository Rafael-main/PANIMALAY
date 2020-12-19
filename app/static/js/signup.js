$(document).ready(function(){
    $("#firstName").on('keyup',function(e){
      if (e.target.value.length<=1){
         $('#firstName').attr("class","form-control is-invalid");
      }
      else{
        $('#firstName').attr("class","form-control is-valid");
      }
    })
    $("#lastName").on('keyup',function(e){
      if (e.target.value.length<=1){
         $('#lastName').attr("class","form-control is-invalid");
      }
      else{
        $('#lastName').attr("class","form-control is-valid");
      }
    })
    $("#accountType").on('change',function(){
       $('#accountType').attr("class","form-control is-valid");
    })
    $("#birthDate").on('change',function(){
       $('#birthDate').attr("class","form-control is-valid");
    })
    $("#gender").on('change',function(){
       $('#gender').attr("class","form-control is-valid");
    })
    $("#username").on('keyup',function(e){
      if (e.target.value.length<8){
         $('#username').attr("class","form-control is-invalid");
      }
      else{
        $('#username').attr("class","form-control is-valid");
      }
    })
    $("#username").on('click',function(){
      $("#errorMsg").hide();
    })
    $("#email").on('keyup',function(){
       $('#email').attr("class","form-control is-valid");
    })
    $("#password").on('keyup',function(e){
      if (e.target.value.length<8){
         $('#password').attr("class","form-control is-invalid");
      }
      else{
        $('#password').attr("class","form-control is-valid");
      }
    })
   $("#phoneNumber").on('keyup',function(e){
      if (!$.isNumeric(e.target.value))
      {
         $('#phoneNumber').attr("class","form-control is-invalid");
      }
      else{
        $('#phoneNumber').attr("class","form-control is-valid");
      }
    })
});