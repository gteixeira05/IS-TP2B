import grpc
import sales_pb2
import sales_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = sales_pb2_grpc.SalesServiceStub(channel)

category = 'Office Supplies'

print(f"Vendas por categoria '{category}':")
request = sales_pb2.SalesRequest(category=category)
response = stub.GetSalesByCategory(request)
if response.products:
    print(f"Total na categoria: {response.category_total:.2f} (de {response.num_items} itens)")
    sorted_products = sorted(response.products, key=lambda x: x.sales_amount, reverse=True)[:10]
    print("\nTop 10 produtos (maiores vendas):")
    for i, prod in enumerate(sorted_products, 1):
        print(f"{i}. {prod.product_name[:50]}... : {prod.sales_amount:.2f}")
else:
    print("Nenhum item encontrado.")

print("\nTotal de vendas geral no dataset:")
total_resp = stub.GetTotalSales(sales_pb2.EmptyRequest())  # Usa custom EmptyRequest
print(f"{total_resp.total:.2f} (de {total_resp.num_records} registos)")
