import scrapy

#提取数据
# scrapy shell "http://quotes.toscrape.com/page/1/"

#运行命令
#scrapy crawl quotes -o quotes.jl

# 查看带有 response 对象的 CSS 选择元素：
# response.css('title')
# [<Selector xpath='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]

class QuotSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        #查看带有 response 对象的 CSS 选择元素：
        response.css('title')# [<Selector xpath='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]

        response.css('title::text').extract()# ['Quotes to Scrape']
        response.css('title::text')[0].extract()
        response.css('title::text').extract_first() # 'Quotes to Scrape'


        response.css('title').extract()#['<title>Quotes to Scrape</title>']

        response.xpath('//title')#[<Selector xpath='//title' data='<title>Quotes to Scrape</title>'>]
        response.xpath('//title/text()').extract_first() # 'Quotes to Scrape'

        #查看author 和quote:
        queote = response.css("div.quote")
        title = queote.css("span.text::text").extract_first()
        author = queote.css("span.author::text").extract_first()
        tags = queote.css("div.tags a.tag::text").extract_first()

        # follow links to author pages
        for href in response.css('.author+a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                callback=self.parse_author)

        # 读取当前页的下一页内容 跟进链接
        next_page = response.css("li.next a::attr(href)").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_author(self,response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name' : extract_with_css("h3.author-title::text").extract_first(),
            'brithday' : extract_with_css(".author-born-date::text").extract_first(),

        }
