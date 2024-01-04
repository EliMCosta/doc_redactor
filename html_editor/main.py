import json

doc = "html_editor/1234.html"

NAMED_ENTITIES = {
    'á': '&aacute;',
    'Á': '&Aacute;',
    'â': '&acirc;',
    'Â': '&Acirc;',
    'à': '&agrave;',
    'À': '&Agrave;',
    'å': '&aring;',
    'Å': '&Aring;',
    'ã': '&atilde;',
    'Ã': '&Atilde;',
    'ä': '&auml;',
    'Ä': '&Auml;',
    'æ': '&aelig;',
    'Æ': '&AElig;',
    'ç': '&ccedil;',
    'Ç': '&Ccedil;',
    'é': '&eacute;',
    'É': '&Eacute;',
    'ê': '&ecirc;',
    'Ê': '&Ecirc;',
    'è': '&egrave;',
    'È': '&Egrave;',
    'ë': '&euml;',
    'Ë': '&Euml;',
    'í': '&iacute;',
    'Í': '&Iacute;',
    'î': '&icirc;',
    'Î': '&Icirc;',
    'ì': '&igrave;',
    'Ì': '&Igrave;',
    'ï': '&iuml;',
    'Ï': '&Iuml;',
    'ñ': '&ntilde;',
    'Ñ': '&Ntilde;',
    'ó': '&oacute;',
    'Ó': '&Oacute;',
    'ô': '&ocirc;',
    'Ô': '&Ocirc;',
    'ò': '&ograve;',
    'Ò': '&Ograve;',
    'ø': '&oslash;',
    'Ø': '&Oslash;',
    'õ': '&otilde;',
    'Õ': '&Otilde;',
    'ö': '&ouml;',
    'Ö': '&Ouml;',
    'ß': '&szlig;',
    'ú': '&uacute;',
    'Ú': '&Uacute;',
    'û': '&ucirc;',
    'Û': '&Ucirc;',
    'ù': '&ugrave;',
    'Ù': '&Ugrave;',
    'ü': '&uuml;',
    'Ü': '&Uuml;',
    'ÿ': '&yuml;',
    '©': '&copy;',
    '®': '&reg;',
}

def custom_escape(s):
    return ''.join(NAMED_ENTITIES.get(c, c) for c in s)

def load_words_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def escape_words_to_html_entities(words):
    return [custom_escape(word) for word in words]

# Load words from the JSON file
words_list = load_words_from_json('html_editor/censored_words.json')

escaped_list = escape_words_to_html_entities(words_list)

# Ler o arquivo HTML
with open(doc, 'r') as file:
    content = file.read()

# Substituir palavras censuradas por [CENSURADO]
for palavra in escaped_list:
    content = content.replace(palavra, '<strong>[CENSURADO]</strong>')

# Salvar o arquivo HTML editado
with open(doc, 'w') as file:
    file.write(content)

print("Arquivo "+doc+" editado com sucesso!")
