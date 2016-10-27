var softwareRU = softwareRU || {};
softwareRU.enableButtons = function(){
	$("#notification_li").click(function(){
		console.log(111);
		$("#notificationContainer").toggle();
		
	});
};
$(document).ready(function(){
	softwareRU.enableButtons();
});

