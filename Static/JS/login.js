$(document ).ready(function()
	{
		$('#btnlogin').click(function(){
		
			$.ajax({
				url: '/login',
    	        data: $('form').serialize(),
    	        type: 'POST',
    	        success: function(response){
    	           window.location = "../showProfile";
    	            
    	        },
    	        error: function(error){
    	            console.log(error);
				}
			});
			
		return false;
		});
	});