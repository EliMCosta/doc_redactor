import json
import requests
import time
neuron_catalyst="Maria Fulana"
def process_text_with_ai(text_to_analyse: str, ai_api: str):
    # Substituir quebras de linha e tabs
    text_to_analyse = text_to_analyse.replace("\n", "\\n").replace("\t", "\\t")

    if ai_api == "openai":
      from openai import OpenAI
      client = OpenAI()
      
      prompt = f"Me dê o json com possíveis PII da cadeia de strings: {text_to_analyse}"
      response = client.chat.completions.create(
        model = "gpt-4-1106-preview",
        #seed=159644,
        #temperature=0.1,
        response_format={"type": "json_object"},
        messages=[
          {"role": "system", "content": "Você é uma IA que analisa documentos administrativos em busca de Informações Pessoais (PII) e ignora substantivos comuns."},
          {"role": "user", "content": "Me dê o json com possíveis PII da cadeia de strings: Banana , \n 013.000.111-09, contrato \n  assina este serviços de informática"},
          {"role": "assistant", "content": 
          """{
              "pii": [
                {
                  "type": "CPF",
                  "value": "013.000.111-09",
                  "context": "Número de documento de assinante de contrato de prestação de serviços de informática"
                }
              ]
            }"""
          },  
          {"role": "user", "content": "Me dê o json com possíveis PII da cadeia de strings: Em atenção ao Despacho  ̶  TERRACAP/PRESI/GABIN/ASSOC(122558628), em referência à minuta da Política de Privacidade de Dados Pessoais"},
          {"role": "assistant", "content": 
          """{
              "pii": []
            }"""
          },      
          {"role": "user", "content": prompt}
        ] 
      )
      response=response.choices[0].message.content

    else:
      url = "http://localhost:11434/api/generate"
      payload = {
          "model": "openhermes:7b-mistral-v2.5-q5_K_M",
          "prompt": f"Give me all personal related information in this text. Use json only for response with 'type', 'value' and 'context' with each pii under a 'pii':[{'type', 'value', 'context', 'is_value_pii'}] list. Type can be person's name, date of birth, RG, CPF, CNH number, passport number, identity number, address, personal phone number, email address, banking information, medical history, employment information, affiliation, academic information, data from social networks and geographic location; value is a pii instance. Return 'pii':[] if no pii found. TEXT: '{text_to_analyse}'", #openhermes2.5-mistral:7b-q5_K_M
          "format": "json",
          "stream": False,
          "options": {
            "temperature": 0
          }
      }
      headers = {"Content-Type": "application/json", "accept": "application/json"}

      response = requests.post(url, json=payload, headers=headers)
      if response.status_code == 200:
          # Verifica se a resposta é uma string JSON
          if isinstance(response.text, str):
              # Fazendo o parsing da string JSON
              parsed_response = json.loads(response.text)
              response = json.loads(parsed_response["response"])
          else:
              response = "A resposta não é uma string JSON"
      else:
          response = f"Erro na chamada: {response.status_code}"
      # Verifica se response é uma string e faz o parsing JSON
      if isinstance(response, str):
          response = json.loads(response)
      # Filtrar os dicionários onde o 'value' não é vazio
      filtered_pii = [item for item in response['pii'] if item.get('value') and item.get('value') != neuron_catalyst]
      # Atualizar o dicionário original com os dicionários filtrados
      response['pii'] = filtered_pii
      time.sleep(1)
      
    return response

