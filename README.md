# Headliner #
## A simple newsreader that looks nice ##

That's what Headliner is, but why? I like to read the news, but sometimes the news sites I read are blocked at school. Also, a lot of news sites are covered with advertisements and other content I'm not interested in. 

After putting up with this for a while, I decided to make myself a dashboard where I can see all of the latest news that might interest me. On top of that, it cleans up the news stories and makes them very readable (column layout, just like the print edition!).

It works pretty well, but some improvements need to be made.

##Todo:##

* Fetch sources at interval in the background using a worker program
	* store them in a shelf
* Add more sources (only NYT and AP right now)
* Make a better reading interface (double click to close stinks)
* Add user authentication (let people other than me use it?)
	* maybe not - check the developer license terms
* Better article parsing (don't just rely on viewtext and diffbot)
