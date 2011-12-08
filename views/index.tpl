<!doctype html>
<html>
<head>
	<title>Headliner</title>
	<link rel="stylesheet" type="text/css" href="/static/index.css" />
	<script type="text/javascript" src="static/jquery.js"></script>
	<script type="text/javascript" src="static/index.js"></script>
	<!-- start Mixpanel --><script type="text/javascript">var mpq=[];mpq.push(["init","ca3cd0bc73f9f1769760e83bc934727e"]);(function(){var b,a,e,d,c;b=document.createElement("script");b.type="text/javascript";b.async=true;b.src=(document.location.protocol==="https:"?"https:":"http:")+"//api.mixpanel.com/site_media/js/api/mixpanel.js";a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(b,a);e=function(f){return function(){mpq.push([f].concat(Array.prototype.slice.call(arguments,0)))}};d=["init","track","track_links","track_forms","register","register_once","identify","name_tag","set_config"];for(c=0;c<d.length;c++){mpq[d[c]]=e(d[c])}})();</script><!-- end Mixpanel -->
</head>

<body>
	<div id="divider"></div>
<div id="wrapper">
	<div id="content" class="columns">
	%for article in articles:
		<div class="article" url="{{article['url']}}" ts="{{article['timestamp']}}" tags="{{", ".join(article['tags'])}}">
			<div class="source">
				{{article['source']}}, {{article['pub_date']}}
			</div>
			{{article['title']}}
			<div class="tags">
				{{", ".join(article['tags'])}}
			</div>
		</div>
	%end
	</div>

<div id="text" class="columns"></div>
	<!-- start Clicky--> <script type="text/javascript"> var clicky_site_ids = clicky_site_ids || []; clicky_site_ids.push(66505054); (function() { var s = document.createElement('script'); s.type = 'text/javascript'; s.async = true; s.src = '//static.getclicky.com/js'; ( document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0] ).appendChild( s ); })(); </script><!-- end Click -->
</div>
<div id="pageTitle">Headliner - The Daily News</div>
</body>

</html>
