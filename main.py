from time import time
import os
import pickle

def comparar_datas(data1, data2):
    if data1[2] != data2[2]:
        return data1[2] > data2[2]
    if data1[1] != data2[1]:
        return data1[1] > data2[1]
    if data1[0] != data2[0]:
        return data1[0] > data2[0]
    if data1[3] != data2[3]:
        return data1[3] > data2[3]
    return data1[4] > data2[4]

def troca(lista, i, j):
    lista[i], lista[j] = lista[j], lista[i]

def prioridade(lista, dicionario, pivot):
    nome, seguindo, seguidores, _ = dicionario[lista]
    nome_pivot, seguindo_pivot, seguidores_pivot, _ = dicionario[pivot]

    if seguidores != seguidores_pivot:
        return seguidores > seguidores_pivot
    if seguindo != seguindo_pivot:
        return seguindo > seguindo_pivot
    if nome != nome_pivot:
        return nome < nome_pivot
    return lista < pivot

def particao(lista, inf, sup, dicionario):
    pivot = lista[inf]
    i = inf + 1
    j = sup

    while i <= j:
        while i <= j and prioridade(lista[i], dicionario, pivot):
            i += 1

        while i <= j and not prioridade(lista[j], dicionario, pivot):
            j -= 1

        if i < j:
            troca(lista, i, j)

    troca(lista, inf, j)
    return j

def qsort(lista, inf, sup, dicionario):
    if inf < sup:
        pos = particao(lista, inf, sup, dicionario)
        qsort(lista, inf, pos - 1, dicionario)
        qsort(lista, pos + 1, sup, dicionario)

def particao_postagens(lista, inf, sup):
    pivot = lista[inf]
    i = inf + 1
    j = sup

    while i <= j:
        while i <= j and prioridade_postagens(lista[i], pivot):
            i += 1

        while i <= j and not prioridade_postagens(lista[j], pivot):
            j -= 1

        if i < j:
            troca(lista, i, j)

    troca(lista, inf, j)
    return j

def qsort_postagens(lista, inf, sup):
    if inf < sup:
        pos = particao_postagens(lista, inf, sup)
        qsort_postagens(lista, inf, pos - 1)
        qsort_postagens(lista, pos + 1, sup)

def prioridade_postagens(postagem1, postagem2):
    data1 = postagem1[1][2]
    data2 = postagem2[1][2]   

    if data1 != data2:
        return comparar_datas(data1, data2)
    return postagem1[0] < postagem2[0]

def main(argv=None):
    dicionario = {}
    lista_usuarios = []
    lista_postagens = []
    arquivo = 'usuarios.bin'

    if os.path.isfile(arquivo):
        with open(arquivo, 'rb') as file:
            usuarios = pickle.load(file)

        for login, informacao in usuarios.items():
            dicionario[login] = (informacao[0], len(informacao[1]), len(informacao[2]), informacao[3])
            lista_usuarios.append(login)

        t1 = time()
        qsort(lista_usuarios, 0, len(lista_usuarios) - 1, dicionario)
        t2 = time()
        print(t2-t1)

        primeiro_usuario = lista_usuarios[0]
        for seguindo in usuarios[primeiro_usuario][1]:
            for postagem in usuarios[seguindo][3]:
                lista_postagens.append((seguindo, postagem))

        qsort_postagens(lista_postagens, 0, len(lista_postagens) - 1)

        with open("saida.txt", "w") as f:
            for usuario in lista_usuarios:
                f.write(f"{dicionario[usuario][0]} (segue {dicionario[usuario][1]}, seguido por {dicionario[usuario][2]})\n")

            f.write("---\n")
            f.write(f"Feed de {dicionario[primeiro_usuario][0]}:\n")
            f.write("***\n")
            for postagem in lista_postagens:
                f.write(f"{postagem[0]}\n")
                f.write(f"{postagem[1][0]}\n")
                f.write(f"{postagem[1][1]}\n")
                data = postagem[1][2]
                f.write(f"{data[0]:02}/{data[1]:02}/{data[2]} {data[3]:02}:{data[4]:02}\n")
                f.write("***\n")

if __name__ == '__main__':
    main()