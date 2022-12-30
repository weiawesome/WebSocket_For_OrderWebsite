import json

import pandas as pd
b=pd.read_csv('b.csv')
a=pd.read_csv('a.csv')
print(a)
a=a.loc[a['CustomerId']!=1]
b=b.loc[b['CustomerId']!=1]
print()
print(a)
print(b)