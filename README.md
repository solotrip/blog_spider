# Blog Spider

Generic spider for extracting information from blog posts.

## Install dependencies

```
pip install -r requirements.txt
```


## Spider

This spider depends on `sitemap.xml` files to scrape every blog post in given domains.

The output file format is `domain_YYYY-MM-DD-hh-mm-ss.jsonl`


```
scrapy crawl generic -a start_urls=https://www.nomadicmatt.com,https://worldofwanderlust.com -s  OUTPUT_PATH=crawled/
```
### Parameters 

- *start_urls* : Comma separated lists of domains to be crawled

