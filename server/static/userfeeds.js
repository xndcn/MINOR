$(document).ready(function() {
	$("#addfeed").click(function() {
		url = $("#feedurl")[0].value;
		username = $("#username")[0].attributes['value'].value;
		addUserFeed(username, url);
		$("#username")[0].attributes['value'].value = "";
	});
})

var addUserFeed = function(username, url) {
	$.get("/"+username+"/append?url="+url, function() {
		getUserFeeds(username);
	});
}

var getUserFeeds = function(username) {
	$("#feed-list").empty();
	$.getJSON("/"+username+"/feeds.json", function(feeds) {
		for(var i in feeds) {
			li = $('<li/>');
			feedlink = $('<a/>', {
				id: feeds[i]['id'],
				text: feeds[i]['title'],
				href: '#',
				click: function(event) {
					
				}
			});
			li.append(feedlink);
			$("#feed-list").append(li);
		}
	});
}
