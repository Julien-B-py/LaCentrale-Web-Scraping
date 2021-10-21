import pandas as pd

from lacentrale import LaCentrale

if __name__ == "__main__":
    la_centrale = LaCentrale(brand="Porsche")
    sales = la_centrale.collect_multiple_pages_sales(pages=2)
    # Turn data to a dataframe and export as csv file
    df = pd.DataFrame.from_dict(sales, orient="index")
    df.to_csv("results.csv")