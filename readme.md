Implementation of token assistance in link shortening is in following way:
	1. Give the url in json format {"url":"the_url_to_be_shortened_with_all_token_holders_as_<%token%>"} at http://localhost:5001/tiny endpoint.
	2. Along with the generated short url append all the tokens in following format, https://shortened-link/token1/token2/token3...
		Entering inconsistent number of tokens would lead to wrong url generation