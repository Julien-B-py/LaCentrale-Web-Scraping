from math import ceil
import pandas as pd
import random
import time

from bs4 import BeautifulSoup
import requests

from config import headers


class LaCentrale:
    def __init__(self):
        self.current_page = 1
        self.current_sale = 0
        self.sales = {}
        self.url = f"https://www.lacentrale.fr/listing?energies=ess&gearbox=MANUAL&makesModelsCommercialNames=HONDA%3ACIVIC&options=&page={self.current_page}&sortBy=firstOnlineDateDesc"
        self.sales_qty = self.get_number_of_sales()
        self.results_pages_qty = self.get_number_of_results_pages()

    def get_number_of_sales(self) -> int:
        """
        Returns an integer representing the total numbers of sales found for the requested car.
        """
        page = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        sales_count = soup.find("span", {"class": "numAnn"})
        return int(sales_count.get_text())

    def get_number_of_results_pages(self):
        """
        Returns an integer representing the total numbers of search results pages for the requested car.
        """
        # For each page 16 sales are listed
        # To get the total number of pages we just need to divide the total sales per 16
        return ceil(int(self.sales_qty) / 16)

    def collect_current_page_sales(self):
        """
        Returns a dict containing all the sales listed on the current page including all specific information
        (eg: Model, Price, Year, Mileage, etc)
        """
        print(f"Collecting data from search results page #{self.current_page}.")

        response = requests.get(self.url, headers=headers)
        print(response.status_code)
        soup = BeautifulSoup(response.content, "html.parser")

        models = soup.find_all("span", {"class": "searchCard__makeModel"})
        versions = soup.find_all("span", {"class": "searchCard__version"})
        prices = soup.find_all("div", {"class": "searchCard__fieldPrice"})
        kilometers = soup.find_all("div", {"class": "searchCard__mileage"})
        years = soup.find_all("div", {"class": "searchCard__year"})
        links = soup.find_all("a", {"class": "searchCard__link"})
        departments = soup.find_all("div", {"class": "searchCard__dptCont"})
        sellers = soup.find_all("div", {"class": "cbm-txt--default searchCard__customer"})
        good_deals = soup.find_all("span", {"class": "goodDeal-label"})



        print(models)


        # Loop through all the lists at the same time
        for (model, version, price, kilometer, year,
             link, department, seller, good_deal) in zip(models, versions, prices, kilometers, years, links,
                                                         departments, sellers, good_deals):
            # Increment sale index for every loop run
            self.current_sale += 1
            print(self.current_sale)

            # Cleaning some unwanted characters from prices and mileages strings and cast as integer
            formatted_price = int(price.get_text().replace(u"\xa0", u"").replace("€", ""))
            formatted_kilometer = int(kilometer.get_text().replace(u"\xa0", u"").replace("km", ""))

            # Create a new entry in the dict with the current_sale id as the key and another dict containing all the
            # information as the value
            self.sales[self.current_sale] = {"Model": model.get_text(),
                                             "Version": version.get_text(),
                                             "Price": formatted_price,
                                             "Mileage": formatted_kilometer,
                                             "Year": int(year.get_text()),
                                             "URL": f"https://www.lacentrale.fr{link.get('href')}",
                                             "Location": department.get_text(),
                                             "Seller": seller.get_text(),
                                             "Good deal?": good_deal.get_text(),
                                             }

        print(self.sales)
        return self.sales

    def collect_multiple_pages_sales(self, pages: int = 3):
        """
        Returns a dict containing all the sales information (eg: Model, Price, Year, Mileage, etc) from the requested
        number of results pages.
        """
        while True:

            self.collect_current_page_sales()

            # If we scraped the requested number of pages we stop the process
            # or if the current page is equal to the number of results pages
            # We stop the process
            if self.current_page in [pages, self.results_pages_qty]:
                break

            # Pause to avoid spamming requests.
            pause_time = random.uniform(5, 15)
            print(f"Taking a break for {round(pause_time)} seconds before requesting next page.")
            time.sleep(pause_time)
            # Update the dynamic url for the next request
            self.current_page += 1
            self.update_url()

        return self.sales

    def update_url(self):
        """
        Update the url to the current requested results page.
        """
        self.url = f"https://www.lacentrale.fr/listing?energies=ess&gearbox=MANUAL&makesModelsCommercialNames=HONDA%3ACIVIC&options=&page={self.current_page}&sortBy=firstOnlineDateDesc"

        print(self.url)


if __name__ == "__main__":
    la_centrale = LaCentrale()
    sales = la_centrale.collect_multiple_pages_sales(pages=3)
    # Turn data to a dataframe and export as csv file
    df = pd.DataFrame.from_dict(sales, orient="index")
    df.to_csv("results.csv")
