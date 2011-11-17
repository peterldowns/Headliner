<!doctype html>
<html class="bg_image">
<head>
	<title>Headliner</title>
	<link rel="stylesheet" type="text/css" href="/static/index.css" />
	<script type="text/javascript" src="static/jquery.js"></script>
	<script type="text/javascript" src="static/index.js"></script>
</head>
<body>
	<div id="content" class="columns">
	%for article in articles:
		<div class="article" url="{{article.url}}" tags="{{", ".join(article.tags)}}">
			<div class="source">
				{{article.source}}, {{article.pub_date}}
			</div>
			{{article.title}}
			<div class="tags">
				{{", ".join(article.tags)}}
			</div>
		</div>
	%end
	</div>
	<div id="text" class="columns"></div>
	<!-- Analytics -->
	<a title="Web Statistics" href="http://getclicky.com/66505054"><img alt="Web Statistics" src="//static.getclicky.com/media/links/badge.gif" border="0" /></a><script type="text/javascript"> var clicky_site_ids = clicky_site_ids || []; clicky_site_ids.push(66505054); (function() { var s = document.createElement('script'); s.type = 'text/javascript'; s.async = true; s.src = '//static.getclicky.com/js'; ( document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0] ).appendChild( s ); })(); </script> <noscript><p><img alt="Clicky" width="1" height="1" src="//in.getclicky.com/66505054ns.gif" /></p></noscript>

</body>
</html>
