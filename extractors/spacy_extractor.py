import json
import spacy

text_to_analyse = """
Contratante: Soluções XYZ Ltda., sociedade empresária limitada, inscrita no CNPJ
sob o nº 12.345.678/0001-90, com sede na Rua das Acácias, nº 123, Centro, São
Paulo, SP, CEP 01000-000, neste ato representada por seu Diretor, Sr. João da Silva,
brasileiro,casado, portador da cédula de identidade RG nº 1.234.567-8 SSP/SP e 
inscrito no CPF sob o nº 123.456.789-00
"""

nlp = spacy.load('pt_core_news_lg')

def extract_pii(text):
    doc = nlp(text)
    
    pii_list = []
    for entity in doc.ents:
        if entity.label_ in ["PER", "LOC"]:
            pii_dict = {"type": entity.label_, "value": str(entity.text)}
            pii_list.append(pii_dict)
    
    return json.dumps({"pii": pii_list})

# Substitua {text_to_analyse} pelo seu texto real
response = extract_pii(text_to_analyse)
print(response)
