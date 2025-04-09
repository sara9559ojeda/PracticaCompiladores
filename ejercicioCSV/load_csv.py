import sys
import re
from antlr4 import *
from CSVLexer import CSVLexer
from CSVParser import CSVParser
from CSVListener import CSVListener

class Loader(CSVListener):
    EMPTY = ""

    def __init__(self):
        self.rows = []
        self.header = []
        self.currentRowFieldValues = []
        self.monthCount = {} 
        self.monthTotals = {}  # ← Suma total por mes
        self.uniqueRows = set()       
        self.duplicateRows = []
        self.formatErrors = []
        self.currentLine = 1

    def enterRow(self, ctx: CSVParser.RowContext):
        self.currentRowFieldValues = []
        self.currentLine = ctx.start.line

    def exitText(self, ctx: CSVParser.TextContext):
        self.currentRowFieldValues.append(ctx.getText())

    def exitString(self, ctx: CSVParser.StringContext):
        self.currentRowFieldValues.append(ctx.getText())

    def exitEmpty(self, ctx: CSVParser.EmptyContext):
        self.currentRowFieldValues.append(self.EMPTY)

    def exitHeader(self, ctx: CSVParser.HeaderContext):
        self.header = list(self.currentRowFieldValues)

    def is_valid_cantidad(self, val):
        val = val.strip().replace('"', '')
        pattern = r"^\$\d{1,3}(,\d{3})*$|^\$\d+$"
        return re.match(pattern, val) is not None

    def parse_cantidad(self, val):
        # "$1,200" -> 1200.0
        val = val.replace('"', '').replace('$', '').replace(',', '')
        return float(val)

    def exitRow(self, ctx: CSVParser.RowContext):
        if ctx.parentCtx.getRuleIndex() == CSVParser.RULE_header:
            return

        m = {}
        for i, val in enumerate(self.currentRowFieldValues):
            key = self.header[i] if i < len(self.header) else f"col_{i}"
            m[key] = val
        self.rows.append(m)

        mes = m.get("Mes", "").strip().replace('"', '')

        if mes:
            self.monthCount[mes] = self.monthCount.get(mes, 0) + 1

        cantidad_str = m.get("Cantidad", "").strip()

        if self.is_valid_cantidad(cantidad_str):
            cantidad = self.parse_cantidad(cantidad_str)
            if mes:
                self.monthTotals[mes] = self.monthTotals.get(mes, 0.0) + cantidad
        else:
            self.formatErrors.append({
                "linea": self.currentLine,
                "valor": cantidad_str,
                "error": "Cantidad vacía o mal formateada"
            })

        # Duplicados
        row_tuple = tuple(m.get(col, "") for col in self.header)
        if row_tuple in self.uniqueRows:
            self.duplicateRows.append(m)
        else:
            self.uniqueRows.add(row_tuple)

def main(argv):
    input_stream = FileStream(argv[1], encoding='utf-8')
    lexer = CSVLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CSVParser(stream)
    tree = parser.csvFile()

    loader = Loader()
    walker = ParseTreeWalker()
    walker.walk(loader, tree)

    print("📋 Filas procesadas:")
    for row in loader.rows:
        print(row)

    print("\n📅 Conteo de meses:")
    for mes, count in loader.monthCount.items():
        print(f"{mes}: {count} vez/veces")

    print("\n💰 Totales por mes:")
    for mes, total in loader.monthTotals.items():
        print(f"{mes}: ${total:,.2f}")

    print("\n🚨 Filas duplicadas:")
    if loader.duplicateRows:
        for dup in loader.duplicateRows:
            print(dup)
    else:
        print("✅ No hay filas duplicadas.")

    print("\n🧯 Errores en el campo 'Cantidad':")
    if loader.formatErrors:
        for err in loader.formatErrors:
            print(f"Línea {err['linea']}: Valor '{err['valor']}' -> {err['error']}")
    else:
        print("✅ Todos los campos 'Cantidad' tienen formato válido.")

if __name__ == '__main__':
    main(sys.argv)
