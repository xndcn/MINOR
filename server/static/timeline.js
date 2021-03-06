maketimeline = function(sampleData) {	
	var timeLine = document.getElementById("timeline");
	timeline.innerHTML = "<div id='line' class='line'></div>";
	var timeStampArr = [];
	var eventItems = [];
	for(var i=0,len=sampleData.length; i<len; i++){
		var eventItem = createLineItem(sampleData[i]);
		timeLine.appendChild(eventItem);
		eventItems.push(eventItem);
		
		if(i==0){
			$(eventItem).css("left","200px");
			timeLine.appendChild(eventItem);
			continue;			
		}
		
		var thisTime = sampleData[i]["time"].split(",");
		var thisDate = new Date(Date.UTC(thisTime[0],thisTime[1]-1,thisTime[2],thisTime[3],thisTime[4],thisTime[5]));
		
		var thatTime = sampleData[i-1]["time"].split(",");
		var thatDate = new Date(Date.UTC(thatTime[0],thatTime[1]-1,thatTime[2],thatTime[3],thatTime[4],thatTime[5]));
		
		var diffTime  = thatDate - thisDate;
		var timeStamp = false;
		
		var diffMinite = diffTime/(1000*60);
		if(diffMinite > 180){
			diffMinite = 180;
			timeStamp  = true;
		}else if(diffMinite <5){
			diffMinite = 5;
		}
		
		var preNode = $(eventItem).prev(".event");
				
		var leftNum = (Number(preNode.css("left").slice(0,-2)) + diffMinite + 32) + "px";
		//var leftNum = (Number($(eventItem).prev(".event").css("left").slice(0,-2)) + diffMinite + 32) + "px";
		$(eventItem).css("left",leftNum);
		var temp = $("#line").width() + diffMinite;
		document.getElementById("line").style.width = temp + "px";
		
		if(i==len-1){
			document.getElementById("line").style.width = (Number(document.getElementById("line").style.width.slice(0,-2))+150+32*len + 50) + "px";
		}
		
		if(timeStamp){
			var div = document.createElement("div");
				$(div).addClass("month");
				$(div).html(thisTime[2] + "日" + "</br><span>" + thisTime[3] + ":" + thisTime[4] + "</span>");
			//$("#timeline").append(div);
			
			var posi = Number(leftNum.slice(0,-2)) - 90 - 32;
			div.style.left = posi + "px";
			timeStampArr.push(div);
			
			timeStamp = false;
		}
	}
	for(var i=0,len=timeStampArr.length; i<len; i++){
		$("#timeline").append(timeStampArr[i]);
	}
	
	for (var i = 0; i < sampleData.length; i+=2) {
		if (Math.random() > 0.5) {
			beginSlide(eventItems[i]);
			i+=4;
		}
	}
	for (var i = 1; i < sampleData.length; i+=2) {
		if (Math.random() > 0.5) {
			beginSlide(eventItems[i]);
			i+=4;
		}
	}
}

makeWholeTimeline = function() {
	$.getJSON("/"+username+"/articles.json", function(articles) {
		maketimeline(articles);
	})
	$("#timeline").unbind();
	$("#timeline").bind("mousedown", dragX);
}

makeTimeline = function(feedid) {
	$.getJSON("/"+username+"/"+feedid+"/articles.json", function(articles) {
		maketimeline(articles);
	})
	$("#timeline").unbind();
	$("#timeline").bind("mousedown", dragX);
}

$("#recommend_a").css("width",$("#recommend").width()-23);

//
//(function() {
//	$("#timeline").bind("mousedown", dragX);
//})();
