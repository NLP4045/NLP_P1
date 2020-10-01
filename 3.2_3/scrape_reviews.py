from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
import pandas as pd 

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions
from multiprocessing import Queue, Process


#options = ChromeOptions()



def get_reviews(url):
    print("Now getting: {}".format(url))
    #comments_parsed = []
    #res = requests.get(url)
    # Parse to html
    html_src = get_reviews_selenium(url)
    soup = BeautifulSoup(html_src, "html.parser")
    # Get all comments
    comments = soup.find_all('q')
    parsed_comments = []
    for comment in comments:
        # Convert br to \n
        b = str(comment).replace("<br/>", "\n")
        comment = BeautifulSoup(b, 'html.parser')
        parsed_comments.append(comment.find("span").text)
        
    print("Done with: {}".format(url))
    return parsed_comments

def get_reviews_selenium(url):
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get(url)
    readmores = driver.find_elements_by_class_name("_3maEfNCR")
    while True:
        try:
            readmores[0].click()
        except:
            return driver.page_source



# with ThreadPoolExecutor(max_workers=16) as executor:
#     reviews = executor.map(get_reviews, urls)
#     reviews = reduce(lambda x,y: x+y, reviews)
#     df = pd.DataFrame({'reviews': reviews})
#     df.to_csv("jewel_reviews.csv")


def mp_writer(queue, urls):

    already_sent_to_queue = []
    
    for url in urls:
        
        if url in already_sent_to_queue: # if already exported, ignore
            continue

        queue.put(url)
        already_sent_to_queue.append(url)
        print("[mp_master] Sent to queue - %s" % url)

    
def mp_worker(i, queue, result_queue):
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    
    while queue.qsize()>0:
        url = queue.get()
        print("[mp_worker #{}]: Processing: {}".format(i, url))
        driver.get(url)
        readmores = driver.find_elements_by_class_name("_3maEfNCR")
        driver.implicitly_wait(2)
        while True:
            try:
                readmores[0].click()
            except:
                break 
        src = driver.page_source
        soup = BeautifulSoup(src, "html.parser")
        # Get all comments
        for br in soup.find_all("br"):
            br.replace_with("\n")
        comments = soup.find_all('q')
        result_queue.put([comment.find("span").text for comment in comments])
        print("[mp_worker #{}]: Done with: {}".format(i, url))

    driver.quit()

if __name__ == '__main__':
    urls = ["https://www.tripadvisor.com.sg/Attraction_Review-g294265-d17237163-Reviews-Jewel_Changi_Airport-Singapore.html"]
    urls = urls + ["https://www.tripadvisor.com.sg/Attraction_Review-g294265-d17237163-Reviews-or{}-Jewel_Changi_Airport-Singapore.html".format(i) for i in range(5,890,5)]

    queue = Queue()
    result_queue = Queue()
    pool_size = 15

    master = Process(target=mp_writer, args=(queue,urls))
    #if production:
    #    writer = Process(target=result_writer)

    processes = [Process(target=mp_worker, args=(i+1, queue,result_queue)) for i in range(pool_size)]

    master.start()
    # if production:
    #     writer.start()
    for process in processes:
        process.start()

    results = []
    while len(results) < len(urls):
        while (result_queue.qsize() >0):
            results.append(result_queue.get())

    for process in processes:
        process.join()
    
    master.join()


    reviews = reduce(lambda x,y: x+y, results)
    df = pd.DataFrame({'reviews': reviews})
    df.to_csv("jewel_reviews.csv")


    
    

