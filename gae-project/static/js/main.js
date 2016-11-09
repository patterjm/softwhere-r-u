var softwareRU = softwareRU || {};
softwareRU.enableButtons = function() {
	$("#notification_li").hover(function() {
		$("#notificationContainer").toggle();

	});

	$('.table > tbody > tr').hover(function() {
		$(this).css('cursor', 'pointer');
	});

	$('.table > tbody > tr').click(function() {
		console.log(111);
	});

	$('input[name=dob]').datepicker();

	$('.addfriend').click(
			function() {
				if ($(this).text() === "Add Friend") {
					var receiver = $(this).next("input").val();
					var sender = $("#user_key").val();
					var message = "User" + $("#user_name").val()
							+ "wants to be your friend!";
					softwareRU.addfriend(receiver, sender, message, this);
				} else {
					var key = $(this).next("input").next("").val();
					softwareRU.cancelRequest(key,this);
				}
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

softwareRU.addfriend = function(receiver, sender, message, item) {
	var dataToSend = {
		"receiver" : receiver,
		"sender" : sender,
		"message" : message
	}
	$.post("/insert-notification", dataToSend).done(function(data) {
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
		console.log("canceled");

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
