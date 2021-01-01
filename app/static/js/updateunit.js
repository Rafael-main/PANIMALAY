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
});
