def driverFunction(url):
# url : Url of the twitter page
	
	url= "https://twitter.com/" + url
	output = processTweet(url)
	output = dict(sorted(output.items(), key=lambda item: item[1]))
	return output

def processTweet(url):
	response = {"Every single American has a right to clean drinking water. It’s just plain wrong that in the United States of America today, millions of children still receive their water through lead service pipes. It’s long past time we fix that.":True}

	return response
