import scrapy
import requests

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from scrapy.selector import Selector
from selenium.webdriver.firefox.options import Options

from lights_scraper.items import productItem
from lights_scraper.settings import FILES_STORE


class LightSpider(scrapy.Spider):
    name = "lights_co_uk"
    allowed_domains = ["lights.co.uk"]
    start_urls = [
        "https://www.lights.co.uk/philips-hue-white-color-impress-led-pillar-light.html"
    ]

    def parse(self, response):
        options = Options()
        options.headless = True
        options.binary_location = r"/var/lib/flatpak/app/org.mozilla.firefox/x86_64/stable/553fe334341e45e5e7232b508b510eac7d2d31a1ecc92d9c5103d9d91941325a/files/lib/firefox/firefox"
        driver = webdriver.Firefox(
            options=options, executable_path=GeckoDriverManager().install()
        )
        driver.get(
            "https://www.lights.co.uk/philips-hue-white-color-impress-led-pillar-light.html"
        )

        # click to get pdf link
        driver.find_element_by_class_name("download-file__link").click()

        sel = Selector(text=driver.page_source)

        # find and save pdf
        file = sel.css(".download-file__link::attr(href)").get()
        if file:
            pdf_url = response.urljoin(file)
            self.save_pdf(pdf_url)

        # find images
        file = sel.css(".gallery-image").xpath("@data-src")
        file_url = file.extract()

        yield productItem(file_urls=file_url)

    def save_pdf(self, url):
        name = url.split("/")[-1]
        r = requests.get(url)
        with open(f"{FILES_STORE}/{name}", "wb") as f:
            f.write(r.content)
