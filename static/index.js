function bg_main_on(){	
	$("html").removeClass("bg_reader");
	$("html").addClass("bg_main");
}
function bg_main_off(){
	$("html").removeClass("bg_main");
	$("html").addClass("bg_reader");
}

$(document).ready(function(){
	$("#content").show(); // show the articles
	$("#text").hide(); // don't show any one article in particular
	bg_main_on(); // turn on the background image
	$(".article").each(function(index, obj){
		$(obj).click(function(e){
			$("#content").fadeOut("fast");
			var loadingstr = "<h1> Loading </h1><img src=\"/static/ajax-loader.gif\" />";
			$("#pageTitle").html(loadingstr);
			bg_main_off();
			var url = $(this).attr('url');
			$.get("/viewtext?url="+url, function(datastr){
				var data = $.parseJSON(datastr);
				var close = '<a class="close" href="">(close)</a>';
				var title = '<a href="'+data.url+'">'+data.title+'</a>';
				console.log(data);
				$("#pageTitle").html(title).append(close);
				$("#text").html(close+data.body+close).fadeIn("slow");
				$(".close").each(function(index, obj){
					$(obj).click(function(){
						$("#text").hide().html("");
						$("#pageTitle").html("<h1>Headliner - The Daily News</h1>");
						bg_main_on();
						$("#content").fadeIn("slow");
					});
				});
			});
			return false;
		});
	});
});
