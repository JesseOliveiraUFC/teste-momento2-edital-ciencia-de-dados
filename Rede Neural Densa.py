import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import keras
from keras.models import Sequential
from keras.layers import Dense

#Leitura dos dados
data = pd.read_csv("dataset_teste_selecao.csv",encoding = "cp860")

#Organização dos dados da Planílha
data = data.replace({"Nπo":0, "Sim":1})
data = data.replace({"MACRORREGI├O DE SA┌DE - FORTALEZA":"Fortaleza",
                     "MACRORREGI├O DE SA┌DE - SERT├O CENTRAL":"Sertão Central",
                     "MACRORREGI├O DE SA┌DE - LITORAL LESTE /JAGUARIBE":"Litoral Leste",
                     "MACRORREGI├O DE SA┌DE - SOBRAL":"Sobral"})
data = data.replace({"Nπo informado":"Não Informado", "Vi·vo":"Viúvo"})

#Organização dos dados por Sintomas
sintomas = data[["coriza","tosse_seca_ou_produtiva","calafrios","febre",
                "dispneia","fadiga","anorexia","mialgia","astenia",
                 "dor_de_garganta","congestao_nasal","cefaleia","diarreia",
                 "nausea","vomitos","anosmia","ageusia","tipo_caso_α_admissπo"]]
sintclasse = sintomas["tipo_caso_α_admissπo"]
sintclasse = sintclasse.replace({"Caso suspeito":0,"Caso confirmado":1})
sintprev = sintomas.drop("tipo_caso_α_admissπo", axis = 1)

#Exportação dos dados de teste e treinamento
prev_train, prev_test, class_train, class_test = train_test_split(sintprev, sintclasse, test_size=0.2)
prev_train.to_csv("Prev_train.csv", index=False)
class_train.to_csv("Class_train.csv", index=False)
prev_test.to_csv("Prev_test.csv", index=False)
class_test.to_csv("Class_test.csv", index=False)

#Construção da Rede Neural Densa para prever se é Covid ou é só suspeita
prev_train, prev_test, class_train, class_test = train_test_split(sintprev, sintclasse, test_size=0.2)

clf = Sequential()  #Rede Neural com duas camadas ocultas
clf.add(Dense(units=16, activation="relu", 
        kernel_initializer="random_uniform", input_dim=17))
clf.add(Dense(units=16, activation="relu", 
        kernel_initializer="random_uniform"))
clf.add(Dense(units=1, activation="sigmoid"))
                    #Compilação e Fitting da Rede Neural
clf.compile(optimizer="adam", loss='binary_crossentropy',
            metrics=["binary_accuracy"])
clf.fit(prev_train, class_train, batch_size=(10), epochs=1000)
                    #Prevendo os dados de teste
prev = clf.predict(prev_test)
prev = (prev > 0.5)
                    #Comparando os dados previstos com a classe de testes
precision = accuracy_score(class_test, prev)
                    #Exportação dos valor da precisão da Rede Neural
precision = accuracy_score(class_test, prev)
with open("Precisão da Rede Neural.txt", "w") as arq:
    arq.write(str(precision))

