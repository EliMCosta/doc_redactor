# Solucao para "doc redaction"

### Disclaimer: este repositorio possui codigo a nivel de PoC apenas e nao constitui produto pronto. Necessario otimizacoes, integracoes, adicionar robustez (manipulacao de erros e excecoes, performance de concorrencia etc.), revisoes de seguranca etc.

Instalar dependências:
python -m pip install -r requirements.txt

Exporte a chave de API da OpenAI:
export OPENAI_API_KEY=yourapikei

Executar o servidor:
cd src/
uvicorn main:app --reload

Documentacao OpenAPI da API REST do servidor FastAPI:
http://127.0.0.1:8000/docs

Chamada:
POST /process-pdf?input_pdf_path={your_absolute_input_path} HTTP/1.1
Accept: application/json
Host: 127.0.0.1:8000

Recomendado trabalhar com ambiente python virtual usando Conda ou outros gerenciadores.

Para contrucao de solucao com hardware fraco (pouca capacidade de processamento paralelo), recomenda-se o uso de reconhecimento de padroes + modulo de processamento de linguagem leves (como Spacy).

