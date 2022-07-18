import scrapy
from scrapy_playwright.page import PageCoroutine


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    n_of_items = 0
    final_n_of_items = 200
    # allowed_domains = ['test.com']
    # start_urls = ['http://test.com/']

    def start_requests(self):
        yield scrapy.Request('https://www.sreality.cz/hledani/prodej/byty',
                             meta=dict(
                                 playwright=True,
                                 playwright_include_page=True,
                                 playwright_page_coroutines=[
                                     PageCoroutine('wait_for_selector', 'div.dir-property-list')
                                 ],
                             )
                             )

    async def parse(self, response):
        for flat in response.css('div.property.ng-scope'):
            if self.n_of_items >= self.final_n_of_items:
                break
            name = flat.css('span.name.ng-binding::text').get()
            location = flat.css('span.locality.ng-binding::text').get()
            price = flat.css('span.norm-price.ng-binding::text').get()
            images = flat.css('preact.ng-scope.ng-isolate-scope img::attr(src)').extract()
            yield {
                'title': '{}, {}'.format(name, location),
                'price': price,
                'image': images,
            }
            self.n_of_items += 1
        # Finding the next page
        next_page = response.css('a.btn-paging-pn.icof.icon-arr-right.paging-next').attrib['href']
        splitter = '/{}'.format(next_page.split('/')[1])
        base_url = response.url.split(splitter)[0]
        next_page = base_url+next_page

        if next_page is not None and self.n_of_items < self.final_n_of_items:
            yield response.follow(next_page, callback=self.parse,
                                  meta=dict(
                                      playwright=True,
                                      playwright_include_page=True,
                                      playwright_page_coroutines=[
                                          PageCoroutine('wait_for_selector', 'div.dir-property-list')
                                      ],
                                  )
                                  )
