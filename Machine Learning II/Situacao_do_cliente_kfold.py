#!-*- coding: utf8 -*-
import pandas as pd
from collections import Counter
import numpy as np
from sklearn.cross_validation import cross_val_score

df = pd.read_csv("situacao_do_cliente.csv")

X_df = df[['recencia','frequencia','semanas_de_inscricao']]
Y_df = df['situacao']

Xdummies_df = pd.get_dummies(X_df)
Ydummies_df = Y_df

X = Xdummies_df.values
Y = Ydummies_df.values

porcentagem_treino = 0.8

tamanho_de_treino = int(porcentagem_treino * len(Y))

#tamanho_de_validacao = len(Y) - tamanho_de_treino

treino_dados = X[:tamanho_de_treino]
treino_marcacoes = Y[:tamanho_de_treino]

validacao_dados = X[tamanho_de_treino:]
validacao_marcacoes = Y[tamanho_de_treino:]


def fit_and_predict(nome, modelo, treino_dados, treino_marcacoes):
	k = 10
	scores = cross_val_score(modelo, treino_dados, treino_marcacoes, cv = k)
	taxa_de_acerto = np.mean(scores)
	msg = "Taxa de acerto {0}: {1}".format(nome, taxa_de_acerto)
	print (msg)
	return taxa_de_acerto

resultados = {}

from sklearn.naive_bayes import MultinomialNB
modeloMultinomial = MultinomialNB()
resultadoMultinomial = fit_and_predict("MultinomialNB", modeloMultinomial, treino_dados, treino_marcacoes)	
resultados[resultadoMultinomial] = modeloMultinomial

from sklearn.ensemble import AdaBoostClassifier
modeloAdaBoost = AdaBoostClassifier()
resultadoAdaBoost = fit_and_predict("AdaBoostClassifier", modeloAdaBoost, treino_dados, treino_marcacoes)	
resultados[resultadoAdaBoost] = modeloAdaBoost

from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
modeloOneVsRest = OneVsRestClassifier(LinearSVC(random_state = 0))
resultadoOneVsRest = fit_and_predict("OneVsRest", modeloOneVsRest, treino_dados, treino_marcacoes)
resultados[resultadoOneVsRest] = modeloOneVsRest

from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC
modeloOneVsOne = OneVsOneClassifier(LinearSVC(random_state = 0))
resultadoOneVsOne = fit_and_predict("OneVsOne", modeloOneVsOne, treino_dados, treino_marcacoes)
resultados[resultadoOneVsOne] = modeloOneVsOne

maximo = max(resultados)
vencedor = resultados[maximo]
vencedor.fit(treino_dados, treino_marcacoes)
resultado = vencedor.predict(validacao_dados)
acertos = (resultado == validacao_marcacoes)
total_de_acertos = sum(acertos)
total_de_elementos = len(validacao_dados)
taxa_de_acerto = 100.0 * total_de_acertos/total_de_elementos

acerto_base = max(Counter(Y).values())
taxa_de_acerto_base = 100.0 * acerto_base/len(Y)

msg = "Taxa de acerto no mundo real: {0}".format(taxa_de_acerto)
print(msg)


acerto_base = max(Counter(validacao_marcacoes).values())
taxa_de_acerto_base = 100.0 * acerto_base/len(validacao_marcacoes)
print("Taxa de acerto base: %f" % taxa_de_acerto_base)
print("Total de elementos: %d" % len(teste_dados))