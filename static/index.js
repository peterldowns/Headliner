function bg_main_on(){	
	$("html").removeClass("bg_reader");
	$("html").addClass("bg_main");
}
function bg_main_off(){
	$("html").removeClass("bg_main");
	$("html").addClass("bg_reader");
}
function viewtext(url){
	var a = "http://viewtext.org/api/text?url="+url+"&format=html";
	$.get(a, function(data){
		$("content").hide();
		bg_main_off();
		$("#text").html(data);
		$("#text").fadeIn("slow");
	});
}
$(document).ready(function(){
	$("#content").show(); // show the articles
	$("#text").hide(); // don't show any one article in particular
	bg_main_on(); // turn on the background image
	$(".article").each(function(index, obj){
		$(obj).click(function(e){
			$("#content").fadeOut("fast");
			$("#text").html("<center><h1>Loading</h1></center>");
			$("#content").fadeOut("fast");
			bg_main_off();
			$("#text").fadeIn("slow");
			var url = $(this).attr('url');
			var a = "/viewtext?url="+url;
			console.log("request to "+a);
			$.get(a, function(data){
				var close = '<center><a class="close" href="#">(close)</a></center>';
				$("#text").html(data);
				$("#text").append(close);
				$("#text").prepend(close);
				$(".close").each(function(index, obj){
					$(obj).click(function(){
						$("#text").hide().html("");
						bg_main_on();
						$("#content").fadeIn("slow");
					});
				});
			});
			return false;
		});
	});
});
