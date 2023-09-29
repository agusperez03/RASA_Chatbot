"""
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_graphviz

from sklearn import tree

# Obtenemos el dataset a entrenar
nombre_archivo = 'c:/Users/Usuario/ChatBotNetflix/decisionTree.csv'

df = pd.read_csv(nombre_archivo)
#df = df.drop(columns=['Unnamed: 0']) 

print(df)

# Imprimimos 5 filas aleatorias
print("5 EJEMPLOS DE LOS DATOS....................................................")
print(df.sample(5))
print("INFORMACIÓN DEL DATASET....................................................")
print(df.info())


# convertimos las variables categóricas en one-hot encoding
df = pd.get_dummies(data=df, drop_first=True)

# Imprimimos 5 filas aleatorias
print("5 EJEMPLOS CON FORMATO ONE-HOT....................................................")
print(df.sample(5))

# Separamos las features y el target
x = df.drop(columns='')     # features
y = df['']                  #target

print("DATASET DE LOS FEATURES....................................................")
print(x.info())
"""