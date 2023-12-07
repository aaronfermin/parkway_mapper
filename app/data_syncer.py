from datetime import datetime, timedelta

from dateutil.parser import parse

from data_scraper import DataScraper
from file_helper import FileHelper


class DataSyncer:

    def __init__(self):
        self.directory = 'data'
        self.file_name = 'parkway_data.json'
        self.file_path = '/'.join([self.directory, self.file_name])

    def sync(self, force_update: bool = False) -> None:
        """
            checks if a data file already exists.
            if the file exists and the date on the file is old, run the scraping process
            if the file exists and the date is current, do nothing to avoid spamming the website
            if the file doesn't exist, run the scraping process
        """
        if FileHelper.file_exists(self.file_path) and not force_update:
            last_update = self.get_last_update()
            yesterday = datetime.today() - timedelta(days=1)
            if last_update < yesterday:
                self.move_old_file(last_update)
                self.sync_table()
        else:
            self.sync_table()

    def get_last_update(self) -> datetime:
        """loads the existing file and returns the data timestamp to determine if we need to re-sync"""
        contents = FileHelper.load_json_file(self.file_path)
        return parse(contents.get('last_update'))

    def sync_table(self) -> None:
        scraper = DataScraper()
        scraper.url = 'https://www.nps.gov/blri/planyourvisit/roadclosures.htm'
        scraper.root_xpath = '//div[@id="cs_control_6725830"]//div[contains(@class, "Component")]/'
        scraper.table_xpath = 'h3[text()="North Carolina Sections of Parkway"]/following-sibling::div/table/tbody/tr'
        table_data = scraper.scrape()

        FileHelper.save_json_file(self.file_path, table_data)

    def move_old_file(self, last_update: datetime) -> None:
        new_path = 'old_data/' + last_update.strftime('%Y%m%d') + '_' + self.file_name
        FileHelper.move_file(self.file_path, new_path)
