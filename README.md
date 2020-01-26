# simple-web-crawler

  - Install the packages:
    
    ```
    pip install -r requirements.txt
    ```

  - Start the simple spider:

    ```
    cd simplecrawler
    scrapy crawl simple -a allowed_domains="toscrape.com,scrapinghub.com"
    ```

  - Start url is configured in settings.py  
  - Test the filter:

    ```
    python -m unittest simplecrawler.tests.filters
    ```
  - Jobs: pausing and resuming crawls. Reference: https://docs.scrapy.org/en/latest/topics/jobs.html#jobs-pausing-and-resuming-crawls

    ```
    scrapy crawl simple -a allowed_domains="toscrape.com,scrapinghub.com" -s JOBDIR=crawls/simple-1
    ```