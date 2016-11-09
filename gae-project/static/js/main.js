var softwareRU = softwareRU || {};
softwareRU.enableButtons = function(){
	$("#notification_li").hover(function(){
		$("#notificationContainer").toggle();
		
	});
	
	$('.table > tbody > tr').hover(function() {
		$(this).css('cursor','pointer');
	});
	
	$('.table > tbody > tr').click(function() {
		var projectKeyString = $(this).children("td:nth-child(3)").text();
		window.location.replace("./project-detail?project_entity_key="+projectKeyString);
	});
	
	$('input[name=dob]').datepicker();
	
	$(".collaborator_input").keyup(function(){
		if($(this).parent().nextAll(".collaborator_div").length == 0){
			if($(this).next().length == 0){
				$(this).after("<button class=\"btn-danger remove_collaborator pull-right\"><span class=\"glyphicon glyphicon-remove\"></span></button>");
				$(".remove_collaborator").click(function(){
					if($(".collaborator-form-div").children(".collaborator_div").length > 1){
						$(this).parent().remove();
					}else{
						$(this).remove();
					}
				});
			}
			var nextElem = $(this).parent('div').clone(true);
			nextElem.children()[0].value = "";
			nextElem.appendTo('.collaborator-form-div');
		}
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

