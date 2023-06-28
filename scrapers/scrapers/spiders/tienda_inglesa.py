from typing import Iterator

from requests.utils import requote_uri
from scrapy import signals
from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapers.azure_helpers import append_file_to_blob
from scrapers.items import PropertyItem

import os
class TiendaInglesaSpider(CrawlSpider):
    name = "tienda_inglesa"
    custom_settings = {
        "USER_AGENT": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ),
        "FEEDS": {
            'properties_tienda_inglesa.jl':{"format":"jsonlines"}
        },
        "max_items_per_label": 1,
        "label_field": "property_type",
        "CLOSESPIDER_ITEMCOUNT": 1,
        "DEPTH_LIMIT":os.environ.get("MAX_ITEMS")
    }
    start_urls = [
       "https://www.tiendainglesa.com.uy/busqueda?0,0,*:*,78,0,0,,%5B%5D,false,%5B%5D,%5B%5D,,0",
       "https://www.tiendainglesa.com.uy/busqueda?0,0,*:*,1894,0,0,,%5B%5D,false,%5B%5D,%5B%5D,,0",
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    [
                        r"\/busqueda\?0,0,\*:\*,(78|1894).*",
                    ]
                )
            )
        ),
        Rule(LinkExtractor(allow=(r"\/[A-Za-z0-9-.]+producto\?[0-9]+,,[0-9]+")), callback="parse_property"),
    )

    def parse_property(self, response: HtmlResponse) -> Iterator[dict]:
        print(response.css)
        def get_with_css(query: str) -> str:
            return response.css(query).get(default="").strip()

        # property details
        property_id = get_with_css("#TXTPRODUCTCODE::text").split(" ")[-1]
        img_urls = get_with_css("#vVARMAINPRODUCTPICTURE::attr('src')")
        img_urls = [[img for img in img_urls.split(",") if img][0]]
        possible_types = {
            "78": "WAREHOUSE",
            "1894": "FRESH",
            "1001": "DRINKS",
            "181": "CLEANING",
            "1895": "FROZEN",
            "569": "TOY",
            "302": "TECHNOLOGY",
            "618": "HOME",
            "4677": "FITNESS",
            "1005": "PERFUMERY"
        }

        # every property has this fixed list of details on tienda_inglesa (Ver si esta bien tomado desde ahi)
        category = get_with_css(".wBreadCrumbText a:nth-child(2)::attr('href')").split("/")[-1]
        product_name=get_with_css("#SECTIONH1::text")
        property_type = possible_types.get(category,'UNDEFINED')

        property = {
            "id": property_id,
            "image_urls": img_urls,
            "source": "tienda_inglesa",
            "url": requote_uri(response.request.url),
            "link": requote_uri(response.request.url),
            "property_type": property_type,
            "product_name":product_name,
        }
        yield PropertyItem(**property)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(TiendaInglesaSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.logger.info("Spider closed: %s", spider.name)
        for uri, _ in self.settings.getdict("FEEDS").items():
            append_file_to_blob(uri)
