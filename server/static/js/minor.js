function createLineItem(data){
	var div = document.createElement("div");
		div.className = "event " + data.direction;
	var aBtn = document.createElement("a");
		aBtn.className = "event";
		aBtn.href = "#";
		aBtn.id = data['id'];
		aBtn.style.backgroundPosition = "center";
		aBtn.style.backgroundSize = "30px";
		var thisTime = data["time"].split(",");
		var date = new Date(Date.UTC(thisTime[0],thisTime[1]-1,thisTime[2],thisTime[3],thisTime[4],thisTime[5]));
		aBtn.title = date.toLocaleString();
		$(aBtn).css("background-image", "url(" + data.iconUrl + ")");
		$(aBtn).bind("click",slideItem);
	var spanLine = document.createElement("span");
		spanLine.className = "vLine";
		
	var aContent = document.createElement("a");
		aContent.className = "content " + data.direction + " " + data.layout;
		aContent.target = "_blank";
		aContent.href = data.targetUrl;
	if(data.layout != "onlytext"){
		var spanimage = document.createElement("span");
			spanimage.className = "image";
			spanimage.style.backgroundImage = "url(" + data.imageUrl + ")";
		aContent.appendChild(spanimage);
	}
	if(data.layout != "onlyimage"){
		var spantitle = document.createElement("span");
			spantitle.className = "title";
		
		var formatText = data.text;
		/*
		if(formatText.length >= 32){
			formatText = formatText.slice(0,30);
			formatText += "...";
		}
		*/
		
		if(typeof spantitle.innerText != "undefined"){
			spantitle.innerText = formatText;
		}else if(typeof spantitle.textContent != "undefined"){
			spantitle.textContent = formatText;
		}
		aContent.appendChild(spantitle);
	}
	var loveBtn = document.createElement("a");
		loveBtn.id = data['id'];
		loveBtn.className = "loveBtn";
		$(loveBtn).bind("click", function(evt){
			$.get("/"+username+"/activity?articleid="+this.id+"&"+"status=star");
			var $thisDiv = $("#"+this.id);
			var bg_url = $thisDiv.css('background-image');
			bg_url = /^url\((['"]?)(.*)\1\)$/.exec(bg_url);
			icon = /images\/([a-z]+_icon)_([a-z]+)\.png/.exec(bg_url[2]);
			if (icon) {
				$thisDiv.css("background-image", "url(/static/images/" + icon[1] + "_light.png)");
			}
			return false;			
		});
		aContent.appendChild(loveBtn);
	
	div.appendChild(aBtn);
	div.appendChild(spanLine);
	div.appendChild(aContent);	
	
	return div;
}

function beginSlide(thisDiv) {
	var regUp	= /^up\s|\sup\s|\sup$/;
	var regDown = /^down\s|\sdown\s|\sdown$/;
	var $thisDiv = $(thisDiv);
	
	var direction = "";
	if(regUp.test($thisDiv.attr("class"))){
		direction = "up";
	}else if(regDown.test($thisDiv.attr("class"))){
		direction = "down";
	}
	
	$thisDiv.animate({height:"250px"},500);
	$thisDiv.children("span.vLine").animate({height:"225px"},500);
	setTimeout(function(){
		$thisDiv.children("a.content").fadeIn(1200);
	},500);
	
	if(direction == "down"){
		$thisDiv.children("a.event, a.content").css("top","auto");
		$thisDiv.children("span.vLine").css("top","10px");
	}
	
	$thisDiv.addClass("slided");
}

function slideItem(evt){
	var regUp	= /^up\s|\sup\s|\sup$/;
	var regDown = /^down\s|\sdown\s|\sdown$/;
	
	var $thisDiv = $(evt.target).parent();
	
	var bg_url = $(evt.target).css('background-image');
	bg_url = /^url\((['"]?)(.*)\1\)$/.exec(bg_url);
	icon = /images\/([a-z]+_icon)\.png/.exec(bg_url[2]);
	if (icon) {
		$(evt.target).css("background-image", "url(/static/images/" + icon[1] + "_grey.png)");
	}
	
	$.get("/"+username+"/activity?articleid="+this.id+"&"+"status=read")
	$.getJSON("/" + username + "/" + this.id + "/recommend", function(article) {
		//document.getElementById("recommend").innerHTML="";
		//if (!article){return;}
		$("#recommend_a span:eq(0)").css("background-image","url(" + article["imageUrl"] + ")");
		$("#recommend_a span:eq(1)").text(article["text"]);
		$("#recommend_a").attr("href", article['targetUrl']);
		
		
	}).error(function() {
		
	});
	
	var direction = "";
	if(regUp.test($thisDiv.attr("class"))){
		direction = "up";
	}else if(regDown.test($thisDiv.attr("class"))){
		direction = "down";
	}
	
	if($thisDiv.hasClass("slided")){
		
		$thisDiv.children("a.content").fadeOut(1200);
		setTimeout(function(){
			$thisDiv.animate({height:"32px"},500);
			$thisDiv.children("span.vLine").animate({height:"8px"},500);
			setTimeout(function(){
				if(direction == "down"){
					$thisDiv.children("span.vLine").css("top","4px");
				}
			},500);
		},1200);
		
		$thisDiv.removeClass("slided");
		
	}else{
		/*目标元素滚动至时间轴中央*/
		var xScroll = $(evt.target).offset().left + $("#timeline").scrollLeft() - Math.floor($(window).width()/2);
		$("#timeline").animate({scrollLeft:xScroll},700);

		$thisDiv.animate({height:"250px"},500);
		$thisDiv.children("span.vLine").animate({height:"225px"},500);
		setTimeout(function(){
			$thisDiv.children("a.content").fadeIn(1200);
		},500);
		
		if(direction == "down"){
			$thisDiv.children("a.event, a.content").css("top","auto");
			$thisDiv.children("span.vLine").css("top","10px");
		}
		
		$thisDiv.addClass("slided");
		
		var eleArr = [$thisDiv.prev().prev().prev().prev(),$thisDiv.prev().prev(),$thisDiv.next().next(),
				$thisDiv.next().next().next().next()];
		for(var i=0; i<4; i++){
			var $tar = eleArr[i];
			if($tar.hasClass("slided") && $tar.hasClass(direction)){
				$tar.children("a.event").trigger("click");
			}
		}
	}
}

function dragX(evt){
	var target = $("#timeline");
	var origin = evt.pageX;
	var initPo = target.scrollLeft();
	
	var overOrigin = 0;
	var overOriginLeft  = 0;
	var overOriginRigth = 0;
	var overSymbol = true;
	
	$("#timeline").addClass("draging");
	
	$(document).unbind();
	$(document).bind("mousemove",function(evt){
		positionOffset = origin - evt.pageX;
		target.scrollLeft( initPo + positionOffset );
		
		/*模拟拖拉回弹抗拒力*/
		/*斜率渐增单调递增函数，k为可调节斜率*/
		var x = overOrigin - evt.pageX;
		var k = 500;
		if( (initPo + positionOffset)<=0 ){
			if(overSymbol){
				overOrigin = evt.pageX;
				overSymbol = false;
			}
			var y = (k*(-x))/(k+(-x));
			target.css("left",y);
		}else if( (initPo + positionOffset) >= (document.getElementById("timeline").scrollWidth - target.width()) ){
			if(overSymbol){
				overOrigin = evt.pageX;
				overSymbol = false;
			}
			var y = (k*(x))/(k+(x));
			target.css("left",-(y));
		}
	});
	
	$(document).bind("mouseup",function(evt){
		$("#timeline").removeClass("draging");
		$("#timeline").animate({left:"0px"},300);
		$(document).unbind();
	});
	
}













/*
var sampleData = {
	"layout":"leftright",
	"direction":"up",
	"time":"2012,1,18,17,51,46",
	"text":"这张卡片的说明文字",
	"imageUrl":"这张卡片的图片url",
	"targetUrl": "这张卡片的链接",
	"iconUrl":"图标的链接",
	"headline":"这张卡片的标题"
}
*/








