import sqlite3

conn = sqlite3.connect('../output/complaints.sqlite')
cur = conn.cursor()
cur.execute("""SELECT Products.product FROM Products JOIN Individual_Complaints
ON Products.id = Individual_Complaints.product_id""")

def how_many():
    how_many = input("\nHow many products do you want to see with the most complaints: ")
    try:
        if int(how_many) < 1:
            print("\nnot valid. we will get the 3 products with the most complaints")
            how_many = 3
        return int(how_many)
    except ValueError:
        print("\nnot valid input. we will get the 3 products with the most complaints")
        return 3
count = 0
product_count = {}
for row in cur:
    count += 1
    product = row[0]
    if product == None:
        continue
    product_count[product] = product_count.get(product, 0) + 1

print("Loaded {} complaints".format(count))
sorted_products = sorted(product_count, key=product_count.get, reverse=True)
num = how_many()
print("\nTop {} Products\n\n".format(num).upper())
for x in sorted_products[:num]:
    print(x, product_count[x], "\n")
