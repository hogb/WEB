import os
import sys
from datetime import datetime,timedelta
import pandas as pd
import numpy as np

import time
mst = pd.read_pickle(r"C:\Users\Jinu\PycharmProjects\CYB\BATCH\MST_Batch.pickle")



pg = pd.read_pickle(r'C:/Users/Jinu/PycharmProjects/CYB/JAMU/Source/PLOG_EX_ALL.pickle')



요일수 = datetime.today().weekday()
기준변동 = 0
if 요일수 ==0:
    print('월',요일수)
    todaycri = 3 + 기준변동
elif 1 <= 요일수 <=4:
    print('주간',요일수)
    todaycri = 1 + 기준변동
elif 요일수 ==5:
    print('토',요일수)
    todaycri = 1 + 기준변동
elif 요일수 ==6:
    print('일',요일수)
    todaycri = 2 + 기준변동


NEWS_html = ''


# target.to_excel('C:/Users/Jinu/PycharmProjects/CYB/NEW22/DART/df_target.xlsx')
# no.to_excel('C:/Users/Jinu/PycharmProjects/CYB/NEW22/DART/df_no.xlsx')
# df3.to_excel('C:/Users/Jinu/PycharmProjects/CYB/NEW22/DART/df3.xlsx')

#newbgs_raw.to_pickle('C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/DART/_DART모니터/newbgs_raw.pickle')
#newbgs_raw.to_pickle('C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/DART/_DART모니터/newbgs.pickle')

#ALL.to_pickle("C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/NEWS_CROL/NEWS_CROL_3/ostk_ALL.xlsx")
n1 = pd.read_pickle("C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/NEWS_CROL/NEWS_CROL_3/ostk_ALL.pickle") #종류별

n2 = pd.read_pickle("C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/NEWS_CROL/NEWS_CROL/many_news.pickle") #매니
n3 = pd.read_pickle("C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/NEWS_CROL/NEWS_CROL_2/stock_news.pickle") #스톡

fl = "C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/NEWS_CROL/NEWS_CROL_3/ostk_ALL.pickle"
last_time = datetime.fromtimestamp(os.path.getmtime(fl)).strftime('%m/%d     %H:%M')


n2['구분'] = '많이본뉴스'
n3['구분'] = '종목뉴스'
nt = pd.concat([n2,n3],axis=0)
nt['뉴스간격'] = (np.datetime64('today') - nt['날짜'].astype('datetime64[D]')).dt.days.fillna(999)
nt = nt[nt['뉴스간격'] <= todaycri]


nt = nt.sort_values(by=['날짜','시간'], ascending=[False,False]).reset_index(drop = True)
nt['제목'] = nt.apply(lambda x :  f"<a href='{str(x['링크'])}'>{str(x['제목'])}</a>" ,axis=1)
nt['뉴스표시'] = nt['표시']
nt = nt[['제목','뉴스표시','구분','날짜','시간']]

nt['날짜'] = nt['날짜'].str.replace('2022-','').str.replace('2023-','').str.replace('2024-','').str.replace('2025-','').str.replace('2026-','')


NEWS23_html = str(nt.to_html(index=False,table_id='news', escape=False))


n1['날짜'] = n1['날짜'].str.replace('2022.','').str.replace('2023.','').str.replace('2024.','').str.replace('2025.','').str.replace('2026.','')
n1 = pd.merge(n1,mst[['종목명_P','코드_P','fn링크','종토링크','링크']].add_suffix('_mst'),left_on='종목명_N',right_on='종목명_P_mst', how='left')
n1 = pd.merge(n1,pg[['종목명_P','등락율_M']].add_suffix('_plog'),left_on='종목명_N',right_on='종목명_P_plog', how='left')

n1 = n1.sort_values(by=['날짜'], ascending=[False]).head(200).reset_index(drop = True)
#n1['링크'] = n1['링크'].apply(lambda x :  f"<a href='{str(x)}'>{'링크'}</a>" )
n1 = n1[n1['뉴스간격'] <= todaycri]


n1['종목명+종토뉴스링크'] = n1.apply(lambda x :  f"<a href='{str(x['종토링크_mst'])}'>{str(x['종목명_N'])}</a>" , axis=1)
n1['종목명+종토뉴스링크'] = n1['종목명+종토뉴스링크'].str.replace('board','news')

n1 = n1[['등락율_M_plog','종목명_N','종목명+종토뉴스링크','제목','뉴스간격','정보제공','날짜']]


NEWS1_html = str(n1.to_html(index=False,table_id='news', escape=False))



NEWS_html += NEWS1_html +"<br><br><br><br>"+NEWS23_html

sys.exit()


















mst = pd.read_pickle(r"C:\Users\Jinu\PycharmProjects\CYB\BATCH\MST_Batch.pickle")


sec_dict_raw = mst[['섹터_B','섹터_대분류_B']].drop_duplicates()
sec_dict = { x : y for x,y in zip(sec_dict_raw['섹터_B'],sec_dict_raw['섹터_대분류_B'])}


print(sec_dict.get('전기차'))

print(sec_dict)

print(type(sec_dict))


sys.exit()


