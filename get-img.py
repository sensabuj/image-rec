from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import datetime
import random
import urllib.request
from urllib.parse import quote
import pyodbc

# URl to web scrap from.

# page_url = "http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=-1&IsNodeId=1&Description=GTX&bop=And&Page=1&PageSize=36&order=BESTMATCH"

page_url = "http://127.0.0.1:5500/accordion.htm"



# opens the connection and downloads html page from url
uClient = uReq(page_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

# finds each product from the store page
containers = page_soup.findAll("div", {"class": "item-container"})

# name the output file to write to local disk
out_filename = "graphics_cards.csv"
# header of csv file to be written
headers = "item_name,item_image_src,item_image,item_data,created_on \n"

# opens file, and writes headers
f = open(out_filename, "w")
f.write(headers)

# DB instance
# conn = pyodbc.connect(driver = '{SQL Server}', server = '(local)', database = 'ImageClassify', Trusted_Connection='yes', autocommit=True)

# loops over each product and grabs attributes about
for container in containers:

    # the list of queries.
    item_name = container.a.img["title"].title()
    
    # item_image = 'https:' + quote(container.a.img["src"])
    item_image = 'http://127.0.0.1:5500/' + quote(container.a.img["src"])
    
    item_data = 'n/a'
    created_on = '{date:%Y-%m-%d_%H:%M:%S}'.format(date=datetime.datetime.now())
    name = random.randrange(1, 100)
    fullname = str(name) + ".jpg"
    print("item_image: ", item_image)
    urllib.request.urlretrieve(item_image, "download_raw_images//" + fullname)
    f.write(item_name + ", " + item_image + ", " + ", " + fullname + ", " + ", " + item_data + ", " + created_on + "\n")

    # Mapping with database
    Name = name
    Path = item_image
    Extension = 'jpg'
    ItemName = item_name
    ItemData = item_data
    FullName = fullname
    TypeName = 'card'

    # sql = """\
    # EXEC [dbo].[InsertImageMaster] @Name=?, @Path=?, @Extension=?, @ItemName=?, @ItemData=?, @FullName=?, @TypeName=?;
    # """
    values = (Name, Path, Extension, ItemName, ItemData, FullName, TypeName)
    # conn.execute(sql, values)

f.close()  # Close the file
