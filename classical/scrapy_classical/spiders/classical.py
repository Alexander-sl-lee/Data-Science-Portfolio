# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from bs4 import BeautifulSoup


class ClassicalSpider(CrawlSpider):
    name = 'classical'
    allowed_domains = ['classicalmusicdb.com']
    start_urls = ['http://www.classicalmusicdb.com/composers']

    rules = (
        Rule(LinkExtractor("/composers/view/"), callback='parse_songs', follow = True),
    )

    def parse_author(self, response):
        print("-----------------------------------------------------")
        print("I JUST VISITED " + response.url)
        print("-----------------------------------------------------")
        
        # Parses page into soup
        soup = BeautifulSoup(response.text, 'lxml')

        # Grabs li elements containing authors and href links
        composer_list = soup.find_all('li')

        for composer in composer_list:

            # Creates the links to the songs
            songs_url = "https://www.indeed.com/viewjob?jk={}".format(composer.a['href'])
            
            yield scrapy.Request(url = songs_url, callback = self.parse_songs)
            
    def parse_songs(self, response):
        
        item = {}
        
        soup = BeautifulSoup(response.text, 'lxml')
        songs = soup.find_all('tr')[1:]

        for song in songs:
            item['composer_name'] = response.meta['link_text']

            try:
                item['BWV'] = song.find('td', {'title':'BWV'}).text
            except AttributeError:
                item['BWV'] = "-"
                
            item['OP'] = song.find('td', {'title':'Op.'}).text
            item['NO'] = song.find('td', {'title':'No.'}).text
            item['Instrumentation'] = song.find('td', {'title':'Instrumentation'}).text
            item['Type'] = song.find('td', {'title':'Type'}).text
            item['Work No'] = song.find('td', {'title':'Work No.'}).text
            item['Collection'] = song.find('td', {'title':'Collection'}).text
            item['Aggregated Level'] = song.find('td', {'title':'Aggregated Level'}).text
            item['RCM'] = song.find('td', {'title':'RCM'}).text
            item['ABRSM'] = song.find('td', {'title':'ABRSM'}).text
            item['Henle'] = song.find('td', {'title':'Henle'}).text
            yield item


