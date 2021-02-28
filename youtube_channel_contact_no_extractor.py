import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import openpyxl
from datetime import datetime
import pandas as pd
import time
import re
import json

chrome_options=Options()
driver = webdriver.Chrome(options=chrome_options)#, executable_path ="C:\\Users\\shash\\Downloads\\chromedriver\\chromedriver.exe")
# wait = WebDriverWait(driver,6)
# print("Chrome opened successfully!!")

baseUrl = "https://youtube.com/"
keyword = input("catagory of search : ")
scroll_count = int(input("enter total no. of search : "))
# print("youtube opens!")


def getChannelUrl(): #get page url
    # driver.get(f"{baseUrl}/search?q={keyword}&sp=EgQIBBAB") #filter- within month
    driver.get(f"{baseUrl}/search?q={keyword}&sp=EgIIBQ%253D%253D") #filter-within year
    time.sleep(5)
    url_list = []
    url_link = set()
    for i in range(scroll_count): #loop to scroll page
        driver.execute_script('window.scrollTo(0,(window.pageYOffset+300))')
        time.sleep(5)
        url_list= driver.find_elements_by_css_selector("#text.style-scope.ytd-channel-name a.yt-simple-endpoint.style-scope.yt-formatted-string")
        # url_list = url_list.get_attribute("href")
        for links in url_list:
            if (links != '#'):
                url_link.add(links.get_attribute("href"))
    
    # allChannelList= driver.find_elements_by_css_selector("#text.style-scope.ytd-channel-name a.yt-simple-endpoint.style-scope.yt-formatted-string")
    
    ctime = driver.find_element_by_css_selector("#metadata-line > span:nth-child(2)").text
    print(ctime)
#     links = list(dict.fromkeys(map(lambda a: a.get_attribute("href"),url_list)))
#     pd.DataFrame(url_link).to_excel(f'{keyword}_.xlsx', header=False, index=False)
    return url_link

def getChannelDetails(urls): # get name, about, no. from about
    details = []
    for url in urls:
        driver.get(f"{url}/about")
        time.sleep(5)
        cname = driver.find_element_by_css_selector("#text.style-scope.ytd-channel-name").text #get channel name
        cdesc = driver.find_element_by_css_selector("#description-container > yt-formatted-string:nth-child(2)").text.rstrip() #get channel description
        i = "not given" #default value for contact no
        if re.search(r'\b\d\d\d\d\d\d\d\d\d\d\b', cdesc, flags=0): #_9876543210_
            for i in re.findall(r'\d\d\d\d\d\d\d\d\d\d',cdesc):
                print(f"contact no. {i}")
        elif re.findall(r'\b\d\d\d\d\d \d\d\d\d\d\b', cdesc, flags=0): #+_98765 43210_
            for i in re.findall(r'\b\d\d\d\d\d \d\d\d\d\d',cdesc):
                print(f"contact no. {i}")
        elif re.search(r'\d\d\d\d\d-\d\d\d\d\d\b', cdesc, flags=0): #+9198765-43210_
            for i in re.findall(r'\d\d\d\d\d-\d\d\d\d\d\b',cdesc):
                print(f"contact no. {i}")
        elif re.search(r'\b\d\d\d\d\d-\d\d\d\d\d', cdesc, flags=0): #_98765-43210_
            for i in re.findall(r'\b\d\d\d\d\d-\d\d\d\d\d',cdesc):
                print(f"contact no. {i}")
        clink = url
        # otherLinkObj = bot.find_elements_by_css_selector("#link-list-container.style-scope.ytd-channel-about-metadata-renderer a.yt-simple-endpoint.style-scope.ytd-channel-about-metadata-renderer")
        # otherLinks = list(dict.fromkeys(map(lambda a: a.get_attribute("href"),otherLinkObj)))
        
        obj = {                         #create dict of details
            
            "cname" : cname,
            "MOB" : i,
            "curl"  : clink,
            # "cdesc" : cdesc,
            # "otherLinks" : otherLinks
        }
        # details.append(obj)
        if i != "not given":
            details.append(obj)
    return details

def gettime():
    tm= str(datetime.now())
    tm=''.join(e for e in tm if e.isalnum())
    return tm


if __name__ == "__main__":
    gettime = gettime()
    allChannelUrls = getChannelUrl()
    allChannelDetails = getChannelDetails(allChannelUrls)
    pd.DataFrame(allChannelDetails).to_excel(f'{keyword}_{gettime}.xlsx', header=False, index=False) #convert list into excel
    
