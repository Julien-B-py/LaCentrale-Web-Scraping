from math import ceil
import random

import pandas as pd
import requests
import time

from bs4 import BeautifulSoup

from config import headers


class LaCentrale:
    def __init__(self):
        self.current_page = 0
        self.current_sale = 0
        self.sales = {}
        self.url = f"https://www.lacentrale.fr/listing?energies=ess&gearbox=MANUAL&makesModelsCommercialNames=HONDA%3ACIVIC&options=&page={self.current_page}&sortBy=firstOnlineDateDesc"
        self.sales_qty = self.get_number_of_sales()
        self.results_pages_qty = self.get_number_of_results_pages()

    def get_number_of_sales(self):
        page = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        sales = soup.find("span", {"class": "numAnn"})
        return int(sales.get_text())

    def get_number_of_results_pages(self):
        # Calcul du nombre de pages à scraper
        return ceil(int(self.sales_qty) / 16)

    def collect_current_page_sales(self):
        self.current_page += 1

        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        models = soup.find_all("span", {"class": "searchCard__makeModel"})
        versions = soup.find_all("span", {"class": "searchCard__version"})
        prices = soup.find_all("div", {"class": "searchCard__fieldPrice"})
        kilometers = soup.find_all("div", {"class": "searchCard__mileage"})
        years = soup.find_all("div", {"class": "searchCard__year"})
        links = soup.find_all("a", {"class": "searchCard__link"})
        departments = soup.find_all("div", {"class": "searchCard__dptCont"})
        sellers = soup.find_all("div", {"class": "cbm-txt--default searchCard__customer"})
        good_deals = soup.find_all("span", {"class": "goodDeal-label"})

        for (model, version, price, kilometer, year,
             link, department, seller, good_deal) in zip(models, versions, prices, kilometers, years, links,
                                                         departments, sellers, good_deals):
            # Increment sale index for every loop run
            self.current_sale += 1

            formatted_price = price.get_text().replace(u'\xa0', u'').replace('€', '')
            formatted_kilometer = kilometer.get_text().replace(u'\xa0', u'').replace('km', '')

            self.sales[self.current_sale] = {'Model': model.get_text(),
                                             'Version': version.get_text(),
                                             'Price': formatted_price,
                                             'Kilometers': formatted_kilometer,
                                             'Year': year.get_text(),
                                             'URL': f"https://www.lacentrale.fr{link.get('href')}",
                                             'Location': department.get_text(),
                                             'Seller': seller.get_text(),
                                             'Good deal?': good_deal.get_text(),
                                             }

        return self.sales

    def collect_multiple_pages_sales(self, pages=3):

        for _ in range(self.current_page, self.results_pages_qty + 1):
            self.collect_current_page_sales()

            if self.current_page == pages:
                break

            pause_time = random.uniform(5, 15)
            time.sleep(pause_time)

        return self.sales


if __name__ == '__main__':
    la_centrale = LaCentrale()
    sales = la_centrale.collect_current_page_sales()

    test = pd.DataFrame.from_dict(sales, orient='index')

    print(test.describe())
    print(test.head())
    print(test.tail())
