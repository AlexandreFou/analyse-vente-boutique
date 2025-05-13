import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'retail_sales_dataset.csv'
sales_df = pd.read_csv(file_path)

conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

sales_df.columns = sales_df.columns.str.replace(' ','_').str.lower()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
               transaction_id INTEGER PRIMARY KEY,
               date TEXT,
               customer_id TEXT,
               gender TEXT,
               age INTEGER,
               product_category TEXT,
               quantity INTEGER,
               price_per_unit INTEGER,
               total_amount INTEGER
               );
''')

sales_df.to_sql('sales', conn, if_exists='replace', index=False )

cursor.execute('PRAGMA table_info(sales);')
for column in cursor.fetchall() :
    print(column)

#requête 1:
print("\n ventes totales par catégories :")
cursor.execute('''
    SELECT product_category, SUM(total_amount) AS total_sales 
    FROM sales
    GROUP BY product_category
    ORDER BY total_sales DESC;
               ''')

for row in cursor.fetchall() :
    print(row)

#requête 2:
print("\n ventes moyennes par catégores :")
cursor.execute('''
    SELECT product_category, ROUND(AVG(total_amount), 2) AS average_amount
    FROM sales
    GROUP BY product_category
    ORDER BY average_amount DESC;
    ''')
for row in cursor.fetchall() :
    print(row)

#requête 3:
print("\n nombre de transactions par catégories :")
cursor.execute('''
    SELECT product_category, COUNT(transaction_id) AS number_of_transactions
    FROM sales
    GROUP BY product_category
    ORDER BY number_of_transactions DESC;
    ''')
for row in cursor.fetchall() :
    print(row)


conn.close()

#analyse exploratoire :
sns.set(style ="whitegrid")

#requête1 : ventes totales par catégories

plt.figure(figsize=(10,6))
sales_by_category = sales_df.groupby("product_category")["total_amount"].sum()
sales_by_category.plot(kind="bar", color="skyblue")
plt.title("Ventes totales par catégories de produit")
plt.xlabel("catégories de produit")
plt.ylabel("ventes totales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#requête2 : analyse des ventes par tranches d'age

plt.figure(figsize=(10,6))
age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
age_labels = ['0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '60+']
sales_df['group_age'] = pd.cut(sales_df['age'], bins=age_bins, labels=age_labels)
sales_by_group_age = sales_df.groupby("group_age")["total_amount"].sum()
sales_by_group_age.plot(kind='bar',color='lightgreen')
plt.title("Chiffres de vente par groupes d'âge")
plt.xlabel("groupes d'âge")
plt.ylabel("Chiffres de ventes")
plt.tight_layout()
plt.show()

#requête 3 : répartition des ventes par sexe

plt.figure(figsize=(10,6))
sales_by_gender = sales_df.groupby("gender")["total_amount"].sum()
sales_by_gender.plot(kind='pie', autopct='%1.1f%%', colors=['lightcoral','lightskyblue'])
plt.title("Répartition des ventes par genre")
plt.ylabel("")
plt.show()

#requête 4 : les catégories de produits les plus vendus

plt.figure(figsize=(10,6))
most_sold_products = sales_df.groupby("product_category")["quantity"].sum()
most_sold_products.plot(kind='bar', color='orange')
plt.title("Nombre de produits vendus par catégories")
plt.xlabel("catégories de produit")
plt.ylabel("nombres de produits vendus")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()





