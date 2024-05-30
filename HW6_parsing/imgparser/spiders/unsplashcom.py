import scrapy
from scrapy.loader import ItemLoader
from imgparser.items import ImgparserItem


class UnsplashcomSpider(scrapy.Spider):
    name = "unsplashcom"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response):
        categories = response.xpath("(//ul)[last()]//a[not(text()='Unsplash+') and not(text()='Editorial')]/@href")
        for category in categories:
            yield response.follow(url=category, callback=self.img_parse)

    def img_parse(self, response):

        list_url = response.xpath("//img[@data-test]")
        for item in list_url:
            loader = ItemLoader(item=ImgparserItem(), response=response)
            loader.add_xpath('category', '//h1/text()')
            url = item.xpath('./@src').get()
            name = item.xpath('./@alt').get()
            loader.add_value('url', url)
            loader.add_value('name', name)
            yield loader.load_item()

