# файл подготовки обучающих данных
# по сути просто подсчет коэффициентов

from parsingvk import testinguser
import networkx as nx
from IPython.display import Image
import matplotlib.pyplot as plt
# подготовим данные о связях, заполнив несуществующие связи нулями


# строит сеть по универу - если учатся в одном универе то 1 иначе 0
# строит сеть по возрасту - если разница меньше или равна 5 то 1 иначе 0
# строит сеть по городам - если живут в одном городе то 1 иначе 0
def createuniveragecitynet(a,listfrend):
    for i in a:
        if listfrend[i[0]]['university_name']==listfrend[i[1]]['university_name']:
            #если универы совпадают пишем 1в шестое поле
            i[5]=1
        if abs(listfrend[i[0]]['bdate']-listfrend[i[1]]['bdate'])<=5:
            #если разница в возрасте не более 5 лет
            i[3]=1
        if listfrend[i[0]]['city'] == listfrend[i[1]]['city']:
            # если города совпадают пишем 1в шестое поле
            i[4] = 1
    return a

#создаем все возможные пары а не только те что создались по дружеским парам
def createmissingpairs(a,listfrend,listfrendnet):
    #пробегаем по всем возможным вершинам и создаем все возможные связи, условие нужно чтобы не было повторяющихся пар
    a = [[i, j,0,0,0,0] for i in listfrend.keys() for j in listfrend.keys() if i>j]
    #если такая дружеская связь существует то выставим третьим аргументом 1
    for i in a:
        if [i[0],i[1],1] in listfrendnet or [i[1],i[0],1] in listfrendnet:
            i[2]=1
    return a





# создание итоговой выборки для обучения
# [вершина1, вершина2, коэф1_друзья, коэф2_друзья,коэф3_друзья,коэф1_возраст, коэф2_возраст, коэф3_возраст, коэф1_город,коэф2_город, коэф3_город, коэф1_универ, коэф2_универ, коэф3_универ ]
def createleninglist(link, level):
    haveallnat = []
    a,b=testinguser(link, level)
    # здесь имеем все текущие параметры которые теперь надо превратить в коэффициенты
    return createuniveragecitynet(createmissingpairs(haveallnat,a,b),a)

    # получаем коэффициенты по возрасту
    # получаем коэффициенты по городу
    # получаем коэффициенты по универу




