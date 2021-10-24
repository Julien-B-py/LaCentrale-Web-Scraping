# LaCentrale-Web-Scraping

Extract most recent sales data from **La Centrale** website. 
 
You can specify the car brand, model, fuel type, gearbox type and how many results pages you want to extract the data from.

If nothing is specified the most recent sales will be extracted.

## Requirements

`pip install requests` (for GET requests)  
`pip install beautifulsoup4` (for pulling data out of HTML) 


## Usage

```python
import pandas as pd
from lacentrale import LaCentrale

la_centrale = LaCentrale(brand="Porsche")
sales = la_centrale.collect_multiple_pages_sales(pages=2)
# Turn data to a dataframe and export as csv file
df = pd.DataFrame.from_dict(sales, orient="index")
df.to_csv("results.csv")
```




