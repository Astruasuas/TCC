from owlready2 import *

sistema = get_ontology('sistema_usuario_tcc.rdf').load()

estudante = sistema.Estudante_1
pesquisador = sistema.Pesquisador_2
instituicao = sistema.instituição_3

pt = sistema.portugues
en = sistema.ingles

def interesses(perfil):

    fala_pt = pt in perfil.falaIdioma
    fala_en = en in perfil.falaIdioma

    termos_pt = []
    termos_en = []

    if fala_pt and fala_en:
        for termo in perfil.temInteresse:
            termos_pt.append(termo.rotuloPT)
            termos_en.append(termo.rotuloEN)
        return termos_pt, termos_en
    elif fala_pt:
        for termo in perfil.temInteresse:
            termos_pt.append(termo.rotuloPT)
        return termos_pt, []
    elif fala_en:
        for termo in perfil.temInteresse:
            termos_en.append(termo.rotuloEN)
        return [], termos_en
    else:
        return [], []


def main():
    interesses(pesquisador)

if __name__ == '__main__':
    main()