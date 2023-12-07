from data_scraper import DataScraper
from file_helper import FileHelper
from datetime import datetime, timedelta
from dateutil.parser import parse


class DataSyncer:

    def __init__(self):
        self.road_statuses = None
        self.last_update = None
        self.directory = 'data'
        self.file_name = 'parkway_data.json'
        self.file_path = '/'.join([self.directory, self.file_name])

    def sync(self):
        """
            checks if a data file already exists.
            if the file exists and the date on the file is old, run the scraping process
            if the file exists and the date is current, do nothing to avoid spamming the website
            if the file doesn't exist, run the scraping process
        """
        if FileHelper.file_exists(self.file_path):
            self.load_data_from_file()
            yesterday = datetime.today() - timedelta(days=1)
            if self.last_update < yesterday:
                self.scrape_and_save_table(move_file=True)
        else:
            self.scrape_and_save_table()

    def load_data_from_file(self):
        contents = FileHelper.load_json_file(self.file_path)
        self.road_statuses = contents.get('road_statuses')
        self.last_update = parse(contents.get('last_update'))

    def scrape_and_save_table(self, move_file=False):
        self.scrape_table()
        if move_file:
            self.move_old_file()
        self.save_data_to_file()

    def scrape_table(self):
        scraper = DataScraper()
        scraper.url = 'https://www.nps.gov/blri/planyourvisit/roadclosures.htm'
        scraper.root_xpath = '//div[@id="cs_control_6725830"]//div[contains(@class, "Component")]/'
        scraper.el_xpath = 'h3[text()="North Carolina Sections of Parkway"]/following-sibling::div/table/tbody/tr'
        scraper.scrape_table()
        self.road_statuses = scraper.table_data
        self.last_update = scraper.last_update

    def save_data_to_file(self):
        data = {
            'last_update': self.last_update,
            'road_statuses': self.road_statuses
        }
        FileHelper.save_json_file(self.file_path, data)

    def move_old_file(self):
        date = self.last_update.strftime('%Y%m%d')
        new_path = 'old_data/' + date + '_' + self.file_name
        FileHelper.move_file(self.file_path, new_path)
