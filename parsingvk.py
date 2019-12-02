# вся суть будет заключаться в получении ссылки на профиль
# у этого профиля будут браться друзья и друзья друзей
# тоесть по умолчанию степень глубины=2
# в случае если нужна глубина больше
# то степень вложенности задавать самому
import copy
import datetime
import re
from dateutil.relativedelta import relativedelta
import vk_api

login, password = '79169686822', 'bios88005553535bios'
vk_session = vk_api.VkApi(login, password)

try:
    vk_session.auth(token_only=True)
except:
    print(vk_api.AuthError)

vk = vk_session.get_api()



#для того чела что мы изучаем берем все данные о его друзьях с нужной степенью вложенности
def testinguser(link,level):
    listfrend = {}
    # спискок с дружескими отношениями
    listfrendnet = []
    domain = link.split('/')[-1]
    aboutuser=vk.users.get(user_ids=domain,fields='city,education,bdate')[0]
    list_field=[]
    f={}
    # f['id']=aboutuser['id']
    f['first_name'] = aboutuser['first_name']
    f['last_name'] = aboutuser['last_name']

    if 'city' in aboutuser:
        f['city']=aboutuser['city']['title']
        list_field.append('city')
    if 'bdate' in aboutuser:
        result = re.split(r'\.', aboutuser['bdate'])
        f['bdate']=relativedelta(datetime.date.today(),datetime.date(int(result[2]),int(result[1]),int(result[0]))).years
        list_field.append('bdate')
    if 'university_name' in aboutuser:
        f['university_name']=aboutuser['university_name']
    f['getfriends']=False
    f['is_closed']=aboutuser['is_closed']
    list_field.append('education')
    f['level']=0



    listfrend[aboutuser['id']]=f
# берем всех друзей этого человека
    for m in range(level):
        listfrend2=copy.deepcopy(listfrend)
        for j in listfrend2:

            #проверяем что у этого человека мы друзей еще не собирали и он на нужном уровне в пищевой цепи
            if not listfrend[j]['getfriends'] and not listfrend[j]['is_closed'] and listfrend[j]['level']<level:
                listfrend[j]['getfriends']=True

                friends=vk.friends.get(user_id=j,fields=','.join(list_field) )

                for friend in friends['items']:
                    foo={}
                    listfrendnet.append([j,friend['id'],1])
                    foo['level']=listfrend[j]['level']+1
                    if 'is_closed' in friend:
                        foo['is_closed']=friend['is_closed']
                    else:
                        foo['is_closed'] =True
                    # foo['id'] = friend['id']
                    foo['first_name'] = friend['first_name']
                    foo['last_name'] = friend['last_name']
                    if 'city' in list_field:
                        if 'city' in friend :
                            foo['city'] = aboutuser['city']['title']
                            list_field.append('city')
                        else:
                            foo['city'] ='Upiter'
                    if 'city' in list_field:
                        if 'bdate' in friend:
                            result = re.split(r'\.', aboutuser['bdate'])
                            foo['bdate'] = relativedelta(datetime.date.today(),
                             datetime.date(int(result[2]), int(result[1]), int(result[0]))).years
                            list_field.append('bdate')
                        else:
                            foo['bdate'] = 2000
                    if 'city' in list_field:
                        if 'university_name' in friend:
                            foo['university_name'] = aboutuser['university_name']
                            list_field.append('education')
                        else:
                            foo['university_name'] ='Kakashka'
                    foo['getfriends']=False
                    listfrend[friend['id']]=foo
    return listfrend, listfrendnet














