### Necessary packages
I honestly lost track, need selenium and webdrivemanager for starters so pip install those
rest install as and when you get errors

### How to use the code
#### First
Open `collectLinks.py` and change the value for number of days to whatever value you want
It defines the number of days that shall be scraped for creation of the dataset by creating a csv file called `input_links.csv` 

#### Second
Run `ScraperForTweetTopics.py`
On completion it will leave individual csv's in the temp_website_links folder

#### Third
By modifying `joinFiles.py` by necessary changes in the file names it references run the file
This joins all the csvs in temp_website_links to one PHAT csv