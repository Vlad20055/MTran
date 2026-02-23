import sys
from focal_lexer.lexer import LexicalAnalyzer

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            source = f.read()
    else:
        # Пример программы
        source = """1.10 T " Решаем квадратное уравнение вида: A*X^2 + B*X + C = 0 "!
1.20 T "Введите коэффициенты A != 0, B, C"!
1.30 A " A=",A, " B=",B, " C=",C
1.35 I (A) 1.40, 1.20, 1.40
1.40 S D=B*B-4*A*C
1.50 T "Дискриминант D=",D," "; I (D)1.90,1.80,1.60
1.60 T !,"Два корня:"!
1.70 T "X1=", (-B+FSQT(D))/(2*A) !
1.75 T "X2=", (-B-FSQT(D))/(2*A) !
1.77 G 1.99
1.80 T !,"Один корень: X=", (-B)/(2*A) !
1.85 G 1.99
1.90 T !,"Корней нет"!
1.99 T "Всё"! ; Q ; comment exit
"""
    lexer = LexicalAnalyzer(source)
    tokens = lexer.tokenize()
    for tok in tokens:
        print(tok)

if __name__ == "__main__":
    main()