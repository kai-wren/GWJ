import json
from urllib import request
from bs4 import BeautifulSoup
from tqdm import tqdm
"""
Simple helper to retrieve biorxiv articles for a given search query.
"""

DEFAULT_URL = {
    'rxivist':
    'https://api.rxivist.org/v1/papers?q={}&timeframe=alltime&metric=downloads&page_size=100&page={}',
    'biorxiv':
    'https://www.biorxiv.org/search/{}%20numresults%3A25%20sort%3Apublication-date%20direction%3Adescending'
}


class BiorxivRetriever():
    def __init__(self, search_engine='biorxiv', search_url=None):
        assert search_engine in ['biorxiv', 'rxivist']
        self.search_engine = search_engine
        self.serach_url = search_url or DEFAULT_URL[search_engine]
        return

    def _get_all_links(self, page_soup, base_url="https://www.biorxiv.org"):
        links = []
        for link in page_soup.find_all(
                "a", {"class": "highwire-cite-linked-title"}, limit=10):
            uri = link.get('href')
            links.append({'title': link.text, 'biorxiv_url': base_url + uri})

        return links


    def _get_papers_list_biorxiv(self, query):
        papers = []
        url = self.serach_url.format(query)
        page_html = request.urlopen(url).read().decode("utf-8")
        page_soup = BeautifulSoup(page_html, "lxml")
        links = self._get_all_links(page_soup)
        papers.extend(links)

        page_links = page_soup.find_all("li", {"class": "pager-item"}, limit=3)
        if len(page_links) > 0:
            page_url = url + '?page={}'.format(1)
            page_html = request.urlopen(page_url).read().decode("utf-8")
            page_soup = BeautifulSoup(page_html, "lxml")
            links = self._get_all_links(page_soup)
            papers.extend(links)
        return papers

    def query(self, query, metadata=True, full_text=True):
        query = query.replace(' ', '%20')

        if self.search_engine == 'biorxiv':
            papers = self._get_papers_list_biorxiv(query)
        else:
            raise Exception('None implemeted search engine: {}'.format(
                self.search_engine))

        return papers