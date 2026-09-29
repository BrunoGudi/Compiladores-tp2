import re

patron_id = re.compile(r"[a-zA-Z_][a-zA-Z_0-9]*")
patron_num = re.compile(r"[0-9]+")


def analizar_ej10(cadena):
    tokens, errores = [], []
    posicion, linea, columna = 0, 1, 1

    while posicion < len(cadena):
        resto = cadena[posicion:]
        if cadena[posicion] in " \t":
            posicion, columna = posicion + 1, columna + 1
            continue
        if cadena[posicion] == "\n":
            posicion, linea, columna = posicion + 1, linea + 1, 1
            continue

        coincidencia = patron_id.match(resto)
        if coincidencia:
            lexema = coincidencia.group()
            tokens.append(("ID", lexema, linea, columna))
            posicion, columna = posicion + len(lexema), columna + len(lexema)
            continue

        coincidencia = patron_num.match(resto)
        if coincidencia:
            lexema = coincidencia.group()
            tokens.append(("NUM", lexema, linea, columna))
            posicion, columna = posicion + len(lexema), columna + len(lexema)
            continue

        if cadena[posicion] == "=":
            tokens.append(("ASIG", "=", linea, columna))
            posicion, columna = posicion + 1, columna + 1
            continue
        if cadena[posicion] == "+":
            tokens.append(("SUMA", "+", linea, columna))
            posicion, columna = posicion + 1, columna + 1
            continue
        if cadena[posicion] == "-":
            tokens.append(("RESTA", "-", linea, columna))
            posicion, columna = posicion + 1, columna + 1
            continue
        if cadena[posicion] == "*":
            tokens.append(("MULT", "*", linea, columna))
            posicion, columna = posicion + 1, columna + 1
            continue
        if cadena[posicion] == "/":
            tokens.append(("DIV", "/", linea, columna))
            posicion, columna = posicion + 1, columna + 1
            continue
        if cadena[posicion] == "(":
            tokens.append(("LPAREN", "(", linea, columna))
            posicion, columna = posicion + 1, columna + 1
            continue
        if cadena[posicion] == ")":
            tokens.append(("RPAREN", ")", linea, columna))
            posicion, columna = posicion + 1, columna + 1
            continue

        errores.append(("ERROR_LEXICO", cadena[posicion], linea, columna))
        posicion, columna = posicion + 1, columna + 1

    return tokens, errores, linea


def mostrar_resultados(tokens, errores):
    print("\n" + "=" * 40 + "\n          TABLA DE TOKENS\n" + "=" * 40)
    print(f"{'LINEA':<8}{'COLUMNA':<10}{'TOKEN':<24}{'LEXEMA'}\n" + "-" * 65)
    for t, lx, l, c in tokens: print(f"{l:<8}{c:<10}{t:<24}{lx}")
    if errores:
        print("\n" + "=" * 40 + "\n          ERRORES LEXICOS\n" + "=" * 40)
        for i, (t, lx, l, c) in enumerate(errores, 1): print(
            f"Error {i} -> Tipo: {t} | Lexema: {lx} | Linea: {l} | Columna: {c}")


if __name__ == "__main__":
    cadenas_prueba = [
        "id + id * id",
        "a + b * c",
        "(a + b) * c",
        "a * (b + c)",
        "a + b * (c - 5)",
        "resultado = a + b * (c - 10)",
        "resultado = a + * b",
        "resultado = (a + b"
    ]

    for c in cadenas_prueba:
        print(f"\n>>> Analizando Cadena: '{c}'")
        tokens, errores, lineas = analizar_ej10(c)
        mostrar_resultados(tokens, errores)