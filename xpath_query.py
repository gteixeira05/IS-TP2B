from lxml import etree
from collections import Counter

tree = etree.parse("Retail-Supply-Chain-Sales-Dataset_NOVO.xml")
root = tree.getroot()

# Produtos em Office Supplies (primeiros 10)
products = root.xpath("//Row[Category='Office Supplies']/ProductName/text()")
print("\n=== Produtos em Office Supplies (Top 10) ===")
for i, prod in enumerate(products[:10], 1):
    print(f"{i}. {prod}")

# Produtos de Office Supplies com Sales > 1000
high_sales = root.xpath("//Row[Category='Office Supplies' and number(Sales) > 1000]/ProductName/text()")
print("\n=== Produtos em Office Supplies com Sales > 1000 ===")
for i, prod in enumerate(high_sales[:10], 1):
    print(f"{i}. {prod}")

# Contagem por categoria
categories = root.xpath("//Row/Category/text()")
cat_counter = Counter(categories)
print("\n=== Contagem de registos por categoria ===")
for cat, count in cat_counter.items():
    print(f"{cat}: {count}")

# Total de vendas de Furniture
furniture_sales = root.xpath("//Row[Category='Furniture']/Sales/text()")
total_furniture = sum(float(val) for val in furniture_sales)
print("\n=== Total de vendas de Furniture ===")
print(f"{total_furniture:,.2f}€")
