$(document).ready(function(){
	$("form").submit(function(e){
		var username = $("#username").val();
		var phoneNumber = $("#phoneNumber").val();
		var password = $("#password").val(); 
		var email  = $("#email").val();
		var firstName = $("#firstName").val(); 
		var lastName = $("#lastName").val();

		if ((/[ `!@#$%^&*()_+\-=\[\]{};':"\\|,<>\/?~]/).test(username)){
			e.preventDefault(e);
			alert("Username must not contain special characters");
		}

		else if  ((/[ `!@#$%^&*()_+\-=\[\]{};':"\\|,<>\/?~]/).test(firstName)){
			e.preventDefault(e);
			alert("First Name must not contain special characters");
		}

		else if  ((/[`!@#$%^&*()_+\-=\[\]{};':"\\|,<>\/?~]/).test(lastName)){
			e.preventDefault(e);
			alert("Last Name must not contain special characters");
		}
		else if  ((/[ `!#$%^&*()_+\-=\[\]{};':"\\|,<>\/?~]/).test(email)){
			e.preventDefault(e);
			alert("Email must not contain special characters");
		}
		else if  (firstName.length<1){
			e.preventDefault(e);
			alert("First Name must contains 2 or more characters ");
		}
		else if (lastName.length<1){
			e.preventDefault(e);
			alert("Last Name must contains 2 or more characters ");
		}
		else if (username.length<8){
			e.preventDefault(e);
			alert("Username must atleast contain 8 characters");
		}
		else if (/\d/.test(firstName)){
			e.preventDefault(e);
			alert("First Name must not contain number");
		}
		else if (/\d/.test(LastName)){
			e.preventDefault(e);
			alert("First Name must not contain number");

		}
		else if (phoneNumber.length!==11){
			e.preventDefault(e);
			alert("Phone no. must contain 11 digits");
		}
		else if (password.length<8){
			e.preventDefault(e);
			alert("Password must atleast contain 8 characters");
		}
		else if (!$.isNumeric(phoneNumber)){
			e.preventDefault(e);
			alert("Phone no. must only contain numbers");
		}
		else if (username.includes(" ")){
			e.preventDefault(e);
			alert("Using space in username input is not allowed");
		}
		else if (phoneNumber.includes(" ")) {
			e.preventDefault(e);
			alert("Using space in phone no. input is not allowed");
		}
		else if (email.includes(" ")){
			e.preventDefault(e);
			alert("Using space in email input is not allowed");
		}
		else if (password.includes(" ")){
			e.preventDefault(e);
			alert("Using space in password input is not allowed");
		}
	})
});
