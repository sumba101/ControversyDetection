def driverFunction(url):
# url : Url of the twitter page
	
	url= "https://twitter.com/" + url
	output = processTweet(url)
	output = dict(sorted(output.items(), key=lambda item: item[1]))
	return output

def processTweet(url):
	response = {"#WestBengalPolls | \"She [Mamata] alleges that polling agent was ousted from one booth. But said nothing when her people pelted stones on media and injured one. Her political ground is slipping away. What she did is illegal\": @SuvenduWB, BJP candidate from Nandigram (reports ANI)":" True"}

	return response
