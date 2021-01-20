$(document).ready(function(){
  var accData = {{accDataJSON|safe}};
  $("#ChangePassword").submit(function(e){
     var oldPassword = $("#oldPassword").val();
     var newPassword = $("#newPassword").val();
     if (accData[2]!==oldPassword){
      e.preventDefault();
      alert("Incorrect Old Password!");
     }
     else if (accData[2]===oldPassword && newPassword.length<8){
      e.preventDefault();
      alert("New password must atleast contain 8 characters!")
     }
     else if (accData[2]===oldPassword && oldPassword===newPassword){
       e.preventDefault();
      alert("New password must be different from the old one!");
     }

  })
  
});
