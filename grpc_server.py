import grpc
from concurrent import futures
import sales_pb2
import sales_pb2_grpc
import xml.etree.ElementTree as ET
from pathlib import Path

class SalesDataService:
    def __init__(self, xml_file):
        xml_path = Path(xml_file).resolve()
        if not xml_path.exists():
            raise FileNotFoundError(f"XML não encontrado: {xml_path}")
        self.tree = ET.parse(str(xml_path))
        self.root = self.tree.getroot()

    def parse_sales_value(self, sales_elem):
        if sales_elem is None:
            return 0.0
        text = sales_elem.text.strip() if sales_elem.text else '0'
        text_clean = text.replace(',', '').replace('$', '')
        try:
            return float(text_clean)
        except ValueError:
            return 0.0

    def get_sales_by_category(self, category):
        sales_list = []
        total = 0.0
        count = 0
        for record in self.root:
            cat_elem = record.find('Category')
            if cat_elem is not None:
                cat_text = cat_elem.text.strip() if cat_elem.text else ''
                if cat_text == category:
                    count += 1
                    prod_elem = record.find('ProductName')
                    sales_elem = record.find('Sales')
                    prod_name = prod_elem.text.strip() if prod_elem is not None else 'N/A'
                    sales_val = self.parse_sales_value(sales_elem)
                    sales_list.append(sales_pb2.ProductSales(product_name=prod_name, sales_amount=sales_val))
                    total += sales_val
        return sales_list, total, count

    def get_total_sales(self):
        total = 0.0
        for record in self.root:
            sales_elem = record.find('Sales')
            total += self.parse_sales_value(sales_elem)
        return total

class SalesServiceImpl(sales_pb2_grpc.SalesServiceServicer):
    def __init__(self):
        self.service = SalesDataService('Retail-Supply-Chain-Sales-Dataset_NOVO.xml')

    def GetSalesByCategory(self, request, context):
        sales_list, cat_total, num = self.service.get_sales_by_category(request.category)
        response = sales_pb2.SalesResponse(products=sales_list, category_total=cat_total, num_items=num)
        context.set_code(grpc.StatusCode.OK)
        return response

    def GetTotalSales(self, request, context):  # request é EmptyRequest (vazio)
        total = self.service.get_total_sales()
        response = sales_pb2.TotalSalesResponse(total=total, num_records=len(self.service.root))
        context.set_code(grpc.StatusCode.OK)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sales_pb2_grpc.add_SalesServiceServicer_to_server(SalesServiceImpl(), server)
    server.add_insecure_port('[::]:50051')
    print('Servidor gRPC a correr em localhost:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
