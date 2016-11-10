var softwareRU = softwareRU || {};
softwareRU.enableButtons = function() {
	$("#notification_li").hover(function() {
		$("#notificationContainer").toggle();

	});

	$('.table > tbody > tr').click(function() {
		$(this).css('cursor', 'pointer');
	});

	$('.table > tbody > tr').click(function() {
		var projectKeyString = $(this).children("td:nth-child(3)").text();
		
		window.location.replace("./project-detail?project_entity_key="+projectKeyString);
	});
	
	$('.projectDetail').click(function() {
		var projectKeyString = $(this).next().next("input").val();
		window.location.replace("./project-detail?project_entity_key="+projectKeyString);
	});

	$('.requestJoin').click(function(){
		var projectKeyString = $(this).next("input").val();
		var receiver = $(this).next("input").val();
		var sender = $("#user_key").val();
		var reponame = $(this).next("input").next("").val();
		var message = "User " + $("#user_name").val()
				+ " wants to join your repo " + reponame;
		softwareRU.projectJoinRequest(receiver,sender,message);
	});
	
	$('input[name=dob]').datepicker();

	$('.addfriend').click(
			function() {
				if ($(this).text() === "Add Friend") {
					var receiver = $(this).next("input").val();
					var sender = $("#user_key").val();
					var message = "User " + $("#user_name").val()
							+ " wants to be your friend!";
					softwareRU.addfriend(receiver, sender, message, this);
				} else {
					var key = $(this).next("input").next("").val();
					softwareRU.cancelRequest(key,this);
				}
			});

	
	$(".collaborator_input").keyup(function(e){
		var code = (e.keyCode || e.which);
		if(code == 37 || code == 38 || code == 39 || code == 40 || code == 8 || code == 20 || code == 16){
			return;
		}else if(code == 13){
			if($(this).nextAll().length == 0){
				var newUserElem = $(this).clone(true);
				newUserElem.val("");
				$(this).after(newUserElem);
			}
			return;
		}
		if($(this).val()){
			var dataToSend = {"input_val":$(this).val()}
			$.get("/get-users", dataToSend).done(function(data) {
				console.log(data);
				$("#user_entities_data").empty();
				for(var i = 0; i < data.query_results.length; i++){
					$("#user_entities_data").append("<option value=\""+data.query_results[i].profile_name+"\" name=\"" + data.query_results[i].user_key+"\">")
				}
			}).fail(function(jqxhr, textStatus, error) {
				console.log("GET Request Failed: " + textStatus + ", " + error);
			});
		}
	});
	
	$(".delete_project_user").click(function(){
		var elemToDelete = $(this).parent();
		var dataToSend = {"user_key": $(this).next().val(),
							"project_key":$(this).prev().val()}
		$.post("/delete-project-user", dataToSend).done(function(data){
			elemToDelete.remove();
		}).fail(function(jqxhr, textStatus, error){
			console.log("POST Request Failed: " + textStatus + ", " + error);
		});
	});
};

softwareRU.enableSearch = function() {
	var $rows = $(".projectBox")
	var rowsTextArray = [];

	var i = 0;
	$.each($rows, function() {
		rowsTextArray[i] = $(this).children(":first").find('p').text().replace(
				/\s+/g, ' ').toLowerCase();
		i++;
	});

	$('#search').keyup(function() {
		var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
		$rows.show().filter(function(index) {
			return (rowsTextArray[index].indexOf(val) === -1);
		}).hide();
	});

};

softwareRU.projectJoinRequest = function(receiver, sender, message){
	var dataToSend = {
			"receiver" : receiver,
			"sender" : sender,
			"message" : message
		}
		$.post("/request-join", dataToSend).done(function(data) {
		}).fail(function(jqxhr, textStatus, error) {
			console.log("POST Request Failed: " + textStatus + ", " + error);
		});
}

softwareRU.addfriend = function(receiver, sender, message, item) {
	var dataToSend = {
		"receiver" : receiver,
		"sender" : sender,
		"message" : message
	}
	$.post("/insert-notification-ajax", dataToSend).done(function(data) {
		$(item).text("Cancel Request");
		$(item).removeClass("btn-primary");
		$(item).addClass("btn-secondary");
		$(item).next("input").next("").val(data);
	}).fail(function(jqxhr, textStatus, error) {
		console.log("POST Request Failed: " + textStatus + ", " + error);
	});
};

softwareRU.cancelRequest = function(key, item) {
	var dataToSend = {
		"key" : key
	}
	$.post("/cancel-friendrequest", dataToSend).done(function(data) {
		console.log("succeed");
		$(item).text("Add Friend");
		$(item).removeClass("btn-secondary");
		$(item).addClass("btn-primary");
		$(item).next("input").next("").val("");

	}).fail(function(jqxhr, textStatus, error) {
		console.log("POST Request Failed: " + textStatus + ", " + error);
	});
};

softwareRU.updateViews = function() {
	$(".addfriend").each(function(){
		var receiver = $(this).next("input").val();
		var sender = $("#user_key").val();
		softwareRU.checkNotification(receiver, sender, this)
	});
};

softwareRU.checkNotification = function(receiver, sender, item) {
	var dataToSend = {
		"receiver" : receiver,
		"sender" : sender,
	}
	$.get("/check-notification", dataToSend).done(function(data) {
		console.log($(item));
		if (!data["hasnoti"]) {
			$(item).text("Add Friend");
			$(item).removeClass("btn-secondary");
			$(item).addClass("btn-primary");
		} else {
			$(item).text("Cancel Request");
			$(item).removeClass("btn-primary");
			$(item).addClass("btn-secondary");
			$(item).next("input").next("").val(data["data"]);
		}

	}).fail(function(jqxhr, textStatus, error) {
		console.log("POST Request Failed: " + textStatus + ", " + error);
	});
};
$(document).ready(function() {
	softwareRU.updateViews();
	softwareRU.enableButtons();
	softwareRU.enableSearch();
});
