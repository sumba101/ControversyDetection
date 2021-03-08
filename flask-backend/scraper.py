from selenium import webdriver

def helper(i,j):
    val= driver.find_elements_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[{}]/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[4]/div[{}]'.format(i,j))
    if len(val)==0:
        val= driver.find_elements_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[{}]/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[3]/div[{}]'.format(i,j))

    return val[0].text if len(val)!=0 else None

class Tweets:
    def __init__(self):
        self.text=''
        self.reply=''
        self.retweet=''
        self.like=''
    def setText(self,tweettext):

        self.text=tweettext

    def setRRL(self,reply,retweet,like):
        self.reply=reply
        self.retweet=retweet
        self.like=like

def scraper(url):
    link = 'https://twitter.com/'+url   
    driver = webdriver.Chrome()

    # link='https://twitter.com/BarackObama/status/1366878648544993281'

    driver.get(link)

    print(driver.title)

    # probably needs a sleep here to allow for chrome to open up fully

    allTweets=list()
    no_of_tweets = 15
    for i in range(1,no_of_tweets):
        component = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[{}]'.format(i))

        if component.text != '':
            tweet=Tweets()
            tweet.setText(component.text)
            reply= helper(i,1)
            retweet= helper(i,2)
            like= helper(i,3)
            tweet.setRRL(reply,retweet,like)
            allTweets.append(tweet)
