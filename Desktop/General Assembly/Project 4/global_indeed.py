# -*- coding: utf-8 -*-
import scrapy, requests
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class IndeedSpider(CrawlSpider):
    name = 'global'
    allowed_domains = ['indeed.com']
    start_urls = ['https://www.indeed.com/jobs?q=Insights&l=']

    rules = (
        Rule(LinkExtractor("start=.*"), callback='parse_item', follow = True),
        )
    
    def parse_item(self, response):
        
        print("-----------------------------------------------------")
        print("I JUST VISITED " + response.url)
        print("-----------------------------------------------------")

        soup = BeautifulSoup(response.text, 'lxml')
        divs = soup.find_all("div", class_ = ["row", "result"])
        
        for job in divs:
            item = {}

            item["id"] = job.get("id")

            try:
                item["company"] = job.find("span", class_ = "company").text.strip("\n").strip()
            except AttributeError:
                item["company"] = None

            item["title"] = job.a.get("title")

            item["loc"]= job.find("span", class_ ="location").text
            
            job_summ_page = job.get("data-jk")
            next_page_url = "https://www.indeed.com/viewjob?jk={}".format(job_summ_page)
            yield scrapy.Request(url = next_page_url, callback = self.parse_summ, meta=dict(item=item))


    def parse_summ(self, response):
        
        item = response.meta['item']
        
        soup = BeautifulSoup(response.text, 'lxml')
        item["summary"] = soup.find("span", class_ = "summary").text.replace("\n", " ")
        yield item

