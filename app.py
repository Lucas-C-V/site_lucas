from flask import Flask, request, jsonify, send_from_directory
import os
import numpy as np
import matplotlib.pyplot as plt

# Configuração da aplicação Flask
site = Flask(__name__)
site.config['UPLOAD_FOLDER'] = 'static/graphs'

# Certifique-se de que o diretório para salvar gráficos existe
os.makedirs(site.config['UPLOAD_FOLDER'], exist_ok=True)

# Funções de geração de gráficos (sem alterações aqui)
def celula_irradiancia_variando(I_SC, Vdc, Vmp, TC, folder):
    q = 1.60217662e-19
    k = 1.38064852e-23
    n = 1.4
    T = 298.15
    I_r = np.arange(200, 1001, 200)
    V = np.linspace(0, Vmp / Vdc, 35)
    T_0 = 298.15
    I_r0 = 1000
    V_OC = 0.721
    V_g = 1.79e-19
    I_s0 = 1.2799e-8
    V_m, I_rm = np.meshgrid(V, I_r)
    I_ph = ((I_SC / I_r0) * I_rm) * (1 + TC * (T - T_0))
    I_s = I_s0 * (T / T_0)**(3 / n) * np.exp((-(q * V_g) / (n * k)) * ((1 / T) - (1 / T_0)))
    I = I_ph - I_s * np.exp(((q * V_m) / (n * k * T)) - 1)
    P = I * V_m
    Iplot = np.where(I < 0, np.nan, I)
    Pplot = np.where(P < 0, np.nan, P)

    plt.figure(1)
    for i in range(len(I_r)):
        plt.plot(V, Iplot[i, :], label=f'I_r = {I_r[i]} W/m²')
    plt.xlabel('Tensão (V)')
    plt.ylabel('Corrente (I)')
    plt.title('Curva I-V')
    plt.legend()
    plt.grid(True)
    iv_path = os.path.join(folder, "iv_graph.png")
    plt.savefig(iv_path)
    plt.close()

    plt.figure(2)
    for i in range(len(I_r)):
        plt.plot(V, Pplot[i, :], label=f'I_r = {I_r[i]} W/m²')
    plt.xlabel('Tensão (V)')
    plt.ylabel('Potência (P)')
    plt.title('Curva P-V')
    plt.legend()
    plt.grid(True)
    pv_path = os.path.join(folder, "pv_graph.png")
    plt.savefig(pv_path)
    plt.close()

    return [iv_path, pv_path]

# Rota para servir o index.html diretamente
@site.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Rota para gerar os gráficos
@site.route('/generate_graphs', methods=['POST'])
def generate_graphs():
    I_SC = float(request.form['I_SC'])
    TC = float(request.form['TC'])
    Vdc = float(request.form['Vdc'])
    Vmp = float(request.form['Vmp'])

    folder = site.config['UPLOAD_FOLDER']
    graph_paths = celula_irradiancia_variando(I_SC, Vdc, Vmp, TC, folder)

    return jsonify(graph_paths)

if __name__ == '__main__':
    site.run(debug=True)
