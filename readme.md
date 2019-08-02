Link Shortner (Python 3.7)

Shortens the link provided.

To run, cd to project directory, then hit "docker-compose up" command, it will run the whole project exposed to localhost:5000

To shorten a link:
	1. Pass your link in the url followed by base url (localhost:5000/<your_url>)
	2. It returns two urls in json,
		a. The shortened link of your url
		b. A link to see the stats (no. of clicks) on your shortened link.
	Note: Shortened link dies within stipulated period of time (currently 60 seconds) if there are no clicks on the link.

Implementation of token assistance in link shortening is in following way:
	1. Post json with following format  
	{
		"url" : "the_url_to_be_shortened_with_all_token_holders_as_<%token%>"
	} 
	at http://localhost:5001/ endpoint.
	2. To retrieve the original link with all the tokens dynamically inserted into shortened link, append all the tokens in 	   following format: 
		https://shortened-link/token1/token2/token3...
	Entering inconsistent number of tokens would lead to wrong url generation
	
Technologies used:
	MongoDB
	Flask
