# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from klsebuddybot.items import KlsebuddybotItem
import re
import datetime


class AppSpider(scrapy.Spider):
    name = 'app'
    allowed_domains = ['klse.i3investor.com', 'cdn1.i3investor.com']
    start_urls = ['https://klse.i3investor.com/jsp/pt.jsp']
    today = datetime.date.today().strftime("%d/%m/%Y")

    def parse(self, response):
        """
        Price target listing: https://klse.i3investor.com/jsp/pt.jsp
        """
        for tr in response.css('table.nc tr').extract():
            tr = re.findall(r'<td class="left">(.*?)</td>', tr)
            if len(tr) == 0: continue
            tr_date, tr_href, tr_analyst = tr
            # if tr_date == self.today:
            if tr_date == '27/10/2020':
                tr_href = re.findall(r'<a href="(.*?)" target="_top"', tr_href)[0]
                yield Request('https://klse.i3investor.com'+tr_href, callback=self.get_reports)

    def get_reports(self, response):
        """
        Individual stock reports: https://klse.i3investor.com/servlets/ptg/1818.jsp
        """
        for report_row in response.xpath('//td[@id="main-content-cell"]/table[5]/tr').extract():
            date_analyst = re.findall(r'<td class="left">(.*?)</td>', report_row)
            if len(date_analyst) == 0: continue
            report_date, report_analyst = date_analyst
            # if report_date == self.today:
            if report_date == '27/10/2020':
                report_href = re.findall(r'<a href="(.*?)"> <img', report_row)[0]
                yield Request('https://klse.i3investor.com'+report_href, callback=self.get_staticfile)
    
    def get_staticfile(self, response):
        """
        Report page: https://klse.i3investor.com/servlets/ptres/57317.jsp
        """
        staticfile = response.xpath('//p[@class="mtop10"]/a/@href').get()
        if staticfile != None:
            yield Request('https://klse.i3investor.com'+staticfile, callback=self.get_pdf)

    def get_pdf(self, response):
        file_title = response.css('div#maincontent730 h2::text').get()
        file_title = file_title.split(' - ')[1].replace(' ', '_')
        file_url = response.xpath('//*[@id="maincontent730"]/div[1]/a/@href').get()
        file_url = response.urljoin(file_url)
        file_extension = file_url.split('.')[-1]
        if file_extension not in ('pdf'):
            return

        item = KlsebuddybotItem()
        item['file_urls'] = [file_url]
        item['file_title'] = file_title
        item['date'] = self.today
        yield item


