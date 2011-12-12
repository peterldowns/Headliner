$(document).ready(function(){
	$("#content").show(); // show the articles
	$("#text").hide(); // don't show any one article in particular
	$(".article").each(function(index, obj){
		$(obj).click(function(e){
			$("#content").fadeOut("fast");
			$("#text").html("<h1>Loading</h1><img src='/static/ajax-loader.gif'/>").show();
			var url = $(this).attr('url');
			$.ajax({
				url: '/viewtext?url='+url,
				cache: true,
				success: function(response){
					var data = $.parseJSON(response);
					var close = '<a class="close" href="">(close)</a>';
					var title = '<a href="'+data.url+'">'+data.title+'</a>';
					$("#pageTitle").html(title);
					$("#pageTitle").append(close);
					$("#text").html(close+data.body+close).fadeIn("fast");
				},
				error: function(response){
					console.log("There was an error with the request");
					console.log("Response:");
					console.log(response);
					$("#pageTitle").html("<h3>There was an error with the request");
					$("#text").html('<center><a class="close" href="">Click here to return to the homepage</a>');
				},
				complete: function(){
					$(".close").each(function(index, obj){
						$(obj).click(function(){
							$("#text").hide().html("");
							$("#pageTitle").html("<h1>Headliner - The Daily News</h1>");
							$("#content").fadeIn("fast");
						});
					});
				},
			});
			return false;
		});
	});
});
