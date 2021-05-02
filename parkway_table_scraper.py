from table_scraper import TableScraper
from datetime import datetime
from dateutil.parser import parse

class ParkwayTableScraper(TableScraper):

    def __init__(self):
        super().__init__()
        self.last_update = None

    def scrape_table(self):
        super().scrape_table()
        self.set_last_update()
        self.format_last_update()

    def set_last_update(self):
        headers = self.scrape_element('h3/text()')
        for header in headers:
            if (header.find('Road Status as of') != -1):
                self.last_update = self.parse_last_update(header)
                break

    def parse_last_update(self, header):
        pieces = header.split('as of')[1].split(' ')
        pieces = list(filter(lambda el: el not in ['', 'at'], pieces))
        pieces = list(map(lambda el: el.strip(',.'), pieces))
        last_update = ' '.join(map(str, pieces))
        return parse(last_update)

    def format_last_update(self):
        self.last_update = self.last_update.strftime('%Y/%m/%d, %H:%M:%S')

    def format_table(self):
        super().format_table()
        table = list()
        for row in self.table_data:
          mileposts = list(map(lambda el: el.strip(), row['parkway_mileposts'].split('-')))
          row['starting_milepost'] = min(mileposts)
          row['ending_milepost'] = max(mileposts)
          table.append(row)
        self.table_data =  table
