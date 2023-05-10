import requests                         # for getting the page
import logging     
import re                               # for regex
from urllib.parse import urljoin
import multiprocessing      


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineon)d - %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


BASE_URL = "https://ssr1.scrape.center"
TOTAL_PAGE = 10


class Spider():
    def __init__(self, url=BASE_URL):
        self.url = url

        # for each page
        self.index_pattern = re.compile('<a.*?href="(.*?)".*?class="name">')
        # for each movie
        self.cover_pattern = re.compile('class="item.*?<imag.*?src="(.*?)".*?class="cover">', re.S)
        self.name_pattern = re.compile('<h2.*?>(.*?)</h2>')
        self.categories_parttern = re.compile('<button.*?category.*?<span>(.*?)</span>.*?</button>', re.S)
        self.pulished_at_pattern = re.compile('(\d{4}-\d{2}-\d{2})\s?上映')
        self.drama_pattern = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)
        self.score_patterm = re.compile('<p.*?score.*?>(.*?)</p>', re.S)

        # for storing info
        


    def scrape_page(self):
        """"Get the page, return its HTML"""
        logger.info(f"scraping {self.url} ...")
        try:
            response = requests.get(self.url)
            if response.status_code == requests.codes.ok:
                return response.text
            logger.error(f"get invalid status code {response.status_code} while scrape {self.url}")
        except requests.RequestException:
            logger.error(f"error occurred while scrape {self.url}", exc_info=True)


    def scrape_index(self, page):
        """Get each page's URL, and scrape it to get HTML"""
        index_url = f"{BASE_URL}/page/{page}"
        return self.scrape_page(index_url)
    

    def parse_index(self, html):
        """Parse the HTML, get each movie's URL"""
        items = re.findall(self.index_pattern, html)
        if not items:
            return []
        for item in items:
            detail_url = urljoin(BASE_URL, item)
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