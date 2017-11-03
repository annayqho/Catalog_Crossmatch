""" I think you have to do this instead of using the api search """

import requests

#www = "https://wis-tns.weizmann.ac.il/search?&amp;page=0&amp;isTNS_AT=yes&amp;classified_sne=1&amp;num_page=1000&amp;format=csv"

payload = {'page': '0', 'isTNS_AT': 'yes', 'classified_sne': '1', 'num_page': '1000', 'format': 'csv'}

www = 'https://wis-tns.weizmann.ac.il/search'

r = requests.get(www, params=payload)
print(r.url)
    
