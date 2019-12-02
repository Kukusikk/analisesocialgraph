import numpy as np
import random
import networkx as nx
from IPython.display import Image
import matplotlib.pyplot as plt



# Load the graph
G_karate = nx.karate_club_graph()
# Find key-values for the graph
pos = nx.spring_layout(G_karate)
# Plot the graph
nx.draw(G_karate, cmap = plt.get_cmap('rainbowv '), with_labels=True, pos=pos)
# plt.show()
n = G_karate.number_of_nodes ()
m = G_karate.number_of_edges ()


# Возьмите случайную выборку ребер
edge_subset = random.sample (G_karate.edges (), int(0.25 * m))
G_karate_train = G_karate.copy ()
G_karate_train.remove_edges_from (edge_subset)


prediction_jaccard = list(nx.jaccard_coefficient(G_karate_train))
prediction_pref = list(nx.preferential_attachment(G_karate_train))
prediction_adamic = list(nx.adamic_adar_index(G_karate_train))

#сформируем итоговую выборку
leninglist=[]
jaccard=pref=adamic=0
for i in prediction_jaccard:
    jaccard = i[2]
    if (i[0],i[1]) in G_karate.edges:
        k=1
    else:
        k=0


    for j in prediction_pref:
        if i[0]==j[0] and i[1]==j[1]:
            pref=j[2]
    for j in prediction_adamic:
        if i[0]==j[0] and i[1]==j[1]:
            adamic=j[2]
    leninglist.append([i[0],i[1],jaccard,pref,adamic,k ])

print(leninglist)

import pandas


dataset=pandas.DataFrame(leninglist)

x = dataset.iloc[:,2:5].values
y = dataset.iloc[:,5:].values



from sklearn import preprocessing
# normalize the data attributes
# normalized_X = preprocessing.normalize(x)
# standardize the data attributes
# standardized_X = preprocessing.scale(x)


from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
# обучение
model.fit(x, y)

# make predictions
# expected = y


def test_model(priznak):
    return model.predict(priznak)



print(test_model([ [0.36363636363636365, 41, 3.3477309568485394]]))
print(test_model([ [0.39, 41, 3.3477309568485394]]))
print(test_model([ [0.36363636363636365, 41, 0]]))
print(test_model([ [0.9, 41, 99]]))
print(test_model([ [0.7, 41, 959]]))

