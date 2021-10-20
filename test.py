import pandas as pd

data = {'1': {
    'modele':'test',
    'year':2020,
    'seller':'pro'
}, '2': {
    'modele':'audi',
    'year':2018,
    'seller':'pro'
}}

test = pd.DataFrame.from_dict(data, orient='index')

print(test)