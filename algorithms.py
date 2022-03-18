##  UNIVERSIDAD DEL VALLE DE GUATEMALA
##  DISEÑO DE LENGUAJES DE PROGRAMACIÓN
##  PROYECTO NO. 1
##  LUIS PEDRO CUÉLLAR - 18220

from thompson import *
import re
from subset import subsets_alg
from direct_construction import direct_const
from tree import generate_tree
from tools import *


expression = input('Ingresar expresión regular --> ')
expression = expression.replace('ε','e')
print('expresión regular ingresada --> : ',expression)
balanced = check(expression)

if balanced != False:
    converted = parseExp(expression)
    print('expresión convertida --> : ', converted)

    expanded = expand(converted)
    print('expresión expandida --> : ', expanded)

    postfix = evaluate(expanded)
    print('expresión postfix --> : ', postfix)

    afn = thompson_alg(postfix)
    graphicAFN(afn)
    gen_afn_txt(afn)
    dfa = subsets_alg(afn)
    graphicAFD(dfa)
    gen_afd_txt(dfa)
    print("construcción directa")
    tree = generate_tree(expanded)
    troptionitions = direct_const(tree, expanded)
    graphicDirect(troptionitions)
else:
    print("La expresión regular ingresada tiene un error!")
