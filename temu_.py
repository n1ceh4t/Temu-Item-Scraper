from bs4 import BeautifulSoup

import requests

from time import sleep

import json

import os

from freeGPT import AsyncClient

import asyncio

from woocommerce import API

from random import randrange

import sys

wcapi = API(
    url="https://your.site.org/wp/",
    consumer_key="your consumer key",
    consumer_secret="your consumer secret",
    version="wc/v3"
)

categories = {
    "chargers" : "474",
    "game accessories" : "475",
    "headphones" : "377",
    "security" : "473",
    "smartwatches" : "378",
    "speakers" : "399",
}

master_list = []

proxies = {
   'http': 'http://p.r.o.xy:8888',
   'https': 'http://p.r.o.xyip:3128',
}

colors = [
        "blue",
        "green",
        "black",
        "white",
        "grey",
        "pink"
    ]

def scrape(url):
    html_document = getHTMLdocument(url)
    with open("product.html", "w+") as x:
        x.write(html_document)

# function to extract html document from given url
def getHTMLdocument(url):
    with requests.Session() as s:
        response = s.get(url, headers={"User-Agent" : "Mozilla/5.0 (Linux; Android 10; K)"}, allow_redirects=False)
        #response = s.get(url, headers={"User-Agent":"Mozilla/5.0"}, allow_redirects=False, proxies=proxies)  # For use with proxies
        with open("index.html", "w+") as x:
            x.write(response.text)
        return response.text

def init():
    temu = 'https://www.temu.com'

    search = '/search_result.html?search_key='

    keywords = input('What are you searching for?\n').replace(" ", "+")

    topParams = '&search_method=shade&refer_page_el_sn=200010&srch_enter_source=top_search_entrance_10005&_x_sessn_id=&refer_page_name=home&refer_page_id=10005_1696179570382_n3gduua9yo&refer_page_sn=10005&filter_items=1%3A1'

    temp = '<script type="application/ld+json">'

    url = temu + search + keywords + topParams

    #print(url)

    html_document = getHTMLdocument(url)
    
    soup = BeautifulSoup(html_document, 'html5lib')
    
    link_list = []

    for link in soup.find_all('a', attrs={'aria-label' : ''}):
        # display the actual urls
        temp = link.get('href')
        link_list.append(temu + link.get('href'))

    parsed_list = []
        
    for x in link_list:
        if ".html" in x:
            if "%" not in x:
                if "search" not in x:
                    if "/channel/" not in x:
                        if "/attendance/" not in x:
                            parsed_list.append(x)

    if parsed_list == []:
        print("List from search was empty. Retrying in 500 seconds...")
        sleep(500)
        main()
        exit()
    
    return parsed_list

def download(url, file, name):
    url = url
    r = requests.get(url, allow_redirects=False)
    open(name + "/" + file, 'wb').write(r.content)

def downloadProduct(url, file):
    with requests.Session() as s:
        response = s.get(url, headers={"User-Agent" : "Mozilla/5.0 (Linux; Android 10; K)"}, allow_redirects=False)
        #response = s.get(url, headers={"User-Agent":"Mozilla/5.0"}, allow_redirects=False, proxies=proxies)  # For use with proxies
        with open(file, "w+") as x:
            x.write(response.text)
        return response.text

def trimURL(url):
    return url.split("/")[6]

def getColors(desc):
    print(desc)
    for color in colors:
        if color in desc:
            print("Color found.")
            return color
        else:
            print("Color not found.")
            return "Undefined."

