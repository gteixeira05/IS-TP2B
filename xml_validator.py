from lxml import etree

def validar_xml(xml_file, xsd_file):
    # Ler o schema XSD
    with open(xsd_file, 'rb') as f:
        schema_root = etree.XML(f.read())
    schema = etree.XMLSchema(schema_root)

    # Ler o XML gerado
    with open(xml_file, 'rb') as f:
        xml_doc = etree.parse(f)

    # Validar
    valido = schema.validate(xml_doc)
    if valido:
        print('XML válido️')
    else:
        print('XML inválido')
        for error in schema.error_log:
            print(error.message)

# Exemplo de uso:
validar_xml('Retail-Supply-Chain-Sales-Dataset_NOVO.xml',
            'Retail-Supply-Chain-Sales-Dataset_NOVO.xsd')



