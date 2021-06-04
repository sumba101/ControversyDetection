import asyncio
# threading imports
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor

# data processing/file handling imports
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm


global DIR

DIR = './temp_website_links'

def scrape_links(link):
    link = link.input
    num = link.split('/')[-1]
    num=num.split('.')[0]
    if num in list(os.listdir(DIR)):
        pbar.update(1)
        return 'DoneBefore'
    # scraping
    chromeOptions = Options()
    chromeOptions.add_argument('--headless')
    driver = webdriver.Chrome(options=chromeOptions)

    driver.get(link)


    data = dict()
    #  First expand the list to expost all the links
    button = driver.find_element_by_class_name( 'readmore-button-box' )  # .find_element_by_tag_name("a")
    button.click()

    # print( "collection" )
    ## collect it all
    first = driver.find_element_by_class_name( 'ranking' )
    second = driver.find_element_by_class_name( 'readmore-area' )
    for f in first.find_elements_by_tag_name( "li" ):
        if f.text:
            data[f.text] = f.find_element_by_tag_name( "a" ).get_attribute( "href" )
    for s in second.find_elements_by_tag_name( "li" ):
        if s.text:
            data[s.text] = s.find_element_by_tag_name( "a" ).get_attribute( "href" )

    temp = {
        'topics': [d for d in data.keys()],
        'links': [v for v in data.values()]
    }
    df = pd.DataFrame( temp, columns=['topics', 'links'] )

    df.to_csv(DIR+'/'+num+".csv", index=False)
    pbar.update(1)
    driver.quit()

    return 'Success'


async def get_restaurant_links(executor, search_links_df):
    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr,
    )

    logging.info('creating executor tasks')
    loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(
            executor, scrape_links, link
        ) for _, link in search_links_df.iterrows()
    ]
    logging.info('waiting for executor tasks')
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    logging.info('results: {!r}'.format(results))
    logging.info('exiting')


if __name__ == '__main__':
    # number of threads
    executor = ThreadPoolExecutor(
        max_workers=10,
    )

    search_links_df = pd.read_csv('./input_links.csv') # CSV containing all the website links by dates

    if len(sys.argv)>1:
        start = int(sys.argv[1])
        search_links_df = search_links_df.loc[start:start+49]
    global pbar
    pbar = tqdm(total=len(search_links_df))
    asyncio.get_event_loop().run_until_complete(
        get_restaurant_links(executor, search_links_df)
    )
