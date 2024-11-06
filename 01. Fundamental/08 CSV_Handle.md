## Basic CSV
```py
import csv

data = ['data 1', 'data 2', 'data 3']

with open("data.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    for item in data:
        writer.writerow([item])

print("CSV file created successfully.")
```
## Dict Writer
```py
import csv

# CSV Header
header = ['company_name', 'position', 'location']

# Data
company_name = ['Tesla', 'Unilever', 'Akij']
position = ['Python Programmer', 'Driver', 'Engineer']
location = ['USA', 'Dhaka', 'Khulna']

# Initialize an empty list to hold the dictionaries
dicts_list = []

i = 0 
while i < len(company_name):
    # Create a new dictionary for each iteration
    dicts = {}
    dicts['company_name'] = company_name[i]
    dicts['position'] = position[i]  # Fixed the spelling
    dicts['location'] = location[i]
    
    # Append the dictionary to the list
    dicts_list.append(dicts)

    # Print statements (optional)
    print(i)
    print(dicts)
    print(dicts_list)

    i += 1

# List to CSV - Write the data after the loop completes
with open('test.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()  # Write CSV Header
    writer.writerows(dicts_list)  # Write CSV Rows

```
## List Writer
```py
import csv
# field names
fields = ['Name', 'Branch', 'Year', 'CGPA']
# data rows of csv file
rows = [ ['Nikhil', 'COE', '2', '9.0'],
		['Sanchit', 'COE', '2', '9.1'],
		['Aditya', 'IT', '2', '9.3'],
		['Sagar', 'SE', '1', '9.5'],
		['Prateek', 'MCE', '3', '7.8'],
		['Sahil', 'EP', '2', '9.1']
       ]
with open('test.csv', 'w', newline='', encoding='utf-8') as file:
	# using csv.writer method from CSV package
	write = csv.writer(file)
	
	write.writerow(fields)
	write.writerows(rows)

# Data Writing example
import csv
datas = [
	['Samrat', '003', 'Boikali'],
	['Fahim', '013', 'Doulatpur'],
]

write_list = []
while start_page < targeted_page:
    datas = []
    for single_data in datas:
	data_list = [single_data[0], single_data[1], single_data[2]]
	write_list.append(data_list)
	header = ['Name','ID','Address']
	with open('test.csv', 'w', newline='', encoding='utf-8') as file:
		write = csv.writer(file)
		write.writerow(header)
		write.writerows(write_list)
```
## Read CSV
```py
import csv

#Start CSV File reading
with open('product.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    dicts = {}
    i = 0
    for list in csv_reader:
        dicts[i] = {
            'keyword':list[0],
            'p1-lnk':list[1],
            'p1-fe':list[2],
            'info-1': list[21],
            'info-2': list[22],
            'buy-1': list[26],
            'buy-2': list[27]
        }
        i = i + 1
csv_file.close()
#End CSV File reading


post_run = 1
while post_run < len(dicts):
  #Link, Image, Title, Info, buying
  p1lnk = dicts[post_run]['p1-lnk']
  p1fe = dicts[post_run]['p1-fe']
  info1 = dicts[post_run]['info-1']
  info2 = dicts[post_run]['info-2']
  buy1 = dicts[post_run]['buy-1']
  buy2 = dicts[post_run]['buy-2']
  
  print(p1lnk)
  print(p1fe)
  print(info1)
  print(info2)
  print(buy1)
  print(buy2)

  post_run += 1
```
## read_csv_excel_with_pandas_for_any_language
```py
import chardet
import pandas as pd

def detect_encoding(file_name):
    with open(file_name, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

def csv_to_dict(file_name):
    encoding = detect_encoding(file_name)
    df = pd.read_csv(file_name, encoding=encoding)
    # df = pd.read_excel(file_name, encoding=encoding)
    data_dict = df.to_dict(orient='records')
    return data_dict

file_name = '/content/datasv.csv'
data_dict = csv_to_dict(file_name)

# Accessing data using column names (CSV headers)
for row in data_dict[:5]:
    print(row['Filo'])
```
## read_excel_with_pandas
```py
import pandas as pd
read = pd.read_excel('/content/drive/MyDrive/Rodrigue/Data-city.xlsx')
dicts = read.to_dict()

post_run = 0
i = 0
dicts_list = []
while i < len(dicts['city']):
    city = dicts['city'][post_run]
    Code_postal = dicts['Code_postal'][post_run]

    print(city)
    print(Code_postal)

    post_run += 1
    i += 1
```
