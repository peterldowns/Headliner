function bg_on(){	
	$("html").addClass("bg_image");
}
function bg_off(){
	$("html").removeClass("bg_image");
}
function viewtext(url){
	var a = "http://viewtext.org/api/text?url="+url+"&format=html";
	$.get(a, function(data){
		$("content").hide();
		bg_off();
		$("#text").html(data);
		$("#text").fadeIn("slow");
	});
}
$(document).ready(function(){
	$("#content").show(); // show the articles
	$("#text").hide(); // don't show any one article in particular
	bg_on(); // turn on the background image
	$(".article").each(function(index, obj){
		$(obj).click(function(e){
			$("#content").fadeOut("fast");
			$("#text").html("<center><h1>Loading</h1></center>");
			$("#content").fadeOut("fast");
			bg_off();
			$("#text").fadeIn("slow");
			var url = $(this).attr('url');
			var a = "/viewtext/"+url;
			console.log("request to "+a);
			$.get(a, function(data){
				$("#text").html(data);
				});
			return false;
		});
	});

	$("#text").dblclick(function(){
		$("#text").hide().html("");
		bg_on();
		$("#content").fadeIn("slow");
	});
});
