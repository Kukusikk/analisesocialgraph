
from kookingleningdata import createleninglist
import random
import networkx as nx
from sklearn.linear_model import LogisticRegression
import pandas
from IPython.display import Image
import matplotlib.pyplot as plt
# находить 3 коэффициента по полученной сети - коэффициент жакара, Индекс Адамико-Адара, Preferential Attachment
def koefficient(G_karate_train):
    prediction_jaccard = list(nx.jaccard_coefficient(G_karate_train))
    prediction_pref = list(nx.preferential_attachment(G_karate_train))
    prediction_adamic = list(nx.adamic_adar_index(G_karate_train))
#дальше сливаем получившиеся списки
    result=[]
    for edge_jaccard, edge_pref, edge_adamic in zip(prediction_jaccard,prediction_pref,prediction_adamic ):
        result.append([edge_jaccard[0],edge_jaccard[1],edge_jaccard[2],edge_pref[2], edge_adamic[2]])
    return result


# показать как выглядет сеть
def drownetwork(mynetwork):
    # plt.figure()
    oldnetwork = nx.Graph()
    oldnetwork.add_weighted_edges_from([i[:3] for i in mynetwork if i[2] != 0])
    # Find key-values for the graph
    # pos = nx.spring_layout(oldnetwork)
    # Plot the graph
    nx.draw(oldnetwork)
    plt.show()

#соеденить все 4 списка со страшными коэффициентами
def sumlist(l1,l2,l3,l4,allinformation):
    results=[]
    #идем по всем возможным парам
    for onedate in allinformation:
        result=[onedate[0],onedate[1],0,0,0,0,0,0,0,0,0,0,0,0, onedate[2]]
        for friendkoef in l1:
            #кидаем коэффициенты дружеских связей
            if result[0] == friendkoef[0] and result[1] == friendkoef[1]:
                result[2]=friendkoef[2]
                result[3] = friendkoef[3]
                result[4] = friendkoef[4]

        for agekoef in l2:
            # кидаем коэффициенты касаемо возраста
            if result[0]==agekoef[0] and result[1]==agekoef[1]:
                result[5]=agekoef[2]
                result[6]=agekoef[3]
                result[7]=agekoef[4]

        for citykoef in l3:
            # кидаем коэффициенты касаемо города
            if result[0]==citykoef[0] and result[1]==citykoef[1]:
                result[8]=citykoef[2]
                result[9]=citykoef[3]
                result[10]=citykoef[4]

        for univerkoef in l4:
            # кидаем коэффициенты касаемо унверситета
            if result[0]==univerkoef[0] and result[1]==univerkoef[1]:
                result[11]=univerkoef[2]
                result[12]=univerkoef[3]
                result[13]=univerkoef[4]
        results.append(result)
    return results




# создаем обучающую выборку
# возвращаем старую сеть и готовый для обучения датафрейм
def createleningkoefficient(datanow):

#



    # получаем все сети на основе тех параметров
    oldnetwork=nx.Graph()
    oldnetwork.add_weighted_edges_from([i[:3] for i in datanow if i[2]!=0])
    # Возьмите 70% выборку ребер
    oldnetwork70 = nx.Graph()
    oldnetwork70.add_weighted_edges_from([i[:3] for i in datanow[:int(len(datanow)*0.7)] if i[2]!=0])

    networkage=nx.Graph()
    networkage.add_weighted_edges_from([[i[0],i[1], i[3]] for i in datanow if i[3]!=0])
    # Возьмите 70% выборку ребер
    networkage70=nx.Graph()
    networkage70.add_weighted_edges_from([[i[0],i[1], i[3]] for i in datanow[:int(len(datanow)*0.7)] if i[3]!=0])



    networkcity=nx.Graph()
    networkcity.add_weighted_edges_from([[i[0],i[1], i[4]] for i in datanow if i[4]!=0])
    # Возьмите 70% выборку ребер
    networkcity70=nx.Graph()
    networkcity70.add_weighted_edges_from([[i[0],i[1], i[4]] for i in datanow[:int(len(datanow)*0.7)] if i[4]!=0])




    networkuniver=nx.Graph()
    networkuniver.add_weighted_edges_from([[i[0],i[1], i[5]] for i in datanow if i[5]!=0])
    # Возьмите 70% выборку ребер
    networkuniver70 = nx.Graph()
    networkuniver70.add_weighted_edges_from([[i[0], i[1], i[5]] for i in datanow[:int(len(datanow) * 0.7)] if i[5]!=0])



#ищем коэфициенты для этих 4х метрик
    oldnetwork702=koefficient(oldnetwork70)
    networkage702=koefficient(networkage70)
    networkcity702=koefficient(networkcity70)
    networkuniver702=koefficient(networkuniver70)
    # по имеющимся коэффициентам свормируем общий список
    resultleningdate=sumlist(oldnetwork702,networkage702, networkcity702, networkuniver702,datanow)


#ищем коэфициенты для всех данных
    oldnetwork2=koefficient(oldnetwork)
    networkage2=koefficient(networkage)
    networkcity2=koefficient(networkcity)
    networkuniver2=koefficient(networkuniver)
    # по имеющимся коэффициентам свормируем общий список
    resultleningdate2=sumlist(oldnetwork2,networkage2, networkcity2, networkuniver2,datanow)

    return oldnetwork, resultleningdate, resultleningdate2











data=createleninglist('https://vk.com/this_fucking_forest', 2)
# data=[[1,2,1,0,0,1],[3,2,1,1,0,1],[1,5,1,1,1,1],[3,2,1,1,1,1],[3,5,0,0,0,0],[5,6,1,0,1,0]]
# старая сеть и список для обучения
print(len(data))
networkold,leninglist, testinglist=createleningkoefficient(data)


# создание и обучение модели
dataset=pandas.DataFrame(leninglist)
x = dataset.iloc[:,2:14].values
y = dataset.iloc[:,14:].values

model = LogisticRegression()
# обучение
model.fit(x, y)
# здесь модель будет отвечать нам на вопрос - будет ли ребро при данной конфигурации или нет
def test_model(priznak):
    return model.predict(priznak)




networknew=[ [edge[0],edge[1],test_model([edge[2:14]])] for edge in testinglist ]

# построим вторую сеть
p=[[i[0],i[1],i[2][0]] for i in networknew]

drownetwork(p)
drownetwork(data)
print(8)
