import sqlite3
from datetime import datetime


conn = sqlite3.connect('../output/complaints.sqlite')
cur = conn.cursor()


def dates():
    cur.execute("SELECT min(date) FROM Dates")
    actual_smallest = cur.fetchone()[0]
    cur.execute("SELECT max(date) FROM Dates")
    actual_greatest = cur.fetchone()[0]

    as1 = datetime.strptime(actual_smallest, "%m/%d/%Y")
    ass1 = datetime.strftime(as1, "%b %d, %Y")
    smallest = input("\nWhat date do you want your graph to start?\nThe first date retrieved was {}.\nIf you press enter, it will start at the oldest possible date. \n\n".format(ass1))

    if len(smallest) == 0:
        smallest = actual_smallest
    else:
        try:
            trial = datetime.strptime(smallest, "%b %d, %Y")
            smallest = datetime.strftime(trial, "%m/%d/%Y")
        except:
            print("Invalid input. graph starting at oldest date.\n")
            smallest = actual_smallest



    ag1 = datetime.strptime(actual_greatest, "%m/%d/%Y")
    agg1 = datetime.strftime(ag1, "%b %d, %Y")
    greatest = input("What date do you want your graph to end?\nThe last date retrieved was {}.\nIf you press enter, it will end at the last date retrivied.\n\n".format(agg1))

    if len(greatest) == 0:
        greatest = actual_greatest
    else:
        try:
            trial = datetime.strptime(greatest, "%b %d, %Y")
            greatest = datetime.strftime(trial, "%m/%d/%Y")
        except:
            print("Invalid input. graph starting at newest date")
            greatest = actual_greatest

    if smallest < actual_smallest or smallest > actual_greatest or smallest > greatest:
        smallest = actual_smallest
        print("Invalid input graph starting at oldest date")
    if greatest < actual_smallest or greatest > actual_greatest or greatest < smallest:
        smallest = actual_smallest
        print("Invalid input graph starting at newest date")

    return smallest, greatest


def how_many():
    how_many = input("\nHow many of the top products with complaints do you want to see in the graph: ")
    try:
        if int(how_many) < 1:
            print("\nnot valid. we will get the 3 products with the most complaints")
            how_many = 3
        return int(how_many)
    except ValueError:
        print("\nnot valid input. we will get the 3 products with the most complaints")
        return 3


def get_counts(smallest, greatest):

    cur.execute("""SELECT Dates.date, Products.product
    FROM Dates JOIN Individual_Complaints JOIN Products
    ON Individual_Complaints.date_id = Dates.id AND Individual_Complaints.product_id = Products.id
    """)

    product_count = dict()
    dates = list()
    for row in cur:
        date = row[0]
        product = row[1]
        if date > greatest or date < smallest:
            continue

        if date not in dates:
            dates.append(date)
        product_count[product] = product_count.get(product, 0) + 1

    sorted_products = sorted(product_count, key=product_count.get, reverse=True)

    num = how_many()
    graph_products = sorted_products[:num]
    print("\n\nTop {} Products\n".format(num).upper())

    for x in graph_products:
        print(x, product_count[x], "\n")

    dates  = sorted(dates)

    cur.execute("""SELECT Dates.date, Products.product
    FROM Dates JOIN Individual_Complaints JOIN Products
    ON Individual_Complaints.date_id = Dates.id AND Individual_Complaints.product_id = Products.id
    """)

    p_d = dict()
    for row in cur:

        if date not in dates:
            continue
        if product not in product_count:
            continue
        product = row[1]
        date = row[0]
        p_d[(date, product)] = p_d.get((date, product), 0) + 1

    return graph_products, dates, p_d


smallest, greatest = dates()
graph_products, dates, p_d = get_counts(smallest, greatest)


with open ("gline.js", "w") as cj:
    cj.write("cj = [ ['Day'")
    for product in graph_products:
        cj.write("'"+product+"',")
    cj.write("],\n")
    for date in dates:
        cj.write("['"+date+"',")
        for product in graph_products:
            num = p_d.get((date, product), 0)
            cj.write("'"+str(num)+"',")
        cj.write("],\n")
