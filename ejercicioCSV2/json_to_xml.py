from antlr4 import *
from JSONLexer import JSONLexer
from JSONParser import JSONParser
from JSONListener import JSONListener
from antlr4.error.ErrorListener import ErrorListener
import sys

# Listener que lanza excepción en errores de sintaxis
class ThrowingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception(f"💥 Error de sintaxis en línea {line}, columna {column}: {msg}")

class XMLEmitter(JSONListener):
    def __init__(self):
        self.xml_map = {}
        self.indent_level = {}

    def indent(self, level):
        return '  ' * level

    def getXML(self, ctx):
        return self.xml_map.get(ctx, '')

    def setXML(self, ctx, value, level=0):
        self.xml_map[ctx] = value
        self.indent_level[ctx] = level

    def exitAtom(self, ctx):
        self.setXML(ctx, ctx.getText(), self.indent_level.get(ctx.parentCtx, 0) + 1)

    def exitString(self, ctx):
        text = ctx.getText().strip('"')
        self.setXML(ctx, text, self.indent_level.get(ctx.parentCtx, 0) + 1)

    def exitObjectValue(self, ctx):
        val = self.getXML(ctx.jsonObject())
        self.setXML(ctx, val, self.indent_level.get(ctx.parentCtx, 0) + 1)

    def exitArrayValue(self, ctx):
        val = self.getXML(ctx.array())
        self.setXML(ctx, val, self.indent_level.get(ctx.parentCtx, 0) + 1)

    def exitPair(self, ctx):
        tag = ctx.STRING().getText().strip('"')
        val = self.getXML(ctx.value())
        level = self.indent_level.get(ctx.parentCtx, 0) + 1
        xml = f"{self.indent(level)}<{tag}>{val}</{tag}>\n"
        self.setXML(ctx, xml, level)

    def exitAnObject(self, ctx):
        level = self.indent_level.get(ctx.parentCtx, 0)
        xml = ''.join(self.getXML(p) for p in ctx.pair())
        self.setXML(ctx, xml, level)

    def exitEmptyObject(self, ctx):
        level = self.indent_level.get(ctx.parentCtx, 0)
        self.setXML(ctx, '', level)

    def exitArrayOfValues(self, ctx):
        level = self.indent_level.get(ctx.parentCtx, 0) + 1
        body = ''.join(f"{self.indent(level)}<element>{self.getXML(v)}</element>\n" for v in ctx.value())
        self.setXML(ctx, body, level)

    def exitEmptyArray(self, ctx):
        level = self.indent_level.get(ctx.parentCtx, 0)
        self.setXML(ctx, '', level)

    def exitJson(self, ctx):
        self.setXML(ctx, self.getXML(ctx.getChild(0)), self.indent_level.get(ctx.getChild(0), 0))

def main(argv):
    if len(argv) < 2:
        print("Uso: python json_to_xml.py entrada.json salida.xml")
        return

    input_file = argv[1]
    output_file = argv[2] if len(argv) > 2 else "salida.xml"

    try:
        input_stream = FileStream(input_file, encoding='utf-8')
        lexer = JSONLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = JSONParser(stream)

        # Activar validación estricta
        parser.removeErrorListeners()
        parser.addErrorListener(ThrowingErrorListener())

        tree = parser.json()

        xml_generator = XMLEmitter()
        walker = ParseTreeWalker()
        walker.walk(xml_generator, tree)

        xml = xml_generator.getXML(tree)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(xml)

        print(f"✅ XML generado y guardado en: {output_file}")

    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main(sys.argv)
