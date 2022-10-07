from msilib.schema import CompLocator
import re
import csv
import sqlite3
from venv import create

conn = sqlite3.connect('uk-energy.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Energy_Type;
DROP TABLE IF EXISTS Energy_Quarter;
DROP TABLE IF EXISTS Years;
DROP TABLE IF EXISTS Amount;

CREATE TABLE Energy_Type (
    type_id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title VARCHAR(128)
);

CREATE TABLE Energy_Quarter (
    quarter_id INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    quarter VARCHAR(128)
);

CREATE TABLE Years (
    title_id INTEGER,
    year INTEGER,
    amount INTEGER
);

CREATE TABLE Amount (
    amount_id INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title_id INTEGER,
    quarter_id INTEGER,
    amount INTEGER,
    FOREIGN KEY(title_id) REFERENCES Energy_Type(type_id),
    FOREIGN KEY(quarter_id) REFERENCES Energy_Quarter(quarter_id)
)
''')

def clean_back_list():
    dir = 'Programs/uk_energy/data/renewables_breakdown.csv'
    column = list();
    elec_generated = 'ELECTRICITY GENERATED (GWh)'
    with open(dir, newline='') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            row = row[:-3]
            column.append(row)
            if elec_generated in row[0]:
                elec_generated_position = i
    ### so I'm slicing the list to remove any items before the elec_generated position.
    cleaned_list = column[elec_generated_position: ]

    return cleaned_list;

def clean_front_list(cleaned_list):
    empty_list_index = 0
    for i, l in enumerate(cleaned_list):
        if l[0] == '':
            empty_list_index = i
            break;
    completely_cleaned_list = cleaned_list[: empty_list_index]

    return completely_cleaned_list

def create_years(completely_cleaned_list):
    years_list = [];
    for i, item in enumerate(completely_cleaned_list[0]):
        if i > 0:
            item = item[:4]
            years_list.append(item)

    single_years_list = list(dict.fromkeys(years_list)) 

    return single_years_list;

def create_yearly_amounts(amount_data):
    abc_list = []
    for list in amount_data:
        abc = chunks(list, 4)
        abc_list.append(abc)
        print(abc_list)
            

def chunks(xs, n):
    n = max(1, n)
    return (xs[i:i+n] for i in range(0, len(xs), n))



def clean_title(cleaned_data):
    title_list = list()
    for i, row in enumerate(cleaned_data):
        if i > 0 : 
            strValue = row[0].split('[', 1)[0]
            strValue = strValue.rstrip()
            strValue = re.sub('[ ]', '_', strValue)
            title_list.append(strValue)

    return title_list

def store_title(titles):
    for title in titles:
        cur.execute('INSERT OR IGNORE INTO Energy_Type (title) VALUES ( ? )', ( title, ) )
        conn.commit()

def clean_quarter(data):
    quarter_list = list()
    for i, row in enumerate(data[0]):
        if ' ' not in row[4]:
            row = row[:4] + " " + row[4:]
        if i > 0 : 
            row = re.sub('\n', '', row)
            quarter_list.append(row)

    return quarter_list

def store_quarter(quarter_data):
    for quarter in quarter_data:
        cur.execute('INSERT OR IGNORE INTO Energy_Quarter (quarter) VALUES ( ? )', ( quarter, ) )
        conn.commit()

def clean_amount(data):
    cleaned_data = []
    for i, list in enumerate(data):
        list.pop(0)
        if i > 0:
            cleaned_data.append(list)

    return cleaned_data

def create_quarter_amount_dict(amount_data):
    cur.execute('SELECT * FROM Energy_Quarter')
    energy_quarter_data = cur.fetchall()
    quarter_list = [quarter[0] for quarter in energy_quarter_data]

    quarter_amount_list = [];
    for list in amount_data:
        quarter_amount_dict = {key:value for (key, value) in zip(quarter_list, list)}
        quarter_amount_list.append(quarter_amount_dict)

    return quarter_amount_list

def store_amounts(quarter_amount_list):
    cur.execute('SELECT * FROM Energy_Type')
    energy_title_data = cur.fetchall()
    type_ids = [title[0] for title in energy_title_data]

    for dict, type_id in zip(quarter_amount_list, type_ids):
        for quarter, amount in dict.items() :
            print(type_id, quarter, amount)
            cur.execute('INSERT OR IGNORE INTO Amount (title_id, quarter_id, amount) VALUES ( ?, ?, ?)', ( type_id, quarter, amount ) )
            conn.commit()


def retrieve_db_test():
    cur.execute('SELECT * FROM Energy_Type')
    row = cur.fetchall()
    print(row)
    cur.execute('SELECT * FROM Energy_Quarter')
    row = cur.fetchall()
    print(row)


def main():
    cleaned_list = clean_back_list()
    completely_cleaned = clean_front_list(cleaned_list)
    years = create_years(completely_cleaned)
    amount = clean_amount(completely_cleaned)
    yearly_amounts = create_yearly_amounts(amount)

    # energy_titles = clean_title(completely_cleaned)
    # store_title(energy_titles)
    # quarter_titles = clean_quarter(completely_cleaned)
    # store_quarter(quarter_titles)
    # quarter_list_dicts = create_quarter_amount_dict(amount)
    # store_amounts(quarter_list_dicts)
    # retrieve_db_test()

if __name__ == "__main__":
    main()
