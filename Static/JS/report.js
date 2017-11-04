$(document ).ready(function()
	{
		$('#btnreport').click(function(){
		
			$.ajax({
				url: '/adminlogin',
    	        data: $('form').serialize(),
    	        type: 'POST',
    	        success: function(response){
    	            window.location = "../showReport";
    	        },
    	        error: function(error){
    	            console.log(error);
				}
			});
		return false;
		});
	});