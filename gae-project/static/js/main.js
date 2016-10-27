var softwareRU = softwareRU || {};
softwareRU.enableButtons = function(){
	$("#notification_li").click(function(){
		$("#notificationContainer").toggle();
		
	});
	
	$('.table > tbody > tr').hover(function() {
		$(this).css('cursor','pointer');
	});
	
	$('.table > tbody > tr').click(function() {
		//direct to the project	
	});
};
$(document).ready(function(){
	softwareRU.enableButtons();
});