def parse_product(url):
    if len(url) > 4:
        try:
            os.remove("product.html")
        except:
            pass
        downloadProduct(url, "product.html")
    else:
        pass

    link_list = []
    parsed_list = []
    final_list = []
    image_list = []
    csv = []



    html_document = open("product.html", "r")
    soup = BeautifulSoup(html_document, 'lxml')

    for link in soup.find_all('script', type='application/ld+json'):
        temp = link.string
        link_list.append(temp)

    for x in link_list:
        if "BreadcrumbList" not in x:
            parsed_list.append(json.loads(x))

    print(parsed_list)

    if parsed_list:

        for i in parsed_list:
            try:
                print("Checking product...")
                if i['@type'] == 'Product': # scrape images first
                    print("checking name...")
                    if i['name']:
                        print("name found...")
                        name = ''.join([i for i in i['name'] if i.isalpha()])
                        pname = i['name']
                        print(name)
                        #os.mkdir(name) # make working directory for the item by product name (debug)
                    else:
                        print("Error getting name.")
                    print(i['image'][0])

                    price = i['offers']['price']
                    csv.append(price)

                    print("image list was not found.")
                    color = getColors(i['image'][0]['description'])
                    image_list.append([color, i['image'][0]['contentURL']]) # if image_list not populated, create the first item

                    for x in i['image']: # iterate through all image entries
                        t = 0
                        print("iterating images...")
                        if image_list:  # if image_list is populated, ensure no duplicate entries
                            print("image list was found.")
                            for p in image_list:
                                if x['contentURL'] == p[1]:  # ensure no duplicate entries
                                    print("Duplicate image found.")
                                    pass
                                else:
                                    print("No duplicate found.")
                                    try:
                                        if ".jpg" in x['contentURL']:
                                            color = getColors(i['image'][t]['description']) # try to find color in short description
                                            image_list.append([color, x['contentURL']]) # add new images to the list
                                        else:
                                            pass
                                    except:
                                        pass
                                t+=1
                                #print("image:")
                                #pimage = i["image"][0]["contentURL"] # save images
                        else:
                            pass                
                    


                    print("Short Description:")
                    short_description = i["image"][0]["description"] # save short description
                    print(short_description)


                print("Long description:")
                long_description = i["description"]
                print(long_description)
                

                if i['@type'] == 'VideoObject':
                    print("Video:")
                    if i["contentURL"]:
                        video = i['contentURL'] # save videos
                    else:
                        video = "No video."
                    csv.append(video)    
                else:
                    video = "No video."
                    csv.append(video)         
            except:
                print("Error parsing schema.")
                break
            csv.append(short_description)
            csv.append(long_description)
            csv.append(pname)
            csv.append(image_list)
            
            #with open(name + "/" + name + ".json", "a+") as x: # debug
                    #x.write(json.dumps(csv)) # debug
            break   
        return csv
    else:
        pass

async def gpt(prompt, desc):
    if prompt == 'short':
        description = "Reply only with the reworded description. I would like you to reword the following description in less than 20 words (Do not use the word 'Introducing'):" + desc
    elif prompt == 'long':
        description = "Reply only with the reworded description. I would like you to reword the following description in less than 250 words:" + desc
    elif prompt == 'tags':
        description = "Reply only with comma seperated tags. I would like you to generate 10 tags seperated by comma for the following description: " + desc
    try:
        resp = await AsyncClient.create_completion("gpt4", description)
        sleep(5)
        print({resp})
        return resp
    except Exception as e:
        print(f"🤖: {e}")
        return "error"

def addItem(data):
    print(wcapi.post("products", data).json())

#print(wcapi.delete("products/1448", params={"force": True}).json()) 

def crap(info):
    print(info)
    if sys.argv[2]:
        cat = sys.argv[2]
    else:
        cat = input('In which category does this belong?\n(chargers, game accessories, headphones, security, smartwatches, speakers)\n')

    if categories[cat]:
        pass
    else:
        print("Invalid category selection.")
        exit()    

    data = {
                "name": info[4],
                "type": "simple",
                "sale_price": str(round(float(info[0])*2.5, 2)),
                "regular_price": str(round(float(info[0])*4.0, 2)),
                "description": asyncio.run(gpt("long", info[2])).replace("\n", " "),
                "short_description": asyncio.run(gpt("short", info[2])).replace("\n", " "),
                "shipping_required": "true",
                "status": "draft",
                #"tags": str(asyncio.run(gpt("tags", info[2])).replace("\n", " ")).split(", "), #implement tags
                "on_sale": "true",
                "categories": [
                    {
                        "id": categories[cat]
                    }
                ],
                "images": [
                    {
                        "src": info[5][0][1]
                    }
                ]
            }
    
    addItem(data)

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        info = parse_product(url)
        crap(info)
        return
    choice = input('Would you like to import a single product? (y/n)\n')
    if choice == 'y':
        url = input('Please enter the product URL:\n')
        info = parse_product(url)
        crap(info)
        return
    else: 
        pass

    parsed_list = init()

    for i in parsed_list:
        print(i)
        print("Sleeping for 100-400 seconds...")
        sleep(randrange(100,400))
        scrape(i)
        info = parse_product('x') #any data less than length of 4 can be put here. Better code to come.
        master_list.append(info)
        crap(info)


    os.remove("index.html")
    return

main()
