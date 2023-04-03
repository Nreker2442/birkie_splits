import streamlit
import pandas as pd
import requests
from urllib.error import URLError
import PyPDF2
import pandas as pd
import numpy as np

streamlit.title('Birkie Split Finder')
streamlit.header('Find Your Splits')

# creating a pdf file object
reader = PyPDF2.PdfReader("C:\ResultListsOverallResults.pdf")
# print the text of the first page
print(reader.pages[0].extract_text())
#create dataframe of first page of pdf data
page = reader.pages[0].extract_text()
#split the list by \n first
cutlist = page.split('\n')
cutlist.remove('Birkie Skate')
table1 = pd.DataFrame(cutlist)
table2 =table1[0].str.split(",", n=1, expand=True)
t3 = table2[0].str.split('', n=1, expand=True)
t4 = t3[1].str.split(' ')
bibnum = pd.DataFrame(t4)

#seperate values in bibnum table into a column of their own
bib = bibnum[1].apply(pd.Series)

#name columns
bib.columns = ['OvrSexDiv', 'AgeGrp', 'BibNum', 'LName', 4]

#clean up first 6 rows
topsix = bib.head(7)
topsix["AgeGrp"] = ['M', 'M', 'M', 'M', 'M', 'M', 'M']
topsix["BibNum"] = ["BibName",'2','1','10','7','6','219']
topsix["LName"] = ['City', 'Norris', 'Agnellet', 'Izquierdo-Bernier', "O'Harra", 'Kornfield', 'Winker']

#merge dataframes back together
frames = [bib, topsix]
results = pd.concat(frames)

#remove dups from concat 
result_df = results.drop_duplicates()

#remove rows with insignificant data
results_clean = result_df.drop(0)
results_clean = results_clean.drop(47)
results_clean = results_clean.drop(46)

#drop extra column
final_results = results_clean.drop(4, axis=1)

#extract finish sector time from the race result url
import urllib.request
import json
import pandas as pd
import requests

#import json from URL and flatten the nested list of splits
def lake_times(bibnum):
        siteExtension = bibnum
        url = ("https://my1.raceresult.com/225100/RRPublish/data/splits?key=101f5d19227d60172fb1415b9dda0769&bib=%s" %(siteExtension))
        response = requests.get(url)
        with urllib.request.urlopen(response.url) as link:
            data = json.loads(link.read().decode())
            df_nested_list = pd.json_normalize(data, record_path =['Splits'])
            lake_time = df_nested_list.loc[5, 'Sector']
            df = print(bibnum, ',', lake_time)
            df
     
lake_times(2)

try:
  bib_num = streamlit.text_input('What bib number are you looking for?')
  if not bib_num:
    streamlit.error("Please try again")
  else:
    back_from_function = lake_times(bib_num)
    streamlit.dataframe(back_from_function)
except URLError as e:
  sreamlit.error()
  
streamlit.write('The user entered', bib_num)




