<!DOCTYPE html>
<head>
	<title>Headliner</title>
	<link rel="stylesheet" type="text/css" href="/static/index.css" />
	<script type="text/javascript" src="static/jquery.js"></script>
	<script type="text/javascript" src="static/index.js"></script>
	<meta name="viewport" content="width=device-width">
</head>

<body>
	<div id="pageTitle"><a href="/" style="color:#000; text-decoration: none;"> Headliner - The Daily News </a></div>
	
	<div id="content" class="columns">
	%for article in articles:
		<div class="article" url="{{article['url']}}" ts="{{article['timestamp']}}" tags="{{", ".join(article['tags'])}}">
      <div class="clickable">
        <div class="source">
          {{article['source']}}
        </div>
        <p>{{!article['title']}}</p>
        <div class="pub_date"></div>
      </div>
      <a class="link" href="{{article['url']}}">(link)</a>
		</div>
	%end
	</div>
	
	<div id="text" class="columns"></div>
</body>

</html>
