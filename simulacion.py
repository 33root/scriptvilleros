# -*- coding: cp1252 -*-
import random
from math import log, sqrt
from IPython import embed
import os


def dibujar():
    for N in N_ARR:
        arr_stol, arr_ptel, arr_ptei = [], [], []
        pstob, pstom = [], []
        for M in M_ARR:
            res = resultados[M, N]
            arr_ptel.append(res['PTEL'])
            # print "x= " + str(res['PTEL'])
            arr_ptei.append(res['PTEI'])

            tot = 0
            for i in res['VTOM']:
                tot = tot + i
            pstom.append(tot / len(res['VTOM']))

            tot = 0
            for i in res['VTOB']:
                tot = tot + i
            pstob.append(tot / len(res['VTOB']))

        dibujar_PTE(arr_ptel, arr_ptei, M_ARR, N)
        dibujar_STO(pstom, pstob, M_ARR, N)


def dibujar_STO(pstom, pstob, arr_m, n):
    import numpy as np
    import matplotlib.pyplot as plt
    pstom = np.array(pstom)
    pstob = np.array(pstob)

    fig, ax1 = plt.subplots(nrows=1, sharex=True)
    ax1.set_title(
        'Porcentaje de tiempos ociosos respecto a M con N =' + str(n))
    ax1.scatter(pstom, arr_m, color='b', label="PSTOM")
    ax1.scatter(pstob, arr_m, color='r', label="PSTOB")
    ax1.set_xlabel('minutos')
    ax1.set_ylabel('Cantidad de operarior Monolingues')
    ax1.legend()

    fig.tight_layout()
    save_STO(fig, n)


def save_STO(pl, n):
    pl.savefig('/home/rott/Escritorio/PSTO' + str(n), format='png')
    pl.clf()  # Clear the figure for the next loop


def save_PTE(pl, n):
    pl.savefig('/home/rott/Escritorio/PTE' + str(n), format='png')
    pl.clf()  # Clear the figure for the next loop


def dibujar_PTE(arr_ptel, arr_ptei, arr_m, n):
    import numpy as np
    import matplotlib.pyplot as plt
    # import matplotlib as mpl

    ptel = np.array(arr_ptel)
    ptei = np.array(arr_ptei)

    # mpl.style.use(sty)

    fig, ax1 = plt.subplots(nrows=1, sharex=True)
    ax1.set_title(
        'Variacion de tiempo de espera respecto a M con N =' + str(n))
    ax1.scatter(ptel, arr_m, color='r', label="PTEL")
    ax1.set_ylabel('Cantidad de operarios monolingues')
    ax1.set_xlabel('minutos')
    ax1.scatter(ptei, arr_m, color='b', label="PTEI")

    ax1.plot([15, 15], [0, 15], color='g',
             lw=2, label="Maxima expera 15'")
    ax1.legend()

    fig.tight_layout()
    save_PTE(fig, n)


def gen_IAI():
    global IAI

    R = random.uniform(0, 1)
    IAI = -4 * log(1 - R)


def gen_IAL():
    global IAL
    accepted = False

    while not accepted:
        M = 0.375

        R1 = random.uniform(0, 1)
        R2 = random.uniform(0, 1)

        x = 4 * R1
        y = M * R2

        fx = -(3.0 / 32) * (x**2 - 4 * x)

        accepted = (y <= fx)

    IAL = x


def gen_TA():
    global TA

    R = random.uniform(0, 1)

    TA = sqrt(400 * R) + 10


def condiciones_iniciales(M, N):
    global STOM, TCM, STOB, TCB, T, TPL, TPI, STEI, STEL, NLI, NLL

    STOM = [0] * M
    TCM = [0] * M
    STOB = [0] * N
    TCB = [0] * N

    T = TPL = TPI = 0
    STEI = STEL = 0
    NLI = NLL = 0

TF = 10000
M_ARR = range(11, 15)
N_ARR = range(7, 10)
resultados = {}

for M in M_ARR:
    for N in N_ARR:

        condiciones_iniciales(M, N)

        while T < TF:
            if TPI < TPL:
                T = TPI
                gen_IAI()
                TPI = T + IAI
                gen_TA()
                j = TCB.index(min(TCB))
                if T < TCB[j]:
                    STEI = STEI + TCB[j] - T
                    TCB[j] = TCB[j] + TA
                else:
                    STOB[j] = STOB[j] + T - TCB[j]
                    TCB[j] = T + TA
                NLI = NLI + 1
            else:
                T = TPL
                gen_IAL()
                TPL = T + IAL
                gen_TA()
                min_com = min(TCM)
                i = TCM.index(min(TCM))
                if T < TCM[i]:
                    min_tcb = min(TCB)
                    ind = TCB.index(min(TCB))
                    if TCB[ind] < TCM[i]:
                        if T < TCB[ind]:
                            STEL = STEL + min_tcb - T
                            TCB[ind] = TCB[ind] + TA
                        else:
                            STOB[ind] = STOB[ind] + T - TCB[ind]
                            TCB[ind] = T + TA
                    else:
                        STEL = STEL + TCM[i] - T
                        TCM[i] = TCM[i] + TA
                else:
                    STOM[i] = STOM[i] + T - TCM[i]
                    TCM[i] = T + TA
                NLL = NLL + 1
        VTOB = []
        for x in range(0, N - 1):
            res = STOB[x] * 100 / T
            VTOB.append(res)

          #  print("Ocio puesto bilingüe %d: %d%%" % (i, res))
        VTOM = []
        for y in range(0, M - 1):
            res = STOM[y] * 100 / T
            VTOM.append(res)
         #   print("Ocio puesto monolingüe %d: %d%%" % (i, STOM[i] * 100 / T))

        PTEL = STEL / NLL
        PTEI = STEI / NLI
        # print "Para %d operadores monolingües y %d operadores bilingües, los
        # clientes locales esperaron en promedio %d minutos y los
        # internacionales %d minutos" % (M, N, PTEL, PTEI)
        resultados[M, N] = {}
        resultados[M, N] = {'M': M, 'N': N, 'PTEI': int(PTEI),
                            'PTEL': int(PTEL), 'VTOM': VTOM, 'VTOB': VTOB}
dibujar()

# """
# =============
# Unit handling
# =============

# basic_units is a mockup of a true units package used for testing
# purposed, which illustrates the basic interface that a units package
# must provide to matplotlib.

# The example below shows support for unit conversions over masked
# arrays.
# """
