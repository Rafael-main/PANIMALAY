$(document).ready(function(){
  var accData = {{accDataJSON|safe}};
  $("#ChangeEmail").submit(function(e){
     var newEmail = $("#newEmail").val();
     var password = $("#password").val();
    if ((/[ `!#$%^&*()_+\-=\[\]{};':"\\|,<>\/?~]/).test(newEmail)){
      e.preventDefault();
      alert("Email must not contain special characters");
    }
    else if(accData[1]===newEmail){
      e.preventDefault();
      alert("Old and New email are the same!");
    }
    else if(accData[2]!==password){
      e.preventDefault();
      alert("Wrong Password");
    }
  })
  
});