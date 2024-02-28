from flask import Flask, render_template, request
pila= []
import re
from tabla_predictiva import tabla_predictiva

app = Flask(__name__)

mensajeERROR = ""
texto = ""
bandera2 = False

@app.route('/')
def pagina():
    return render_template('formulario.html', bandera='')

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"

TOKEN_TYPES = {
    'FUNCTION': r'\bfunction\b', 'OPEN_PAREN': r'\(', 'LETTER': r'[a-zA-Z]', 'VAR': r'\bvar\b', 
    'TWO_DOT': r'\:', 'CLOSE_PAREN': r'\)', 'BOOLEAN': r'\bboolean\b', 'NUMBER': r'\d', 'STRING': r'\bstring\b',
    "DOT_COMA": r'\;', 'WHITESPACE': r'\s', 'EPSILON': r'\ε', 'PESO': r'\$',
}

def tokenize(input_string):
    global mensajeERROR, texto
    tokens = []
    while input_string:
        match = None
        for token_type, token_regex in TOKEN_TYPES.items():
            if token_type in ['WHITESPACE', 'LETTER', 'NUMBER']:
                continue

            regex_match = re.match(token_regex, input_string)
            if regex_match:
                match = regex_match
                tokens.append(Token(token_type, regex_match.group(0)))
                break

        if not match:
            for token_type in ['LETTER', 'NUMBER', 'WHITESPACE']:
                regex_match = re.match(TOKEN_TYPES[token_type], input_string)
                if regex_match:
                    match = regex_match
                    if token_type != 'WHITESPACE':
                        tokens.append(Token(token_type, regex_match.group(0)))
                    break

        if not match:
                mensajeERROR = f"Error en el caracer: {input_string[0]}"
                return render_template('formulario.html', bandera=False, texto=texto, pila=pila, mensajeERROR=mensajeERROR)

        input_string = input_string[match.end():]

    tokens.append(Token('EOF', '$'))
    return tokens

class SimpleParser:
    global mensajeERROR, texto
   
    def __init__(self, input_string):
        self.tokens = tokenize(input_string)
        try:          
            self.tokens.append(Token('EOF', '$'))
        except:
            return render_template('formulario.html', bandera=False, texto=texto, pila=pila, mensajeERROR=mensajeERROR)
        self.stack = ['$', 'start']
        self.pointer = 0
        
    def parse(self):
        global mensajeERROR, bandera2

        while True:
            top = self.stack[-1]
            current_token = self.tokens[self.pointer]

            pila.append(self.stack.copy())

            if self.stack[-1] == '$':
                if any(token.tipo == 'PESO' for token in self.tokens):
                    mensajeERROR = "Error: token PESO ($) detectado en la entrada."
                    self.error(mensajeERROR)
                else:
                    print("Análisis completado correctamente.")
                    break


            if self.is_terminal(top):
                if top == current_token.tipo:
                    print("imprimiendo top para terminal", top)
                    self.stack.pop()
                    pila.append(self.stack.copy())
                    self.pointer += 1
                else:
                    self.error("Error de sintaxis")
            elif top == 'EPSILON':
                print("imprimiendo top para epsilon", top)
                self.stack.pop()
                pila.append(self.stack.copy())
                continue
            else:
                print("imprimiendo top para get", top)
                production = self.get_production(top, current_token.tipo)
                if production:
                    self.stack.pop()
                    self.push_production(production)

    def peek_next_token(self):
        if self.pointer + 1 < len(self.tokens):
            return self.tokens[self.pointer + 1]
        else:
            return Token('EOF', '$')

    def is_terminal(self, token_type):
            terminals = [
                'FUNCTION', 'OPEN_PAREN', 'LETTER', 'VAR', 'TWO_DOT', 
                'CLOSE_PAREN', 'BOOLEAN', 'NUMBER', 'STRING', "DOT_COMA",
            ]

            return token_type in terminals

    def get_production(self, non_terminal, current_token):
        clave = (non_terminal, current_token)
        production = tabla_predictiva.get(clave)

        if production:
            return production
        else:
            self.error(f"No se encontró producción para {non_terminal} con token {current_token}")
            return None


    def push_production(self, production):
        for symbol in reversed(production):
                self.stack.append(symbol)

    def error(self, message):
        global mensajeERROR
        if self.pointer < len(self.tokens):
            current_token = self.tokens[self.pointer]
            raise SyntaxError(f"{message} en la posición {self.pointer} (Token: {current_token.tipo}, Valor: '{current_token.valor}')")
        else:
            raise SyntaxError(f"{message} al final de la entrada")

@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    global mensajeERROR, bandera2
    texto = request.form.get('texto')

    try:
        parser = SimpleParser(texto)
        
    except:
        print("errorsito")
        return render_template('formulario.html', bandera2=False, texto=texto, pila=pila, mensajeERROR=mensajeERROR)

    try:
        parser.parse()
        bandera2 = True
        mensajeERROR = ""
    except SyntaxError as e:
        bandera2 = False
        mensajeERROR = f"Error en el análisis: {e}"

    return render_template('formulario.html', bandera2=bandera2, texto=texto, pila=pila, mensajeERROR=mensajeERROR)

if __name__ == '__main__':
    app.run(debug=False)
