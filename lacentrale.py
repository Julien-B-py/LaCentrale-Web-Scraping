from math import ceil

import requests
from bs4 import BeautifulSoup

from config import headers


class LaCentrale:
    def __init__(self):
        self.current_page = 1
        self.url = f"https://www.lacentrale.fr/listing?energies=ess&gearbox=MANUAL&makesModelsCommercialNames=HONDA%3ACIVIC&options=&page={self.current_page}&sortBy=firstOnlineDateDesc"
        self.create_listings()
        self.sales_qty = self.get_number_of_sales()
        self.results_pages_qty = self.get_number_of_results_pages()
        self.collect_current_page_sales()

    def get_number_of_sales(self):
        page = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        sales = soup.find("span", {"class": "numAnn"})
        return int(sales.get_text())

    def get_number_of_results_pages(self):
        # Calcul du nombre de pages à scraper
        return ceil(int(self.sales_qty) / 16)

    def collect_current_page_sales(self):
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        modeles = soup.find_all("span", {"class": "searchCard__makeModel"})
        versions = soup.find_all("span", {"class": "searchCard__version"})
        prices = soup.find_all("div", {"class": "searchCard__fieldPrice"})
        kilometers = soup.find_all("div", {"class": "searchCard__mileage"})
        years = soup.find_all("div", {"class": "searchCard__year"})
        links = soup.find_all("a", {"class": "searchCard__link"})
        departments = soup.find_all("div", {"class": "searchCard__dptCont"})
        sellers = soup.find_all("div", {"class": "cbm-txt--default searchCard__customer"})
        good_deals = soup.find_all("span", {"class": "goodDeal-label"})

        self.add_to_lists(modeles, versions, prices)

    def create_listings(self):
        self.modeles = []
        self.versions = []
        self.prices = []
        self.kilometers = []
        self.years = []
        self.links = []
        self.departments = []
        self.sellers = []
        self.good_deals = []

    def add_to_lists(self):
        pass





if __name__ == '__main__':
    la_centrale = LaCentrale()
