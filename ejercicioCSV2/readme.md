crear JSON.g4 para la gramatica
 -  antlr4 -Dlanguage=Python3 JSON.g4
crear archivo de prueba t.json
crear json_to_xml.py
 -  python json_to_xml.py t.json
en el load agregar las funciones correspondientes
probar:
python json_to_xml.py t.json
python json_to_xml.py t.json salida.xml
crear archivo error.json
probar el archivo errado:
python json_to_xml.py error.json salida.xml

