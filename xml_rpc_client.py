import xmlrpc.client

proxy = xmlrpc.client.ServerProxy('http://localhost:8000')

category = 'Furniture'

print(f"Vendas no Top 10 por categoria '{category}':")
sales_by_cat = proxy.get_sales_by_category(category)
# Ordena por vendas descendente
sorted_sales = sorted(sales_by_cat, key=lambda x: x['sales'], reverse=True)[:10]
if sorted_sales:
    category_total = sum(sale['sales'] for sale in sales_by_cat)
    print(f"Total na categoria: {category_total:.2f} (de {len(sales_by_cat)} itens)")
    print("\nTop 10 produtos (maiores vendas):")
    for i, sale in enumerate(sorted_sales, 1):
        print(f"{i}. {sale['product'][:50]}... : {sale['sales']:.2f}")
else:
    print("Nenhum item encontrado na categoria.")


total_sales = proxy.get_total_sales()
print(f"\nTotal de vendas geral no dataset: {total_sales:.2f}")
