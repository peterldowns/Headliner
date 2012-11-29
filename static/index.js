var CURRENT_REQ;
var closeInit = function(){
	$("#close").click(function(){
    if (CURRENT_REQ) {
      console.log('aborted!');
      CURRENT_REQ.abort();
    }
		$("#text").hide().html("");
		$("#pageTitle").text("Headliner - The Daily News");
		$("#content").fadeIn("fast");
	});
}
$(document).ready(function(){
	var close = '<div id="close">(close)</a>';
	$("#content").show(); // show the articles
	$("#text").hide(); // don't show any one article in particular
	$(".article").each(function(index, obj){
		var timestamp = $(obj).attr('ts');
		var realdate = new Date();
		realdate.setTime(timestamp);
		var datestr = realdate.toLocaleString();
		var datediv = $(obj).find('.pub_date');
		datediv.html(datestr);

		$(obj).children(".clickable").click(function(e){
			$("#content").fadeOut("fast");
			$("#pageTitle").html(close);
			closeInit();
			$("#text").html("<center><h1>Loading <img style='display:inline;' src='/static/ajax-loader.gif'/><h1></center>").show();
			var url = $(this).attr('url');
			CURRENT_REQ = $.ajax({
				url: '/viewtext?url='+url,
				cache: true,
				success: function(response){
					var data = $.parseJSON(response);
					var title = '<a href="'+data.url+'">'+data.title+'</a>';
					$("#pageTitle").html(close);
					$("#pageTitle").append(title);
					$("#text").html(data.body).fadeIn("fast");
				},
				error: function(response){
					console.log("There was an error with the request");
					console.log("Response:");
					console.log(response);
					$("#pageTitle").html("<h3>There was an error with the request");
					$("#text").html('<center><a class="close" href="">Click here to return to the homepage</a>');
				},
				complete: closeInit,
			});
			return false;
		});
	});
});
