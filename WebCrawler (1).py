import urllib.request
import re

page_count = 100
to_crawl = []
dictText = {}
dictPage = {}

def recurseCrawl(link, file):
    global page_count
    global to_crawl
    global dictText
    global dictPage
    page = urllib.request.urlopen(link)
    #tries to decode page, returns a step if not able to
    try:
        output = page.read().decode('utf-8')
    except:
        return
    links = re.findall('<a\s*href=[\'|"](.*?)[\'"].*?>', output)
    texts = re.findall('>([\?\w*\s?.*]+)</a>', output)
    file.write(link)
    for url in links:
        if "http" in url:
            file.write("," + url)
    file.write("\n")
    #begins iterating through the list of links
    for i in range(0, len(links) - 1):
        if texts[i] in dictText:
            dictText[texts[i]] = dictText.get(texts[i]) + 1
        else:
            dictText[texts[i]] = 0
        #checks to see if the max amount of pages has been reached yet
        if "http" in links[i]:
            #file.write(str(links[i]) + " ,")
            #checks to see if the next link is a valid url
            if page_count > 0:
                print(links[i])
                #if the link is already indexed, adds one to how many times
                #its been found, otherwise adds it into dictPages, and appends it
                #to to_crawl
                if links[i] in dictPage:
                    dictPage[links[i]] = dictPage.get(links[i]) + 1
                else:
                    page_count = page_count - 1
                    dictPage[links[i]] = 0
                    to_crawl.append(links[i])
        else:
            break
    while len(to_crawl) > 0:
        #tries to open the next link and catches the
        #exception if the page denies access or is an invalid page
        try:
            recurseCrawl(to_crawl.pop(0), file)
        except:
            print("Access Denied")
    return
class WebCrawler:
    global to_crawl
    global dictPage
    f_out = open("crawloutput.csv", 'w')
    f_out.write("Page" + "," + "Links")
    f_out.write("\n")
    fileIn = open("urls.txt", 'r')
    for line in fileIn:
        to_crawl.append(line)
    recurseCrawl(to_crawl.pop(0), f_out)
    b = max(dictPage, key = dictPage.get)
    f_out.write(b + " is the top link with" + "," + str(dictPage.get(b)) + " iterations")
    f_out.close()
    print(dictPage)
        
    

