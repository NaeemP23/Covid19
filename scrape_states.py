import zipfile, shutil, requests, io, os

# code for getting massachusetts data
mass_url = 'https://www.mass.gov/doc/covid-19-raw-data-may-18-2020/download'

r = requests.get(mass_url, stream =True)
check = zipfile.is_zipfile(io.BytesIO(r.content))
while not check:
    r = requests.get(mass_url, stream =True)
    check = zipfile.is_zipfile(io.BytesIO(r.content))
else:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path = 'massachusetts')

# the rest of this scrapes the data for indiana, tennessee, washington, and ohio
# the format is pretty simple and other states can easily be added

files = [
['indiana',
'https://hub.mph.in.gov/dataset/5a905d51-eb50-4a83-8f79-005239bd108b/resource/882a7426-886f-48cc-bbe0-a8d14e3012e4/download/covid_report_bedvent.xlsx',
'resources'],
['indiana','https://hub.mph.in.gov/dataset/ab9d97ab-84e3-4c19-97f8-af045ee51882/resource/182b6742-edac-442d-8eeb-62f96b17773e/download/covid_report_date.xlsx',
'cases'],
['tennessee',"https://www.tn.gov/content/dam/tn/health/documents/cedep/novel-coronavirus/datasets/Public-Dataset-Daily-Case-Info.XLSX",
'cases'],
['washington',  "https://www.doh.wa.gov/Portals/1/Documents/1600/coronavirus/data-tables/PUBLIC_CDC_Event_Date_SARS.xlsx?ver=20200528171614",
'cases'],
#['virginia', 'https://www.vdh.virginia.gov/content/uploads/sites/182/2020/05/VDH-COVID-19-PublicUseDataset-KeyMeasures-Hospitals.csv',
#'resources'],
#['virginia','https://www.vdh.virginia.gov/content/uploads/sites/182/2020/05/VDH-COVID-19-PublicUseDataset-Cases.csv',
#'cases'],
#['virginia','https://www.vdh.virginia.gov/content/uploads/sites/182/2020/05/VDH-COVID-19-PublicUseDataset-Outbreaks_by-Date.csv',
#'outbreaks']
['ohio','https://coronavirus.ohio.gov/static/COVIDSummaryData.csv',
'cases']]

for file in files:
	state = file[0]
	url = file[1]
	name = file[2]

	if not os.path.exists(state):
		os.mkdir(state)
	resp = requests.get(url)

	file_path = state + '/' + name + '.csv'

	output = open(file_path, 'wb')
	output.write(resp.content)
	output.close()