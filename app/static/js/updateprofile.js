$(document).ready(function(){
  var takenPhoneNumbers = {{takenPhoneNumbers|safe}};
  $("#updateProfileForm").submit(function(e){
    var phoneNumber = $("#phoneNumber").val();
    var i;
    for (i=0;i<takenPhoneNumbers.length;i++){
      if (phoneNumber===takenPhoneNumbers[i]){
        e.preventDefault();
        alert("Phone number already taken!");
      }
    }
    if (!$.isNumeric(phoneNumber)){
      e.preventDefault(e);
      alert("Phone no. must only contain numbers!");
    }
    else if (phoneNumber.length!==11){
      e.preventDefault()
      alert("Phone number must be 11 digit long!")
    }
  })
});