binary_file = pd.read_pickle(f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_reply2/cond.pickle')

new = list(binary_file.columns).pop('하이퍼')
# binary_file.columns = new
print(new)
#print(binary_file.columns)

sys.exit()


mst = pd.read_pickle(r"C:\Users\Jinu\PycharmProjects\CYB\BATCH\MST_Batch.pickle")

fl = r'C:/Users/Jinu/PycharmProjects/CYB/JAMU/Source/PLOG_EX_ALL.pickle'
tdf = pd.read_pickle(fl)


n1 = pd.read_pickle("C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/NEWS_CROL/NEWS_CROL_3/ostk_ALL.pickle") #종류별


n2 = pd.read_pickle("C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/NEWS_CROL/NEWS_CROL/many_news.pickle")



n2.head(5).to_excel('xx.xlsx')
os.system('xx.xlsx')


rdf['종목명링크'] = rdf.apply(lambda x :  f"<a href='{'https://finance.naver.com/item/board.naver?code='+str(x['코드_P']).replace('A','')}'>{str(x['종목명_P'])}</a>" , axis=1)

print(list(rdf['종목명링크']))




time.sleep(999)

n1 = pd.read_pickle(f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_NOTE/{str(datetime.now()-timedelta(days=5))[:10]}.pickle')
n1 = n1[n1['종목명_P'] == '팬오션']

print(n1['코드_P'])







print('하나증권_솔루스첨단소재_20221031074700.pdf'.split('_'))


rsc = 'C:/REPORT/rep_raw'
test='금호석유,30,7'

try:
    stox = test.split(',')[0]
    limit_day = int(test.split(',')[1])
    limit_cnt = int(test.split(',')[2])
except:
    stox = test
    limit_day = 30
    limit_cnt = 10

rl = [ f for f in os.listdir(rsc) if (str(f).count('_'+str(stox)+'_')>0) and (str(f).count('해당기업')<=0)]
rdict = {}
for r in rl:
    rdict[r] = [str(r).split('_')[0],str(r).split('_')[1],str(r).split('_')[2].replace('.pdf','')]

rdf = pd.DataFrame(rdict).T.reset_index(drop=False)
rdf.columns = ['파일명','회사명','종목','날짜']
rdf = rdf.sort_values(by='날짜',ascending=False)
rdf['파일경로'] = rdf['파일명'].apply(lambda x: rsc+"/"+str(x) )
rdf['날짜'] = rdf['날짜'].str[0:4] +'-'+rdf['날짜'].str[4:6]+'-'+rdf['날짜'].str[6:8]
rdf['날짜간격'] = (np.datetime64('today') - rdf['날짜'].astype('datetime64[D]')).dt.days

rdf = rdf[rdf['날짜간격']<=limit_day]




file_list = list(rdf['파일경로'])[0:limit_cnt]
print(file_list)
for i in file_list:
    파일명 = str(i).replace(rsc,'').replace('.pdf','').replace('/','')

    if len(파일명.split('_')) == 3:
        new_name = f'{파일명.split("_")[2]}_{파일명.split("_")[1]}_{파일명.split("_")[0]}{len(파일명.split("_"))}'
    elif len(파일명.split('_')) == 4:
        new_name = f'{파일명.split("_")[2]}_{파일명.split("_")[1]}_{파일명.split("_")[0]}{len(파일명.split("_"))}'
    else:
        new_name = '힝힝'

    print('=======')
    print(len(파일명.split('_')),i)
    print(파일명)
    print(new_name)

sys.exit()

fl = f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_NOTE/{str(datetime.now()-timedelta(days=1))[:10]}.pickle'

datetime.fromtimestamp(os.path.getmtime(fl)).strftime('%Y-%m-%d %H:%M')

datetime.fromtimestamp(os.path.getmtime(fl)).strftime('%Y-%m-%d %H:%M')


test = '헝'
꾱 = 'ㅇㅇ.ㅇㅇ'

print(f'attachment; filename="레포트_"+{str(꾱).split(".")[0]+"_"+str(test)}.zip')




요일 = '월,화,수,목,금,토,일'.split(',')

print()

요일수 = datetime.today().weekday()
if 요일수 ==0:
    print('월',요일수)
elif 1 <= 요일수 <=4:
    print('주간',요일수)
elif 요일수 ==5:
    print('토',요일수)
elif 요일수 ==6:
    print('일',요일수)

import pandas as pd

fl = r'C:/Users/Jinu/PycharmProjects/CYB/JAMU/Source/PLOG_EX_ALL.pickle'
#tdf = pd.read_pickle("C:/Users/Jinu/Desktop/작업쓰레기/__쓸모있음/MOVE_EX1.pickle")
tdf = pd.read_pickle(fl)


tgtg = {
    '체상':5,'체하':3,'섹등':2,'외국계':0.3,'14수종':2,'30수종':2,'수급7일':0.5,'수급30일':0.5,'세투상':0,
    '진대순위':0.1,'설순위':0.5,'에너지':0.2,'0등급':3,'1등급':0.2,
    '진/30':0.5,'설/30':0.5,'섹롱폭':0.3,'롱폭':0.3,'설현폭':1,
    '컨상':0,'컨하':0,'총점':0,'발표':0,'바텀':0.1
}


new_df = pd.DataFrame(columns = ['필터점수']+list(tgtg.keys()))
fil_df = tdf[tdf['필터']!=''].sort_values(by='필터점수', ascending=False).set_index('종목명_P',drop=True)

for tg in tgtg.keys():
    tfdf = fil_df[fil_df['필터'].str.contains(tg)]
    for stx in tfdf.index:
        new_df.loc[stx,tg] = tgtg.get(tg,0)

for stx in fil_df.index:
    new_df.loc[stx,'필터점수'] = fil_df.loc[stx,'필터점수']

new_df.fillna('',inplace=True)
print(new_df.head())
print(len(fil_df))




