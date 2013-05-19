function createLineItem(data){
	var div = document.createElement("div");
		//div.className = "event " + data.direction;
		$(div).addClass("event");
		$(div).addClass(data.direction);
	var aBtn = document.createElement("a");
		aBtn.className = "event";
		aBtn.href = "#";
		aBtn.style.backgroundImage = "url(" + data.iconUrl + ")";
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
		loveBtn.id = "loveBtn";
		loveBtn.className = "loveBtn";
		$(loveBtn).bind("click",function(evt){
			
		});
		aContent.appendChild(loveBtn);
	
	div.appendChild(aBtn);
	div.appendChild(spanLine);
	div.appendChild(aContent);	
	
	return div;
}

function slideItem(evt){
	var regUp	= /^up\s|\sup\s|\sup$/;
	var regDown = /^down\s|\sdown\s|\sdown$/;
	
	var $thisDiv = $(evt.target).parent();
	
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














