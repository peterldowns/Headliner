# Headliner #
### A simple newsreader that looks nice ###

That's what Headliner is, but why? I like to read the news, but sometimes the news
sites I read are blocked at school. Also, a lot of news sites are covered with
advertisements and other content I'm not interested in. 

After putting up with this for a while, I decided to make myself a dashboard where
I can see all of the latest news that might interest me. On top of that, it cleans
up the news stories and makes them very readable (column layout, just like the
print edition!).

It works pretty well, but some improvements need to be made.

### How does it work? ###

Every 30 seconds, a daemon fetches the latest news from a collection of sources. All
it fetches is some metadata, including the URL of the article. This metadata is stored
in a database (currently a python standard library 'shelf') for later access.

On page loads, the newest 50 'articles' (collections of metadata on news stories) are
pushed onto a page. When an article's headline is clicked, the page asks the server to
get the article text. If the text has been gotten before, the cached result is returned;
otherwise, viewtext.com's API is called instead.

##Todo:##


* Better typography
	* http://3.7designs.co/blog/2008/06/10-examples-of-beautiful-css-typography-and-how-they-did-it/ (s/:first)
	* http://www.informationarchitects.jp/en/100e2r/ (s/lineheight)
* Make /viewtext return JSON and dynamically set the page content
* Start actually creating timestamps on articles
* Add more sources
* Start filtering the news to show headlines that it thinks I would like
* Change fetcher cronjob to a worker process
	* right now, there are weird problems with the python env (?)
* Improve the reading interface
* Better article parsing (don't just rely on viewtext and diffbot)
	* maybe use a custom BeautifulSoup scraper (?)
* Add user authentication (let people other than me use it?)
	* maybe not - check the developer license terms
