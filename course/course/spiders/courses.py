import scrapy


class CoursesSpider(scrapy.Spider):
    name = "courses"
    allowed_domains = ["utoronto.ca"]
    start_urls = [
        "https://artsci.calendar.utoronto.ca/search-courses?page=0",
        "https://utsc.calendar.utoronto.ca/search-courses", "https://utm.calendar.utoronto.ca/course-search"
    ]

    def parse(self, response):
        courses = response.xpath('//div[@class="view-content"]/div[@class="views-row"]')
        for course in courses:
            name = course.xpath('./h3/div/text()')[0].extract()  # course number and title
            br = course.xpath(
                './div/span[@class="views-field views-field-field-breadth-requirements"]/span/text()').extract()
            pre = course.xpath(
                './div/span[@class="views-field views-field-field-prerequisite"]/span/a/text()').extract()
            distribution = course.xpath(
                './div/span[@class="views-field views-field-field-distribution-requirements"]/span/text()').extract()
            exclusion = course.xpath(
                './div/span[@class="views-field views-field-field-exclusion"]/span/a/text()').extract()
            introduction = course.xpath('./div/div[@class="views-field views-field-body"]/div/p/text()').extract()
            yield {'name': name, 'br': br, 'pre': pre, 'distribution': distribution, 'exclusion': exclusion,
                   'introduction': introduction}
        part = response.xpath('//nav[@class="w3-center pager"]/ul/li[last()-1]/a/@href').extract_first()
        if part:
            yield scrapy.Request(response.urljoin(part), callback=self.parse)
