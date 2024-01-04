import re

def validar_cpf(cpf):
    cpf = re.sub('[^0-9]', '', cpf)
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False

    for i in range(9, 11):
        valor = sum((int(cpf[j]) * ((i + 1) - j) for j in range(0, i)))
        dígito = ((valor * 10) % 11) % 10
        if str(dígito) != cpf[i]:
            return False
    return True

def validar_pis_pasep(pis):
    pis = re.sub('[^0-9]', '', pis)
    if len(pis) != 11:
        return False

    multiplicadores = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(digito) * multiplicador for digito, multiplicador in zip(pis, multiplicadores))
    digito = 11 - soma % 11
    digito = 0 if digito >= 10 else digito

    return pis[-1] == str(digito)

def validar_titulo_eleitor(titulo):
    titulo = re.sub('[^0-9]', '', titulo)
    if len(titulo) != 12:
        return False

    estado = int(titulo[-4:-2])
    if estado < 1 or estado > 28:
        return False

    digitos = [int(d) for d in titulo]
    digito1 = sum(d * (i + 2) for i, d in enumerate(digitos[:8])) % 11
    digito1 = 0 if digito1 > 9 else digito1
    digito2 = sum(d * (i + 2) for i, d in enumerate(digitos[8:11] + [digito1])) % 11
    digito2 = 0 if digito2 > 9 else digito2

    return digitos[10] == digito1 and digitos[11] == digito2

def validar_cnh(cnh):
    if not re.match(r'^\d{11}$', cnh):
        return False

    base_cnh = cnh[:-2]
    dv_cnh = cnh[-2:]

    nM1, nM2 = 9, 1
    nDV1, nDV2 = 0, 0
    lMaior = False

    for digito in base_cnh:
        nVL = int(digito)
        nDV1 += nVL * nM1
        nDV2 += nVL * nM2
        nM1 -= 1
        nM2 += 1

    nDV1 = nDV1 % 11
    if nDV1 > 9:
        nDV1 = 0
        lMaior = True

    nDV2 = nDV2 % 11
    if lMaior:
        nDV2 = nDV2 - 2 if nDV2 - 2 >= 0 else nDV2 + 9

    nDV2 = 0 if nDV2 > 9 else nDV2

    return dv_cnh == f'{nDV1}{nDV2}'

def extrair_numeros_documentos(texto):
    # Padrões de regex
    cpf_pattern = r'\b(?:\d{3}[.-]?){3}\d{2}\b'
    pis_pasep_pattern = r'\b\d{3}[.-]?\d{5}[.-]?\d{2}[.-]?\d{1}\b'
    titulo_eleitor_pattern = r'\b\d{12}\b'
    cnh_pattern = r'\b\d{11}\b'
    passaporte_pattern = r'\b[A-Z]{2}\d{6}\b'
    email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
    cep_pattern = r'\b\d{5}-?\d{3}\b'
    telefone_pattern = r'\(?\b[1-9]{2}\)? ?9?\d{4}-?\d{4}\b|\b9?\d{4}-?\d{4}\b'
    placa_veiculo_pattern = r'\b[a-zA-Z]{3}[0-9]{1}[a-zA-Z]{1}[0-9]{2}\b|\b[a-zA-Z]{3}-?[0-9]{4}\b'

    # Padrão para tipo "Outros"
    outros_pattern = r'\b(?:\d[ .-/,]?){2,20}\b'

    # Exclui padrões específicos do tipo "Outros"
    texto_sem_especificos = re.sub('|'.join([cpf_pattern, pis_pasep_pattern, titulo_eleitor_pattern, 
                                             cnh_pattern, passaporte_pattern, email_pattern, 
                                             cep_pattern, telefone_pattern, 
                                             placa_veiculo_pattern]), '', texto)

    # Busca por padrões
    cpfs = re.findall(cpf_pattern, texto)
    pis_pasep = re.findall(pis_pasep_pattern, texto)
    titulos_eleitor = re.findall(titulo_eleitor_pattern, texto)
    cnhs = re.findall(cnh_pattern, texto)
    passaportes = re.findall(passaporte_pattern, texto)
    emails = re.findall(email_pattern, texto)
    ceps = re.findall(cep_pattern, texto)
    telefones = re.findall(telefone_pattern, texto)
    placas_veiculo = re.findall(placa_veiculo_pattern, texto)
    outros = re.findall(outros_pattern, texto_sem_especificos)

    # Validação
    cpfs_validos = [cpf for cpf in cpfs if validar_cpf(cpf)]
    pis_pasep_validos = [pis for pis in pis_pasep if validar_pis_pasep(pis)]
    titulos_validos = [titulo for titulo in titulos_eleitor if validar_titulo_eleitor(titulo)]
    cnhs_validas = [cnh for cnh in cnhs if validar_cnh(cnh)]

    resultados = {
        'CPF': cpfs_validos,
        'PIS/PASEP': pis_pasep_validos,
        'Título de Eleitor': titulos_validos,
        'CNH': cnhs_validas,
        'Passaporte': passaportes,
        'E-mail': emails,
        'CEP': ceps,
        'Telefone': telefones,
        'Placa de Veículo': placas_veiculo,
        'Outros': outros
    }

    return resultados

# Exemplo de uso
texto_exemplo = "Meu CPF é 123.456.789-09, PIS 123.45678.12.3, Título 123456789012, CNH 52798802300, e-mail exemplo@dominio.com, CEP 12345-678, nasci em 01/01/1980, tel: (11) 98765-4321, placa ABC1D23."
dados_extraídos = extrair_numeros_documentos(texto_exemplo)
print(dados_extraídos)
