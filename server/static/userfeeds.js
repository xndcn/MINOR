$(document).ready(function() {
	$("#addfeed").click(function() {
		url = $("#feedurl")[0].value;
		addUserFeed(url);
		$("#feedurl")[0].value = "";
	});
	$('#mygroup').click(function() {
		makeWholeTimeline();
	})
})

var addUserFeed = function(url) {
	$.get("/"+username+"/append?url="+url, function() {		
		getUserFeeds();
	});
}

var getUserFeeds = function() {
	$("#feed-list").empty();
	$.getJSON("/"+username+"/feeds.json", function(feeds) {
		for(var i in feeds) {
			li = $('<li/>');
			icon = $('<img/>', {
				src: feeds[i]['icon'],
				height: '16px',
				width: '16px'
			});
			feedlink = $('<a/>', {
				id: feeds[i]['id'],
				text: feeds[i]['title'],
				href: '#',
				click: function(event) {
					makeTimeline(this.id);
				}
			});
			li.append(icon);
			li.append(feedlink);
			$("#feed-list").append(li);
		}
	});
}
