from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import scrapy
import re
from scrapy.spiders import CrawlSpider


class NotikLaptopSpider(CrawlSpider):
    name = 'notik-scrapy'
    allowed_domains = ['notik.ru']
    start_urls = [
        'https://www.notik.ru/search_catalog/filter/brand.htm?page=1'
        ]

    def scrap_computers(self, response):

        for card in response.xpath("//tr[@class='goods-list-table']"):
            domen = 'https://www.notik.ru'
            url = card.xpath(
                ".//td[@class='glt-cell gltc-title show-mob hide-desktop']"
                ).xpath('.//a').attrib.get('href')
            name = card.xpath(
                ".//td[@class='glt-cell gltc-title show-mob hide-desktop']"
                ).xpath('.//a').css('::text').get()
            price_selector = card.xpath(
                ".//td[@class='glt-cell gltc-cart']"
                )
            price = re.findall(
                r'\d+', price_selector.xpath(".//b").css("::text").get())
            price = int("".join(price))
            cpu_hhz = card.xpath(
                ".//td[@class='glt-cell w4']"
                )[0].css('::text')[5].get().split()[0]
            ram_gb = card.xpath(
                ".//td[@class='glt-cell w4']"
                )[1].css('::text')[0].get().split()[0]
            ssd_gb = card.xpath(
                ".//td[@class='glt-cell w4']"
                )[1].css('::text')[6].get().split()[0]

            yield {
                'url': domen + url,
                'name': name,
                'cpu_hhz': int(cpu_hhz)/1000,
                'ram_gb': int(ram_gb),
                'ssd_gb': int(ssd_gb),
                'price_rub': price
            }

    def parse_start_url(self, response, **kwargs):
        for i in range(1, 12):
            url = (f'https://www.notik.ru/search_catalog'
                   f'/filter/brand.htm?page={i}')

            yield response.follow(
                url, callback=self.scrap_computers
            )


class MegaTehnikaSpider(scrapy.Spider):
    name = 'mega-tehnika-scrapy'
    allowed_domains = ['mega-tehnika.ru']
    start_urls = ['https://mega-tehnika.ru/catalog/noutbuki']

    def parse(self, response):
        for link in response.css('div.product__name a::attr(href)'):
            if '/prod/noutbuk' in str(link):
                yield response.follow(link, callback=self.parse_laptop)

        for i in range(2, 8):
            next_page = f'https://mega-tehnika.ru/catalog/noutbuki/?page={i}'
            yield response.follow(next_page, callback=self.parse)

    def parse_laptop(self, response):
        for card in response.xpath(
            "//div[@class='productDetail__descrPropOne']"
        ):
            cur_type = card.css("::text")[0].get().strip()
            cur_value = card.css("::text")[1].get().strip()
            if cur_type == 'Частота процессора (МГц)':
                cpu_hhz = int(cur_value)
            elif cur_type == 'Объем оперативной памяти (Гб)':
                ram_gb = int(cur_value)
            elif cur_type == 'Объем твердотельных накопителей SSD (Гб.)':
                ssd_gb = int(cur_value)

        yield {
            'url': response.url,
            'name': response.css('h1::text').get().strip(),
            'cpu_hhz': cpu_hhz / 1000,
            'ram_gb': ram_gb,
            'ssd_gb': ssd_gb,
            'price_rub': int("".join(re.findall(r'\d+', response.css(
                'div.productDetail__mainPrice::text').get())))
        }


settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(NotikLaptopSpider)
    yield runner.crawl(MegaTehnikaSpider)
    reactor.stop()


if __name__ == '__main__':
    crawl()
    reactor.run()
