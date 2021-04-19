from parkway_table_scraper import ParkwayTableScraper
from file_helper import FileHelper
from datetime import datetime, timedelta
from dateutil.parser import parse

class NcParkwayScraper():

    def __init__(self):
        self.table_data = None
        self.last_update = None
        self.file_path = 'data/'
        self.file_name = 'nc_parkway_data.json'

    def load_table_data(self):
        path = self.file_path + self.file_name
        if FileHelper.file_exists(path):
            self.load_data_from_file()
            yesterday = datetime.today() - timedelta(days = 1)
            if self.last_update < yesterday:
                self.move_old_file()
                self.scrape_and_save_table()
        else:
            self.scrape_and_save_table()

    def scrape_and_save_table(self):
        self.scrape_table()
        self.save_data_to_file()

    def scrape_table(self):
        nc_table_scraper = ParkwayTableScraper()
        nc_table_scraper.url = 'https://www.nps.gov/blri/planyourvisit/roadclosures.htm'
        nc_table_scraper.root_xpath = '//div[@id="cs_control_6725830"]//div[contains(@class, "Component")]/'
        nc_table_scraper.el_xpath = 'h3[text()="North Carolina Sections of Parkway"]/following-sibling::div/table/tbody/tr' #preceding-sibling for VA
        nc_table_scraper.scrape_table()
        self.table_data = nc_table_scraper.table_data
        self.last_update = nc_table_scraper.last_update

    def load_data_from_file(self):
        path = self.file_path + self.file_name
        contents = FileHelper.load_json_file(path)
        self.table_data = contents['road_data']
        self.last_update = parse(contents['last_update'])

    def save_data_to_file(self):
        path = self.file_path + self.file_name
        data = {
          'last_update': self.last_update,
          'road_data': self.table_data
        }
        FileHelper.save_json_file(path, data)

    def move_old_file(self):
        path = self.file_path + self.file_name
        date = self.last_update.strftime('%Y%m%d')
        new_path = 'old_data/' + date + '_' + self.file_name
        FileHelper.move_file(path, new_path)