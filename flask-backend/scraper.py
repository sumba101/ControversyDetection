def driverFunction(url):
# url : Url of the twitter page
	
	url= "https://twitter.com/" + url
	output = processTweet(url)
	output = dict(sorted(x.items(), key=lambda item: item[1]))
	return output

def processTweet(url):
	return {"temp","temp"}
