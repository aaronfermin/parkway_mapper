import requests
from dateutil.parser import parse
from lxml import html


class DataScraper:
    def __init__(self):
        self.url = None
        self.site_contents = None
        self.root_xpath = None
        self.table_xpath = None
        self.data = None
        self.last_update = None

    def scrape(self) -> dict:
        """
            - gets the site contents and stores it as an html tree
            - scrapes the table and converts it to a nice dict
            - scrapes the site for `last_update` to use in determining data freshness
            - returns both data points for the coordinate mapper to consume
        """
        response = requests.get(self.url)
        site_contents = html.fromstring(response.content)

        return {
            'last_update': self.get_last_update(site_contents),
            'road_statuses': self.scrape_table(site_contents),
        }

    def scrape_table(self, site_contents) -> list:
        """
            - gets the table using @self.table_xpath
            - removes the header row from the table, unneeded as I'm using hardcoded keys
            - converts each row to an array & strips each cell to avoid uggo whitespace
            - maps the array to a dict for easier downstream consumption
        """
        # the first row is headers, don't really need them as I'm using hardcoded keys below
        table = site_contents.xpath(self.root_xpath + self.table_xpath)
        del table[0]

        parsed_table = []
        for row in table:
            cell = [c.text_content().strip().replace('\n', ' ') for c in row.getchildren()]

            row_data = {
                'mileposts': cell[0],
                'crossroads': cell[1],
                'status': cell[2],
                'notes': cell[3],
            }
            parsed_table.append(row_data)

        return parsed_table

    def get_last_update(self, site_contents) -> str:
        """
            - find the appropriate header with the data timestamp
            - strip out all the non-date-y characters & whitespaces from the string
            - convert the date string (ex: "11:00 a.m., Thursday, December 7th, 2023.") to a date obj
            - return a formatted str representing the last time the site's data was updated
        """

        def find_as_of_header():
            # there's not a convenient way to get the 'status as of' header directly, so just loop until the str matches
            headers = site_contents.xpath(self.root_xpath + 'h3/text()')
            for header in headers:
                if 'road status as of' in header.lower():
                    return header

        as_of_header = find_as_of_header()
        as_of = as_of_header.split('as of')[1]
        pieces = [x.strip(',.') for x in as_of.split(' ') if x not in ['', 'at']]
        last_update = ' '.join(pieces)
        update_date = parse(last_update)
        return update_date.isoformat()
