$(document ).ready(function()
	{
		$('#adminlogin').click(function(){
		
			$.ajax({
				url: '/adminlogin',
    	        data: $('form').serialize(),
    	        type: 'POST',
    	        success: function(response){
    	            window.location = "../showAdminhome";
    	        },
    	        error: function(error){
    	            console.log(error);
				}
			});
		return false;
		});
	});