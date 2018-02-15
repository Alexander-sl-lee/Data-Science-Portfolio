# -*- coding: utf-8 -*-
import scrapy
import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import requests
import pprint

from bs4 import BeautifulSoup

class WhirlpoolSpider(scrapy.Spider):
    name = 'Whirlpool'
    allowed_domains = ['http://forums.whirlpool.net.au']
    start_urls = ['http://forums.whirlpool.net.au/forum-replies.cfm?t=2691997']

    def parse(self, response):

        
        
        self.log('------------------------------------')
        self.log('I just visited: ' + response.url)
        self.log('------------------------------------')
           
        r = requests.get('http://forums.whirlpool.net.au/forum-replies.cfm?t=2691997')
        soup = BeautifulSoup(r.text, "lxml")

        test = soup.find_all("div", class_="replytext bodytext")

        for i in test:
            item = {}

            item["comment"] = i.text.strip()
            yield item

