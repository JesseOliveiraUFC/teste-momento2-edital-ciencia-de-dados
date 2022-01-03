import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Leitura dos dados
data = pd.read_csv("dataset_teste_selecao.csv",encoding = "cp860")

#Organização dos dados da Planílha
data = data.replace({"Nπo":0, "Sim":1})
data = data.replace({"MACRORREGI├O DE SA┌DE - FORTALEZA":"Fortaleza",
                     "MACRORREGI├O DE SA┌DE - SERT├O CENTRAL":"Sertão Central",
                     "MACRORREGI├O DE SA┌DE - LITORAL LESTE /JAGUARIBE":"Litoral Leste",
                     "MACRORREGI├O DE SA┌DE - SOBRAL":"Sobral"})
data = data.replace({"Nπo informado":"Não Informado", "Vi·vo":"Viúvo"})

#Organização dos dados de mortes
nDeath = data[["idade","desfecho"]].dropna()
nDeath = nDeath.replace({"alta":0, "obito":1})
for i in nDeath.index:
    if nDeath["desfecho"][i] == 0:
        nDeath = nDeath.drop(i, axis = 0)      
nDeath = nDeath.drop("desfecho", axis = 1)

#Visualização dos Dados
#Histogramas Multiplots 
plt.figure(figsize=(12,3),dpi=200)
plt.subplot(1,2,1)
plt.hist(data["idade"], bins = 14, color="green")
plt.title("Casos de Infecção e Número de Mortes")
plt.ylabel("Quantidade de Pessoas")
plt.xlabel("Idade")
plt.subplot(1,2,1)
plt.hist(nDeath["idade"], bins = 14, color="blue")
plt.text(18, 76, "* Casos Registrados", color="green")
plt.text(18, 70, "* Mortes Confirmadas", color="blue")
plt.show()

#Organização dos dados por Comorbidades
comorb = data[["diabetes","obesidade","hipertensao_arterial","doenca_cardiaca",
               "doenca_pulmonar","doenca_reumatologica","doenca_autoimune",
               "doenca_renal_cronica","doenca_hepatica_cronica",
               "desfecho"]].dropna()
desfecho = pd.DataFrame(comorb["desfecho"])
desfecho = desfecho.replace({"alta":"Alta","obito":"Óbito"})

#Organização dos dados para serem plotados
comorbSum = [0]*553
for i in comorb:
    if i!= "desfecho":
        comorbSum = comorbSum + comorb[i]
comorbSum = pd.DataFrame(comorbSum > 0).astype(int).rename(columns={0:"comorbidades","desfecho":"Desfecho"})
comorbSum = comorbSum.replace({0:"Não",1:"Sim"})
#comorbSum = pd.DataFrame(comorbSum).rename(columns={0:"comorbidades"})
comorbSum = comorbSum.join(desfecho)
#Plot dos dados por comorbidades
plt.figure(figsize=(5,3),dpi=200)
sns.countplot("comorbidades", hue="desfecho", data=comorbSum)
plt.ylabel("Quantidade de Pessoas")
plt.xlabel("Possui Comorbidades")

#plot dos dados sobre os tipos de comorbidades
comorb = comorb.replace({0:"Não",1:"Sim","obito":"Óbito","alta":"Alta"})
plt.figure(figsize=(9,9),dpi=200)
plt.subplot(3,3,1)
sns.countplot("diabetes", hue=("desfecho"), data=comorb, order={"Não","Sim"})
plt.ylabel("Número de Pessoas")
plt.xlabel("Diabetes")
plt.subplot(3,3,2)
sns.countplot("obesidade", hue=("desfecho"), data=comorb, order={"Não","Sim"})
plt.ylabel("Número de Pessoas")
plt.xlabel("Obesidade")
plt.subplot(3,3,3)
sns.countplot("hipertensao_arterial", hue=("desfecho"), data=comorb, order={"Não","Sim"})
plt.ylabel("Número de Pessoas")
plt.xlabel("Hipertensão Arterial")
plt.subplot(3,3,4)
sns.countplot("doenca_cardiaca", hue=("desfecho"), data=comorb, order={"Não","Sim"})
plt.ylabel("Número de Pessoas")
plt.xlabel("Doença Cardíaca")
plt.subplot(3,3,5)
sns.countplot("doenca_pulmonar", hue=("desfecho"), data=comorb, order={"Não","Sim"})
plt.ylabel("Número de Pessoas")
plt.xlabel("Doença Pulmonar")
plt.subplot(3,3,6)
sns.countplot("doenca_reumatologica", hue=("desfecho"), data=comorb, order={"Não","Sim"})
plt.ylabel("Número de Pessoas")
plt.xlabel("Doença Reumatológica")
plt.subplot(3,3,7)
sns.countplot("doenca_autoimune", hue=("desfecho"), data=comorb, order={"Não","Sim"})
plt.ylabel("Número de Pessoas")
plt.xlabel("Doença Autoimune")
plt.subplot(3,3,8)
sns.countplot("doenca_renal_cronica", hue=("desfecho"), data=comorb, order={"Não","Sim"})
plt.ylabel("Número de Pessoas")
plt.xlabel("Doença Renal Crônica")
plt.subplot(3,3,9)
sns.countplot("doenca_hepatica_cronica", hue=("desfecho"), data=comorb, order={"Não","Sim"})
plt.ylabel("Número de Pessoas")
plt.xlabel("Doença Hepática Crônica")
plt.tight_layout()

#Organização dos dados por Estilo de Vida
lifeStl = data[["tabagismo","drogas","etilismo","desfecho"]]
#IMPORTANTE!!!
#Os dados sobre estilo de vida são INCONCLUSIVOS
