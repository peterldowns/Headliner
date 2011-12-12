<!DOCTYPE html>
<head>
	<title>Headliner</title>
	<link rel="stylesheet" type="text/css" href="/static/index.css" />
	<script type="text/javascript" src="static/jquery.js"></script>
	<script type="text/javascript" src="static/index.js"></script>
</head>

<body>
	<div id="pageTitle">Headliner - The Daily News</div>
	
	<div id="content" class="columns">
	%for article in articles:
		<div class="article" url="{{article['url']}}" ts="{{article['timestamp']}}" tags="{{", ".join(article['tags'])}}">
			<div class="source">
				{{article['source']}}
			</div>
			{{article['title']}}
			<div class="tags">
				{{", ".join(article['tags'])}}
			</div>
		</div>
	%end
	</div>
	
	<div id="text" class="columns"></div>
</body>

</html>
