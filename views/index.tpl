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
</body>
</html>
