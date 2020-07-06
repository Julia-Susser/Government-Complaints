import csv
import sqlite3

conn = sqlite3.connect('../output/complaints.sqlite')
cur = conn.cursor()
cur.executescript("""
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Company;
DROP TABLE IF EXISTS Companys;
DROP TABLE IF EXISTS States;
DROP TABLE IF EXISTS Submitted_Via;
DROP TABLE IF EXISTS Individual_Complaints;
DROP TABLE IF EXISTS Dates;
DROP TABLE IF EXISTS Issues;

CREATE TABLE  Products(
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    product TEXT UNIQUE
);

CREATE TABLE  Companys(
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    company    TEXT UNIQUE
);

CREATE TABLE  States(
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    state   TEXT UNIQUE
);

CREATE TABLE  Dates(
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    date    TEXT UNIQUE
);

CREATE TABLE  Issues(
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    issue    TEXT UNIQUE
);

CREATE TABLE  Submitted_Via(
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    submitted_via    TEXT UNIQUE
);

CREATE TABLE  Individual_Complaints(
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    date_id INTEGER,
    issue_id INTEGER,
    product_id  INTEGER,
    company_id  INTEGER,
    state_id  INTEGER,
    zip_code INTEGER,
    submitted_id  INTEGER,
    complaint_id INTEGER

)

""")
def parsed_data(x):

    date = x[date_h].strip("\n")
    if len(date) < 1:
        date = None

    product = x[product_h].strip("\n")
    if len(product) < 1:
        product = None

    issue = x[issue_h].strip("\n")
    if len(issue) < 1:
        issue = None

    company = x[company_h].strip("\n")
    if len(company) < 1:
        company = None

    state = x[state_h].strip("\n")
    if len(state) < 1:
        state = None

    zip_code = x[zip_code_h].strip("\n")
    if len(zip_code) < 1:
        zip_code = None

    submitted_via = x[submitted_via_h].strip("\n")
    if len(submitted_via) < 1:
        submitted_via = None

    complaint_id = x[complaint_id_h].strip("\n")
    if len(complaint_id) < 1:
        complaint_id = None
    return (date, product, issue, company, state, zip_code, submitted_via, complaint_id)




with open("../input/Consumer_Complaints.csv", "r") as complaints:
    dict_c = csv.DictReader(open("../input/Consumer_Complaints.csv"), delimiter=",")
    count = 0
    headers =  dict_c.fieldnames
    date_h = headers[0]
    product_h = headers[1]
    issue_h = headers[3]

    company_h = headers[7]
    state_h = headers[8]
    zip_code_h = headers[9]
    submitted_via_h = headers[12]
    complaint_id_h = headers[-1]

    def how_many():
        lines = complaints.readlines()
        print("The limit is {}".format(len(lines)))
        how_many = input("\nHow many complaints do you want to read: ")
        try:
            if int(how_many) < 1:
                print("not valid. we will extract 5 rows")
                how_many = 5
            return int(how_many)
        except ValueError:
            print("not valid input. we will extract 5 rows")
            return 5



    how_many = how_many()
    count = 0
    print("retrieving {} rows".format(str(how_many)))
    for x in dict_c:
        conn.commit()

        complaint = parsed_data(x)

        if count == how_many:
            break
        count += 1
        print("\n\nnew complaint ".upper() + str(count) + "\n")

        date, product, issue, company, state, zip_code, submitted_via, complaint_id = complaint
        company = company.lower()
        print("date:", date)
        print("product:", product)
        print("issue:", issue)
        print("company:", company)
        print("state:", state)
        print("zip code:", zip_code)
        print("submitted via:", submitted_via)
        print("complaint id:", complaint_id)

        cur.execute('''INSERT OR IGNORE INTO Products (product)
            VALUES ( ? )''', ( product, ))
        cur.execute('SELECT id FROM Products WHERE product = ? ', (product, ))
        try:
            product_id = cur.fetchone()[0]
        except:
            "Could not fetch id!"
            continue

        cur.execute('''INSERT OR IGNORE INTO Companys (company)
            VALUES ( ? )''', ( company, ))
        cur.execute('SELECT id FROM Companys WHERE company = ? ', (company, ))
        try:
            company_id = cur.fetchone()[0]
        except:
            "Could not fetch id!"


        cur.execute('''INSERT OR IGNORE INTO States (state)
            VALUES ( ? )''', ( state, ))
        cur.execute('SELECT id FROM States WHERE state = ? ', (state, ))
        try:
            hey = cur.fetchone()
            state_id = hey[0]
        except:
            "Could not fetch id!"


        cur.execute('''INSERT OR IGNORE INTO Submitted_Via (submitted_via)
            VALUES ( ? )''', ( submitted_via, ))
        cur.execute('SELECT id FROM Submitted_Via WHERE submitted_via = ? ', (submitted_via, ))
        try:
            submitted_id = cur.fetchone()[0]
        except:
            "Could not fetch id!"


        cur.execute('''INSERT OR IGNORE INTO Dates (date)
            VALUES ( ? )''', ( date, ))
        cur.execute('SELECT id FROM Dates WHERE date = ? ', (date, ))
        try:
            date_id = cur.fetchone()[0]
        except:
            "Could not fetch id!"

        cur.execute('''INSERT OR IGNORE INTO Issues (issue)
            VALUES ( ? )''', ( issue, ))
        cur.execute('SELECT id FROM Issues WHERE issue = ? ', (issue, ))
        try:
            issue_id = cur.fetchone()[0]
        except:
            "Could not fetch id!"

        cur.execute('''INSERT OR IGNORE INTO Individual_Complaints(date_id, product_id, issue_id, company_id, state_id, zip_code, submitted_id, complaint_id)
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ? )''', (date_id, product_id, issue_id, company_id, state_id, zip_code, submitted_id, complaint_id))


        print("\n\n\n")
