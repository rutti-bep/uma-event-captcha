
#TODO DBを受け取り照合、出力する

"""
def eventsearch(eventName):
    print(eventName)
    f = open('uma_event_datas.js', 'r',encoding='utf-8')
    #w = open('uma_event.json','w',encoding='utf-8')
    event_datas = f.read().split(';',2)[0].split('\n',2)[2].rsplit('\n',2)[0].rsplit(',',1)[0].replace('\'','\"').replace(',]',']').replace(',}','}').replace('[br]','').split('\n')
    #w.write(event_datas)
    #w.close()
    f.close()

    ary = [];
    for s in event_datas:
        try:
            event = json.loads(s.rsplit(',',1)[0])
            #print(event)
            if eventName in event['e']:
                 print('match:',event['choices'])
                 ary += [event]
        except Exception as e:
            print(e)
            #print('err',s)

    print(ary)
"""