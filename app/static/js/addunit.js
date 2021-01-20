$(document).ready(function(){
  $("#unitForm").submit(function(e){
    var lat = $("#latitude").val();
    var lng = $("#longitude").val();
    if (lat.length===0 && lng.length===0){
      e.preventDefault();
      alert("Please click locate first");
    }
  })
  $("#locate").click(function(){
    if (navigator.geolocation){
      navigator.geolocation.getCurrentPosition(function(position){
        $("#longitude").attr('value',position.coords.longitude);
        $("#latitude").attr('value',position.coords.latitude);
        console.log($("#latitude").val());
        console.log($("#longitude").val());
      })
    }
    else{
      console.log("geolocation is not supported in this browser");
    }
  })
  
  
  $("#bedCaption").hide();
  $("#comfortroomCaption").hide();
  $("#aircoolingsystemCaption").hide();
  $("#studyareaCaption").hide();
  $("#wifizoneCaption").hide();
  $("#showerCaption").hide();
  
  $('#bedCaptionHide').click(function(){
    $("#bedCaption").hide();
  })
  $('#comfortroomCaptionHide').click(function(){
    $("#comfortroomCaption").hide();
  })
  $('#aircoolingsystemCaptionHide').click(function(){
    $("#aircoolingsystemCaption").hide();
  })
  $('#studyareaCaptionHide').click(function(){
    $("#studyareaCaption").hide();
  })
  $('#wifizoneCaptionHide').click(function(){
    $("#wifizoneCaption").hide();
  })
  $('#showerCaptionHide').click(function(){
    $("#showerCaption").hide();
  })
  $('#bed').click(function(){
    $("#bedCaption").show();
  })
  $('#comfortroom').click(function(){
    $("#comfortroomCaption").show();
  })
  $('#aircoolingsystem').click(function(){
    $("#aircoolingsystemCaption").show();
  })
  $('#studyarea').click(function(){
    $("#studyareaCaption").show();
  })
  $('#wifizone').click(function(){
    $("#wifizoneCaption").show();
  })
  $('#shower').click(function(){
    $("#showerCaption").show();
  })
  

  var facilitiesValue = [];
  $("#unitForm").submit(function(e){

    
    if ($("#bedCaption").is(":visible")){
      facilitiesValue.push("bed");
    }
    if ($("#comfortroomCaption").is(":visible")){
      facilitiesValue.push("comfort room");
    }
    if ($("#aircoolingsystemCaption").is(":visible")){
      facilitiesValue.push("air cooling system");
    }
    if ($("#studyareaCaption").is(":visible")){
      facilitiesValue.push("study area");
    }
    if ($("#wifizoneCaption").is(":visible")){
      facilitiesValue.push("wifi zone");
    }
    if ($("#showerCaption").is(":visible")){
      facilitiesValue.push("shower");
    }
    $("#facilities").attr("value",facilitiesValue);
    var facilities = $("#facilities").val();

    if ((facilities.length)===0){
      e.preventDefault();
      alert("Please select some amenities first...");
    }

    })

  
});