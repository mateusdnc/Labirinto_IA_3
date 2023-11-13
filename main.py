import random as rd
import copy as cp
import math as ma

# ROTINA PARA GERA MATRIZ DE ADJACÊNCIAS
def gera_Ambiente(minimo,maximo,n):
    
    mat = []
    
    for i in range(n):
        linha = []
        for j in range(n):
            if i==j:
                linha.append(0)
            else:
                linha.append(rd.randint(minimo,maximo))
        mat.append(linha)
    return mat

# ROTINA PARA GERAR UMA SOLUÇÃO INICIAL ALEATÓRIA
def solucao_Inicial(n):
    
    s = []
    for i in range(n):
        s.append(i)
    rd.shuffle(s)
    return s

# ROTINA PARA AVALIAR UMA DADA SOLUÇÃO
def avalia_Solucao(s,mat,n):
    
    custo = 0
    for i in range(n-1):
        custo += mat[s[i]][s[i+1]]
    custo += mat[s[n-1]][s[0]]
   
    return custo

# ROTINA PARA GERAR SUCESSORES PARA SUBIDA DE ENCOSTA
def sucessores_enc(s,v,mat):
    melhor = cp.deepcopy(s)
    vm = v
    
    ind = rd.randrange(0,len(s))
    
    for i in range(len(s)):
        suc = cp.deepcopy(s)
        aux      = suc[ind]
        suc[ind] = suc[i]
        suc[i]   = aux
        
        vs = avalia_Solucao(suc,mat,len(s))
        
        if vs<vm:
            melhor = suc
            vm = vs
    
    return melhor, vm

# ROTINA PARA GERAR SUCESSORES PARA TÊMPERA SIMUILADA
def sucessores_temp(s,v,mat):
    suc = cp.deepcopy(s)
    
    ind1 = rd.randrange(0,len(s))
    ind2 = rd.randrange(0,len(s))
    
    aux       = suc[ind1]
    suc[ind1] = suc[ind2]
    suc[ind2] = aux
        
    vs = avalia_Solucao(suc,mat,len(s))

    return suc, vs

# ROTINA SUBIDA DE ENCOSTA
def encosta(si,vi,matriz,n):
    atual = cp.deepcopy(si)
    va = vi
    
    while True:
        novo, vn = sucessores_enc(atual,va,matriz)
        if vn<va:
            atual = novo
            va = vn
        else:
            return atual, va

# ROTINA SUBIDA DE ENCOSTA ALTERADA
def encosta_alt(s,v,matriz,n,tmax):
    atual = cp.deepcopy(si)
    va = vi
    t = 1
    
    while True:
        novo, vn = sucessores_enc(atual,va,matriz)
        if vn<va:
            atual = novo
            va = vn
            t = 1
        else:
            if t<tmax:
                t += 1
            else:
                return atual, va

# ROTINA TÊMPERA SIMULADA
def tempera(si,vi,matriz,ti,tf,fr):
    atual = cp.deepcopy(si)
    va = vi
    temp = ti
    
    while temp>tf:
        novo, vn = sucessores_temp(atual,va,matriz)
        de = vn - va
        if de<0:
            atual = novo
            va = vn
        else:
            ale = rd.uniform(0,1)
            aux = ma.exp(-de/temp)
            if ale<=aux:
                atual = novo
                va = vn
        temp = temp*fr
        
    return atual, va

# ---------------------------------
# MÓDULO PRINCIPAL
# ---------------------------------

# CONFIGURAÇÃO DO PROBLEMA
n      = 6
minimo = 20
maximo = 50

# GERA PROBLEMA - MATRIZ DE ADJACÊNCIAS
matriz = gera_Ambiente(minimo,maximo,n)

qt = 50
ga1 = 0
ga2 = 0
ga3 = 0
for i in range(qt):
    # GERA SOLUÇÃO INICIAL ALEATÓRIA
    si = solucao_Inicial(n)
    
    # AVALIA SOLUÇÃO INICIAL
    vi = avalia_Solucao(si,matriz,n)
    
    # EXECUTA - SUBIDA DE ENCOSTA
    sf, vf = encosta(si,vi,matriz,n)
    ga1 += (vi - vf)/vi
    
    # EXECUTA - SUBIDA DE ENCOSTA ALTERADA
    tmax = n-1
    sf, vf = encosta_alt(si,vi,matriz,n,tmax)
    ga2 += (vi - vf)/vi
     
    # EXECUTA - TEMPERA SIMULADA
    t_ini  = 800
    t_fim  = 0.01
    ft_red = 0.95
    sf, vf = tempera(si,vi,matriz,t_ini,t_fim,ft_red)
    ga3 += (vi - vf)/vi
    
print("Ganho - Subida de Encosta....: ",100*ga1/qt)
print("Ganho - Subida de Encosta_A..: ",100*ga2/qt)
print("Ganho - Têmpera Simulada.....: ",100*ga3/qt)
