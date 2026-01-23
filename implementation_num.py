# ============================================================================
# 1 IMPORTS
# ============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import itertools

# ============================================================================
# 2 PARAMÈTRES DU MODÈLE
# ============================================================================

#on utilise les mêmes paramètres que dans l'exemple du chapitre 8 

S0 = 100
K = 100
r = 0.05
sigma = 0.2
T = 1
N = 4
N2 = [4,6,8,10,12,14,16,18,20]  # différentes valeurs de N pour les tests
delta_t = T / N
u = np.exp(sigma * np.sqrt(delta_t))
d = 1 / u
R = np.exp(r * delta_t)
p = (R - d) / (u - d)

# ============================================================================
# 3 GENERATION DES CHEMINS ET CALCUL DES PRIX
# ============================================================================

#fonction qui génère tous les chemins possibles de l'arbre binomial non recombinant
def paths_generate(N):
    # Génère toutes les combinaisons possibles de 0 et 1 sur N périodes
    paths = list(itertools.product([0, 1], repeat=N))
    # Convertit en array numpy
    return np.array(paths)

#fonction qui calcule les prix pour un chemin donné
def path_prices(path, S0, u, d):
    prices = np.zeros(len(path) + 1)  # vecteur de taille N+1 pour inclure le temps 0
    prices[0] = S0  # prix initial
    for i in range(len(path)):
        if path[i] == 1:
            # si hausse on multiplie par u
            prices[i + 1] = prices[i] * u
        else:
            # si baisse on multiplie par d
            prices[i + 1] = prices[i] * d
    return prices



# ============================================================================
# 4 PRICING DE L'OPTION ASIATIQUE
# ============================================================================


def asian_payoff(path, S0, u, d, K):
    prices = path_prices(path, S0, u, d)
    S_bar = np.mean(prices)  # prix moyen le long du chemin
    return max(S_bar - K, 0)  # payoff du call asiatique


def price_and_time_asian(N, S0, K, r, sigma, T):
    # Calcul des paramètres
    delta_t = T / N
    u = np.exp(sigma * np.sqrt(delta_t))  
    d = 1 / u  
    R = np.exp(r * delta_t)
    Q = (R - d) / (u - d)  # probabilité risque-neutre
    
    # On lance le chrono
    t0 = time.time()
    
    # On génère les chemins
    paths = paths_generate(N)
    
    # Pour chaque chemin on calcule le payoff
    payoffs = np.array([asian_payoff(paths[i], S0, u, d, K) for i in range(len(paths))])
    
    # On calcule pour chaque chemin la proba sous Q
    probas = np.zeros(len(paths))
    for i in range(len(paths)):
        up = np.sum(paths[i])  # nombre de 1 (hausses)
        down = len(paths[i]) - up  # nombre de 0 (baisses)
        probas[i] = Q**up * (1 - Q)**down
    
    # Le prix = espérance du payoff actualisé
    price = np.exp(-r * T) * np.sum(payoffs * probas)
    
    # On arrête le chrono
    t1 = time.time()
    
    return {
        'N': N,
        'Price': price,
        'Time': t1 - t0,
        'Paths': len(paths)
    }

def main():
    # ============================================================================
    # 5 DATAFRAME DES PRIX 
    # ============================================================================

    # Calcul des résultats pour différentes valeurs de N
    results = []
    for Na in N2:
        result = price_and_time_asian(Na, S0, K, r, sigma, T)
        results.append({
            'Type': 'Call asiatique',
            'Strike': 'ATM',
            'N': result['N'],
            'Paths': result['Paths'],
            'Price': result['Price'],
            'Time': result['Time']
        })

    asian_option_dataframe = pd.DataFrame(results)

    # ============================================================================
    # 5 VISUALISATION DE L'ARBRE
    # ============================================================================


    paths = paths_generate(N) 
    M = len(paths)  # 2^N chemins

    # Calcul des prix pour tous les chemins en utilisant la fonction path_prices
    prix = np.zeros((M, N + 1))
    for i in range(M):
        prix[i, :] = path_prices(paths[i], S0, u, d)
    print("\n----affichage de l'arbre des prix----")
    # Affichage graphique
    plt.figure(figsize=(12, 8))
    for i in range(M):
        plt.plot(range(N + 1), prix[i, :], 'o-', alpha=0.6, linewidth=1.5)
    plt.xlabel('Période')
    plt.xticks(range(N + 1))
    plt.ylabel('Prix')
    plt.title(f'Arbre Binomial Non Recombinant ({M} chemins)')
    plt.grid(True, alpha=0.3)
    plt.show()

    # ============================================================================
    # AFFICHAGE DES PRIX ET TEMPS DE CALCUL
    # ============================================================================

    print("\n----Prix et temps de calcul pour différentes valeurs de N----")
    print(asian_option_dataframe)

    # ============================================================================
    # VISUALISATION DU TEMPS DE CALCUL EN FONCTION DE N
    # ============================================================================  

    print("\n----Visualisation du temps de calcul en fonction du nombre de périodes N----")
    plt.figure(figsize=(10, 6))
    plt.plot(asian_option_dataframe['N'], asian_option_dataframe['Time'], marker='o', linewidth=2, markersize=8)
    plt.xlabel('Nombre de périodes N', fontsize=12)
    plt.ylabel('Temps de calcul (secondes)', fontsize=12)
    plt.title('Croissance exponentielle du temps de calcul', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()





