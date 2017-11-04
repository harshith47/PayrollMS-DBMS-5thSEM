$(document ).ready(function()
	{
		$('#btnaddemployee').click(function(){
		
			$.ajax({
				url: '/adminlogin',
    	        data: $('form').serialize(),
    	        type: 'POST',
    	        success: function(response){
    	            window.location = "../showSignUp";
    	        },
    	        error: function(error){
    	            console.log(error);
				}
			});
		return false;
		});
	});