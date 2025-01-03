import scrapy


class BookSpider(scrapy.Spider):
    name = "book"
    start_urls = [
        "https://books.toscrape.com/"
    ]

    def parse(self, response):
        block_selector = ".col-xs-6.col-sm-4.col-md-3.col-lg-3"
        next_page_selector = ".pager .next a::attr(href)"

        # Extract book links and follow them
        for block in response.css(block_selector):
            first_a_href = block.xpath(".//a[1]/@href").get()

            if first_a_href:
                yield response.follow(first_a_href, callback=self.parse_book)

        # Handle pagination
        next_page = response.css(next_page_selector).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        yield {
            "title": response.css("h1::text").get(default="").strip(),
            "price": response.css("p.price_color::text").get(default="").strip(),
            "amount_in_stock": response.css("p.instock.availability::text").re_first(r"\d+"),
            "rating": response.css("p.star-rating::attr(class)").re_first(r"star-rating (\w+)"),
            "description": response.css("#product_description + p::text").get(default="").strip(),
            "upc": response.css("table > tr:nth-child(1) > td::text").get(default="").strip(),
        }
