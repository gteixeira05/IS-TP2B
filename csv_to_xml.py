import csv
import xml.etree.ElementTree as ET

def csv_para_xml(caminho_csv, caminho_xml):
    # Criar elemento root
    root = ET.Element("Root")

    # Abrir o ficheiro CSV
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for linha in reader:
            row_elem = ET.SubElement(root, "Row")

            # Para cada coluna, criar um elemento XML
            for campo, valor in linha.items():
                # Converter nomes das colunas para CamelCase e remover caracteres inválidos
                nome_tag = campo.strip().replace(" ", "").replace("-", "")
                nome_tag = nome_tag[0].upper() + nome_tag[1:]  # Primeira letra maiúscula
                elem = ET.SubElement(row_elem, nome_tag)
                elem.text = valor.strip() if valor else ""

    # Criar árvore XML
    arvore = ET.ElementTree(root)
    ET.indent(arvore, space="  ", level=0)  # Formatar com indentação

    # Escrever no ficheiro
    with open(caminho_xml, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        arvore.write(f, encoding='utf-8')

    print(f"XML gerado com sucesso: {caminho_xml}")

# Exemplo de uso
csv_para_xml("Retail-Supply-Chain-Sales-Dataset.csv",
             "Retail-Supply-Chain-Sales-Dataset_NOVO.xml")
