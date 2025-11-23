import xml.etree.ElementTree as ET
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from pathlib import Path

print("DEBUG: Servidor XML-RPC arrancou!")

class SalesDataService:
    def __init__(self, xml_file):
        xml_path = Path(xml_file).resolve()
        if not xml_path.exists():
            raise FileNotFoundError(f"XML não encontrado: {xml_path}")
        self.tree = ET.parse(str(xml_path))
        self.root = self.tree.getroot()

    def get_sales_by_category(self, category):
        category = category.strip()
        sales = []
        for record in self.root:
            cat_elem = record.find('Category')
            if cat_elem is not None:
                cat_text = cat_elem.text.strip() if cat_elem.text else ''
                if cat_text == category:
                    prod_elem = record.find('ProductName')
                    sales_elem = record.find('Sales')
                    prod_name = prod_elem.text.strip() if prod_elem is not None else 'N/A'
                    text_sales = sales_elem.text.strip() if sales_elem is not None else '0'
                    text_clean = text_sales.replace(',', '').replace('$', '')
                    try:
                        sales_val = float(text_clean)
                    except ValueError:
                        sales_val = 0.0
                    sales.append({'product': prod_name, 'sales': sales_val})
        return sales

    def get_total_sales(self):
        total = 0.0
        for record in self.root:
            sales_elem = record.find('Sales')
            if sales_elem is not None:
                text = sales_elem.text.strip() if sales_elem.text else '0'
                text_clean = text.replace(',', '').replace('$', '')
                try:
                    val = float(text_clean)
                    total += val
                except ValueError:
                    pass
        return total

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

if __name__ == '__main__':
    server = SimpleXMLRPCServer(('0.0.0.0', 8000), requestHandler=RequestHandler)
    server.register_introspection_functions()
    service = SalesDataService('Retail-Supply-Chain-Sales-Dataset_NOVO.xml')
    server.register_instance(service, allow_dotted_names=True)
    print('Servidor XML-RPC a correr em localhost:8000')
    server.serve_forever()
