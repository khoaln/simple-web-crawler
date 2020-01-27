# Simple Web Crawler
The assignment is implemented using [Scrapy](https://scrapy.org/) framework. It consists of a simple crawler that can travel the websites and download images based on user input.

## Simple Crawler
### Setup:
  - Install the packages:
    ```
    pip install -r requirements.txt
    ```
  - Create some necessary folders under "simplecrawler/simplecrawler":  `logs`, `media/images`, `output`. You can find and change the name of the folders in `settings.py`.

### Features:
  - From the root folder, enter the `simplecrawler` subfolder before running commands.
  - Start the simple crawler with a command as follow:
    ```
    scrapy crawl simple -a allowed_domains="dooa.no,dyreklinikk.no" -a search=katt -s JOBDIR=crawls/simple-1
    ```
  - The start URL is configured in `settings.py`
  - In order to restrict the traversal by one or several domains, add the allowed_domains argument to the command: `-a allowed_domains="dooa.no,dyreklinikk.no"`
  - The crawler never visit the same site twice: In the filter class `VisitedSiteFilter`, requested urls are stored in a MongoDB database. Their sha1 hashed value is used as the id. For the new requests, the Scrapy engine will check and filter out the urls that exist in the database.
  - Adding argument `-s JOBDIR=crawls/simple-1` to the command will make the crawler to remember its state. Each job should have a separate directory to store the state. The last requested url will be stored in the state of class `SimpleSpider`. When the crawler is resumed, it checks for the last url in the state.
  - Users can download the images for a specific search. There's a simple approach to reduce the number of downloading: Adding `-a search=katt` argument, then the crawler only download the images that have "katt" in their `src` or `alt` attributes or in the title of the web page.

### Testing:
  - Run the unittest for the filters:
    ```
    python -m unittest simplecrawler.tests.filters
    ```
  - A simple check on various constraints for how the callback processes the response using spider contracts:
    ```
    scrapy check
    ```

### Discussion:
  - Using Scrapy can build a high performance crawler since it uses asynchronous system calls. Scrapy provides lots of useful features such as proxies, data pipeline, etc. It's also customizable and extensible. One disadvantage compared to building from scratch is that we have to rely on third party framework, truly understand it in order to customize.
  - The current implementation can get banned by the websites. To improve it, we can add middlewares to rotate the user agent and IP when making the requests.
  - The current approach can miss some relevant images. We can improve by also searching for the text around the image tag.
  - This solution can be scaled for a distributed environment:
    - If we have to crawl from many domains, we can partition the domain list and have one crawler instance to process each part. The crawlers can run on different servers. We can implement the Master-Slave model whereas each crawler is a slave. The following requests will be sent to the Master and the Master can control which slave to process them based on the requested domain.
    - MongoDB can be hosted on a separate server so all crawlers can persist the data and access to check visited urls.
    - Instead of storing downloaded images locally, the crawlers can upload them to Amazon S3 or Google Cloud with Scrapy built-in feature supports.
