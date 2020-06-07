import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# https://coronavirus.dc.gov/page/hospital-status-data

page = requests.get('https://coronavirus.dc.gov/page/hospital-status-data')
# print(page)

soup = BeautifulSoup(page.content, 'html.parser')
data = soup.find('div', class_ = 'field-items')
dates = []
total_icu_beds, avail_icu_beds, total_vent, inuse_vent, avail_vent, total_covid_patients, total_patients, percent_pre_bed = [], [], [], [], [], [], [], []
for d in data:
    for line in d.text.split("\n\n\n"):
        content = line.split("\n\n")
        date = content[0]
        dates.append(date)
        attributes = content[1].split("\n")
        i = 0
        for attribute in attributes: 
            num = re.sub(r'\D+', '', attribute)
            if i == 0: total_icu_beds.append(num)
            elif i == 1: avail_icu_beds.append(num)
            elif i == 2: total_vent.append(num)
            elif i == 3: inuse_vent.append(num)
            elif i == 4: avail_vent.append(num)
            elif i == 5: total_covid_patients.append(num)
            elif i == 6: total_patients.append(num)
            else: percent_pre_bed.append(num)
            i += 1
        if i <= 5:
            total_covid_patients.append('NR')
            total_patients.append('NR')
            percent_pre_bed.append('NR')

results = {'Date': dates, 
           'Total ICU Beds in Hospitals:': total_icu_beds,
           'ICU Beds Available:': avail_icu_beds,
           'Total Reported Ventilators in Hospitals:': total_vent,
           'In-Use Ventilators in Hospitals': inuse_vent,
           'Available Ventilators in Hospitals': avail_vent,
           'Total COVID-19 Patients in DC Hospitals:': total_covid_patients,
           'Total Patients in DC Hospitals (COVID and non-COVID)': total_patients,
           'Percentage of pre-COVID Hospital Bed Capacity:': percent_pre_bed}

df = pd.DataFrame.from_dict(results, orient = 'index')
df.to_csv('dc_data.csv', index = False)