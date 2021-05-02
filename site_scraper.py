from lxml import html
import requests
import pprint

class SiteScraper:

    def __init__(self):
        self.url = None
        self.root_xpath = None
        self.el_xpath = None
        self.tree = None

    def scrape_site(self):
        self.get_site_contents()

    def scrape_element(self, *args):
        # TODO: put el_xpath on table_scraper
        xpath = self.el_xpath if not args else args[0]
        return self.tree.xpath(self.root_xpath + xpath)

    def get_site_contents(self):
        response = requests.get(self.url)
        self.tree = html.fromstring(response.content)

    def pp(self, val):
        printer = pprint.PrettyPrinter()
        printer.pprint(val)
