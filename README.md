# # Pricing d'Option Asiatique : Arbre Non-Recombinant
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Finance](https://img.shields.io/badge/Finance-Derivatives-green)
![Status](https://img.shields.io/badge/Status-Educational-orange)

## 📋 Description

- implémentation numérique de l'exemple 8.1 du livre **Binomial Models in Finance** afin d'ilustrer la problématiques des arbres non-recombinant 

## 🎯 Objectifs

- Estimer le prix d'un **call asiatique** dont le payoff est donné par : 
```math
$$
\text{Payoff} = \max\left(\bar{S} - K,\, 0\right)\: avec \: \bar{S} = \frac{1}{N + 1} \sum_{k=0}^{N} S_k
$$
```

- Comprendre l'inefficacité de l'arbre binomial non recombinant en mesurant l'impact de la complexité en $$\mathcal{O}(2^N)$$ sur le temps d'exécution pour différentes valeurs de $$N$$.

## 🔧 Méthodologie

- L'évaluation du prix repose sur le **modèle CRR** avec un arbre non recombinant. Pour $$N = 4$$, il y a $$2^N = 16$$ chemins distincts, chacun correspondant à une combinaison de hausse et de baisse.

- Nous reprenons les valeurs numériques de l'exemple 8.1 du livre :
```math
$$
S_0 = 100,\quad K = 100,\quad r = 0.05,\quad \sigma = 0.2,\quad T = 1,\quad N = 4
$$
``` 

- Les paramètres du modèle sont les suivants :
```math
$$
\delta_t = \frac{T}{N}, \quad h = \exp(\sigma \sqrt{\delta_t}), \quad b = \frac{1}{h}, \quad R = \exp(r\delta_t), \quad \mathbb{Q} = \frac{R-b}{h-b}
$$
```



## 📚 Références

- Hoek, J. van der, & Elliott, R. J. (2006). *Binomial Models in Finance*. Springer Finance

## 👤 Auteur

Alexandre R. - Master mathématiques appliquées -  Université Paris Cité

