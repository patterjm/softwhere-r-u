var softwareRU = softwareRU || {};
softwareRU.enableButtons = function(){
	$("#notification_li").hover(function(){
		$("#notificationContainer").toggle();
		
	});
	
	$('.table > tbody > tr').hover(function() {
		$(this).css('cursor','pointer');
	});
	
	$('.table > tbody > tr').click(function() {
		console.log(111);
	});
	
};

softwareRU.enableSearch = function(){
	var $rows = $(".projectBox")
	var rowsTextArray = [];

	var i = 0;
	$.each($rows, function() {
	  rowsTextArray[i] = $(this).children(":first").find('p').text().replace(/\s+/g, ' ').toLowerCase();
	  i++;
	});

	$('#search').keyup(function() {
	  var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
	  $rows.show().filter(function(index) {
	    return (rowsTextArray[index].indexOf(val) === -1);
	  }).hide();
	});
	
	
	
};

$(document).ready(function(){
	softwareRU.enableButtons();
	softwareRU.enableSearch();
});

