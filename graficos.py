import numpy as np
import matplotlib.pyplot as plt

I_SC=13.79 
Vdc=49.34
Vmp=40.66
TC=0.0028

def celula_irradiancia_variando(I_SC, Vdc, Vmp, TC):
    # Constantes globais
    q = 1.60217662e-19  # Carga elementar (em Coulombs)
    k = 1.38064852e-23  # Constante de Boltzmann (em J/K)
    n = 1.4  # Fator de idealidade

    # Variáveis
    T = 298.15  # Temperatura da célula (em Kelvin)
    I_r = np.arange(200, 1001, 200)  # irradiância (de 200 a 1000 com step de 200)
    V = np.linspace(0, Vmp / Vdc, 35)  # Tensão como variável de entrada

    T_0 = 298.15  # Temperatura de referência (25°C em Kelvin)
    I_r0 = 1000  # Irradiância de referência (em W/m²)
    V_OC = 0.721  # Tensão de circuito aberto de referência (em Volts)
    V_g = 1.79e-19  # Bandgap em Joules
    I_s0 = 1.2799e-8  # Corrente de saturação na temperatura de referência

    # Criando a malha para tensão e irradiância
    V_m, I_rm = np.meshgrid(V, I_r)

    # Equações baseadas no artigo referenciado
    I_ph = ((I_SC / I_r0) * I_rm) * (1 + TC * (T - T_0))  # Fotocorrente
    I_s = I_s0 * (T / T_0)**(3 / n) * np.exp((-(q * V_g) / (n * k)) * ((1 / T) - (1 / T_0)))  # Corrente de saturação
    I = I_ph - I_s * np.exp(((q * V_m) / (n * k * T)) - 1)  # Corrente total
    P = I * V_m  # Potência

    # Evitando valores inconsistentes
    Iplot = np.where(I < 0, np.nan, I)
    Pplot = np.where(P < 0, np.nan, P)

    # Gráficos
    plt.figure(1)
    for i in range(len(I_r)):
        plt.plot(V, Iplot[i, :], label=f'I_r = {I_r[i]} W/m²')
    plt.xlabel('Tensão (V)')
    plt.ylabel('Corrente (I)')
    plt.title('Curva I-V')
    plt.legend()
    plt.grid(True)

    plt.figure(2)
    for i in range(len(I_r)):
        plt.plot(V, Pplot[i, :], label=f'I_r = {I_r[i]} W/m²')
    plt.xlabel('Tensão (V)')
    plt.ylabel('Potência (P)')
    plt.title('Curva P-V')
    plt.legend()
    plt.grid(True)

   

def celula_temperatura_variando(I_SC, Vdc, Vmp, TC):
    # Constantes
    q = 1.60217662e-19  # Carga elementar (C)
    k = 1.38064852e-23  # Constante de Boltzmann (J/K)
    n = 1.4  # Fator de idealidade
    I_r = 800  # Irradiância fixa (W/m²)
    T_0 = 298.15  # Temperatura de referência (K)
    V_OC = 0.721  # Tensão de circuito aberto (V)
    V_g = 1.79e-19  # Bandgap em Joules

    # Tensão como variável de entrada
    V = np.linspace(0, Vmp / Vdc, 35)

    # Intervalo de temperaturas (298.15 K a 338.15 K em passos de 10 K)
    temperatures = np.arange(298.15, 338.15 + 1, 10)

    # Matrizes para armazenar os resultados
    Iplot2 = np.zeros((len(temperatures), len(V)))
    Pplot2 = np.zeros((len(temperatures), len(V)))

    # Loop sobre as temperaturas
    for i, T in enumerate(temperatures):
        I_s0 = 1.2799e-8  # Corrente de saturação na temperatura de referência
        I_ph = ((I_SC / I_r) * I_r) * (1 + TC * (T - T_0))  # Fotocorrente
        I_s = I_s0 * (T / T_0)**(3 / n) * np.exp((-(q * V_g) / (n * k)) * ((1 / T) - (1 / T_0)))  # Corrente de saturação
        I = I_ph - I_s * np.exp(((q * V) / (n * k * T)) - 1)  # Corrente total
        P = I * V  # Potência

        # Tratando valores inconsistentes
        Iplot3 = np.where(I < 0, np.nan, I)
        Pplot3 = np.where(P < 0, np.nan, P)

        # Salvando os resultados
        Iplot2[i, :] = Iplot3
        Pplot2[i, :] = Pplot3

    # Plotando as curvas de corrente
    plt.figure(3)
    for i, T in enumerate(temperatures):
        plt.plot(V, Iplot2[i, :], label=f'T = {T:.2f} K')
    plt.xlabel('Tensão (V)')
    plt.ylabel('Corrente (I)')
    plt.title('Variação da Corrente com a Temperatura')
    plt.legend()
    plt.grid(True)

    # Plotando as curvas de potência
    plt.figure(4)
    for i, T in enumerate(temperatures):
        plt.plot(V, Pplot2[i, :], label=f'T = {T:.2f} K')
    plt.xlabel('Tensão (V)')
    plt.ylabel('Potência (P)')
    plt.title('Variação da Potência com a Temperatura')
    plt.legend()
    plt.grid(True)
   

celula_irradiancia_variando(I_SC, Vdc, Vmp, TC)
celula_temperatura_variando(I_SC, Vdc, Vmp, TC)

# Mostrando os gráficos
plt.show()