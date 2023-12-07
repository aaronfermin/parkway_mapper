from datetime import datetime
from dateutil.parser import parse


class DataScraper:
    def __init__(self):
        self.url = None
        self.root_xpath = None
        self.el_xpath = None
        self.tree = None
        self.table_data = None
        self.last_update = None

    def scrape_table(self):
        self.get_site_contents()
        self.import_table()
        self.format_table()
        self.set_last_update()
        self.format_last_update()

    def scrape_element(self, *args):
        xpath = self.el_xpath if not args else args[0]
        return self.tree.xpath(self.root_xpath + xpath)

    def get_site_contents(self):
        response = requests.get(self.url)
        self.tree = html.fromstring(response.content)

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
