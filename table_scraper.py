from site_scraper import SiteScraper

class TableScraper(SiteScraper):

    def __init__(self):
        super().__init__()
        self.table_data = None

    def scrape_table(self):
        super().scrape_site()
        self.import_table()
        self.format_table()

    def import_table(self):
        rows = self.scrape_element()
        data = list()
        for row in rows:
            data.append([c.text_content().strip().replace('\n', ' ') for c in row.getchildren()])
        self.table_data = data

    def format_table(self):
        table = list()
        headers = self.table_data.pop(0)
        headers = list(map(lambda el: el.replace(' ', '_').lower(), headers))
        for row in self.table_data:
          table.append(dict(zip(headers, row)))
        self.table_data = table
