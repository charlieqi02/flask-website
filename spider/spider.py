import requests                         # for getting the page
from colorLog import ColoredFormatter
import logging
import re                               # for regex
from urllib.parse import urljoin
from store import MysqlS


# Set logger
logger = logging.getLogger("Spider")
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

formatter = ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s")
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


# basic settings
BASE_URL = "https://ssr1.scrape.center"
TOTAL_PAGE = 10
SELECT_SQL = "\
    SELECT \n\
        LEFT(name, 10) AS name_simple, \n\
        categroies, pulished_at, score, \n\
        SUBSTRING(cover, CHAR_LENGTH(cover) - 23, 8) AS cover_simple, \n\
        CONCAT(LEFT(drama, 5), '...', RIGHT(drama, 5)) AS drama_simple \n\
    FROM \n\
        movie_info;"


class Spider():
    def __init__(self, url=BASE_URL):
        self.url = url

        # for each page
        self.index_pattern = re.compile('<a.*?href="(.*?)".*?class="name">')
        # for each movie
        self.cover_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)
        self.name_pattern = re.compile('<h2.*?>(.*?)</h2>')
        self.categories_parttern = re.compile('<button.*?category.*?<span>(.*?)</span>.*?</button>', re.S)
        self.pulished_at_pattern = re.compile('(\d{4}-\d{2}-\d{2})\s?上映')
        self.drama_pattern = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)
        self.score_patterm = re.compile('<p.*?score.*?>(.*?)</p>', re.S)

        # for storing info
        self.mysql = MysqlS()
        

    def main(self, select_sql=True):
        for page in range(1, TOTAL_PAGE+1):
            self.get_full_page_info(page)
        if select_sql:
            logger.info(f"if you want to see movie data in mysql, try this select sql: \n{SELECT_SQL}")
        

    
    def get_full_page_info(self, page):
        # create table in mysql to store info
        self.mysql.create_table()
        
        # get every movie's detail url in a page
        index_html = self.scrape_index(page)
        detail_urls = self.parse_index(index_html)

        # get every movie's info and store them in mysql
        for detail_url in detail_urls:
            # get movie's info
            detail_html = self.scrape_detail(detail_url)
            data = self.parse_detail(detail_html)            
            logger.info(f"get detail data {data['name']}")
            
            # get insert sql
            insert_sql = self.mysql.create_insert_sql(data)
            logger.info(f"get insert sql {insert_sql[:29]}")

            # save data
            self.mysql.insert_info(insert_sql)
            logger.info("data saved successfully\n")
        
        

    def scrape_page(self, url):
        """"Get the page, return its HTML"""
        logger.info(f"scraping {url} ...")
        try:
            response = requests.get(url, verify=False)
            if response.status_code == requests.codes.ok:
                return response.text
            logger.error(f"get invalid status code {response.status_code} while scrape {url}")
        except requests.RequestException:
            logger.error(f"error occurred while scrape {url}", exc_info=True)


    def scrape_index(self, page):
        """Get each page's URL, and scrape it to get HTML"""
        index_url = f"{self.url}/page/{page}"
        return self.scrape_page(index_url)
    

    def parse_index(self, html):
        """Parse the HTML, get each movie's URL"""
        logger.debug(f"index_pattern is : {self.index_pattern}; html is {html[:5] if html is not None else None}")
        items = re.findall(self.index_pattern, html)
        if not items:
            return []
        for item in items:
            detail_url = urljoin(self.url, item)
            logger.info(f"get detail url {detail_url}")
            yield detail_url


    def scrape_detail(self, url):
        """get each movie page's HTML"""
        return self.scrape_page(url)
    

    def parse_detail(self, html):
        """get movie page's detail infomation"""
        cover = re.search(self.cover_pattern, html).group(1).strip() \
                    if re.search(self.cover_pattern, html) else None
        name = re.search(self.name_pattern, html).group(1).strip() \
                    if re.search(self.name_pattern, html) else None
        categories = re.findall(self.categories_parttern, html) \
                    if re.findall(self.categories_parttern, html) else []
        pulished_at = re.search(self.pulished_at_pattern, html).group(1) \
                    if re.search(self.pulished_at_pattern, html) else None
        drama = re.search(self.drama_pattern, html).group(1).strip() \
                    if re.search(self.drama_pattern, html) else None
        score = float(re.search(self.score_patterm, html).group(1).strip()) \
                    if re.search(self.score_patterm, html) else None
        
        return {
            'cover': cover,
            'name': name,
            'categroies': categories,
            'pulished_at': pulished_at,
            'drama': drama,
            'score': score,
        }
    

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    sd = Spider()
    sd.main()