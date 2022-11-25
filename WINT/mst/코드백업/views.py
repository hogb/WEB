from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import pandas as pd
import os,sys, time
import numpy as np

from pathlib import Path

from django.views.decorators.csrf import csrf_exempt

from datetime import datetime, timedelta
import re



# Create your views here.

sys.path.append('C:/Users/Jinu/PycharmProjects/CYB')
sys.path.append('C:/Users/Jinu/PycharmProjects/CYB/practice')
sys.path.append('C:/Users/Jinu/PycharmProjects/CYB/JAMU')
sys.path.append('C:/Users/Jinu/PycharmProjects/CYB/NEW22')

import reply2

global basic_uml,basic_dml


basic_uml = f'''
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, maximum-scale=1.0, minimum-scale=1.0">

        <style>
        
        @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@700&display=swap');
        body {{font-family: 'Nanum Gothic', sans-serif;font-size:0.5rem}}
        
        table {{ width:100%;white-space: nowrap}}
        
        td {{text-align: right;}}
        th {{text-align: center;  vertical-align : center; background-color:18D7CB}}
        
        td,ht {{border-top:solid 0.2rem White}}
        td,th {{border-right:solid 0.2rem White}}
        
        </style>
        <body>'''


basic_dml = '''
        </body>
        </html>
        '''


def Templ(con=None):
    tat = '뀨'
    return(f'''
        <html>
        <body>
            <h1> 인덱스 페이지 입니다! {tat}</h1>
            {con}
        </body>
        </html>
    ''')


def m1(request):
    시작시간 = datetime.now()
    tdf = pd.read_pickle(r'C:/Users/Jinu/PycharmProjects/CYB/JAMU/Source/PLOG_EX_ALL.pickle')

    CSS참 = pd.read_excel(r"C:\Users\Jinu\PycharmProjects\WEB\WINT\CSS참고.xlsx")
    CSS컬럼 = CSS참[['컬럼','변경']].set_index('컬럼',drop=True).squeeze().to_dict()
    CSS표현 = CSS참[['컬럼','표현']].set_index('컬럼',drop=True).squeeze().to_dict()
    CSS서식 = CSS참[['컬럼','서식']].set_index('컬럼',drop=True).squeeze().to_dict()

    #CSS참 = pd.Series(CSS참)

    #tdf = pd.read_pickle("C:/Users/Jinu/Desktop/작업쓰레기/__쓸모있음/MOVE_EX1.pickle")

    k_dict = {
    '0등급':['진대', False],
    '1등급':['진대', False],
    '설순위':['설기간합순위', True],
    '진대순위':['진대순위', True],
    '설/30':['설기간합/30일순위', True],
    '외국계':['외국계$$/30일순위', True],
    '에너지':['에너지순위', True],

    '롱폭':['롱폭순위', True],

    '수급7일':['7일_외기법_시총대비_외기법_순위', True],
    '수급30일':['30일_외기법_시총대비_외기법_순위', True],

    '섹등':['ST_등락순위', True],
    '섹롱폭':['ST_롱폭순위', True],
    '바텀':['30일_외기법_시총대비_외기법', False],

    '설현폭':['설현폭순위', True],

    '총점':[ ['총점_J','30수종'], [False,False] ],
    '발표':[ ['발표간격','30수종'], [True,False] ],

    '14수종':['14수종', False],
    '30수종':['30수종', False],

    '체상':['대상점수순위', True],
    '체하':['대상점수순위', True],

    '세투상':['필터에너지합순위_SE', True],
    '진/30':['진대/30일순위', True]
    }

    dicdf = pd.DataFrame(k_dict).T
    dicdf.columns = ['종류','옵션']

    org_list = ['1고현폭',
    '1현재폭',
    '별명_B',
    #'등락2종토링크',
    '30STO표',
    '7일평단대비',
    '30일평단대비',
    '7일_외기법_시총대비_외기법',
    '30일_외기법_시총대비_외기법',
    '7일외기법%',
    '30일외기법%',
    '잠정외기법%',
    '프로그램%',
    '체결강도_M',
    '총점_J',
    '실적이슈',
    '발표간격','섹터_B'
            ]

    org_css = CSS서식

    kind_lam =\
    {
    '??':('??','??')
    ,'등락상':('{background-color:Pink; color:Black; font-weight:bold}',lambda x: f'<div class="등락상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 3))  else x)
    ,'등락상상':('{background-color:FF0000; color:White; font-weight:bold}',lambda x: f'<div class="등락상상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 7))  else x)
    ,'등락하':('{background-color:00D8FF; color:Black; font-weight:bold}',lambda x: f'<div class="등락하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x < -3)) else x)
    ,'등락하하':('{background-color:Blue; color:White; font-weight:bold}',lambda x: f'<div class="등락하하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x < -7)) else x)

    ,'거율상':('{background-color:F599EC; color:000000; font-weight:bold}',lambda x: f'<div class="거율상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 14))  else x)
    ,'거율상상':('{background-color:FF3386; color:FFFFFF; font-weight:bold}',lambda x: f'<div class="거율상상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 28))  else x)
    ,'거율하':('{background-color:83DCFC; color:000000; font-weight:bold}',lambda x: f'<div class="거율하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x < -14))  else x)
    ,'거율하하':('{background-color:314DD8; color:FFFFFF; font-weight:bold}',lambda x: f'<div class="거율하하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x < -28))  else x)

    ,'체강상':('{background-color:F599EC; color:000000; font-weight:bold}',lambda x: f'<div class="체강상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 140))  else x)
    ,'체강상상':('{background-color:FF3386; color:FFFFFF; font-weight:bold}',lambda x: f'<div class="체강상상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 200))  else x)
    ,'체강하':('{background-color:83DCFC; color:000000; font-weight:bold}',lambda x: f'<div class="체강하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x < -140))  else x)
    ,'체강하하':('{background-color:314DD8; color:FFFFFF; font-weight:bold}',lambda x: f'<div class="체강하하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x < -200))  else x)

    }

    # 등락 거% 체강

    # 폭 수급 수종
    # 거래 개인 시총 대금 재무 레포트 공매도 퍼
    # 스토 대차??

    kind_html = ''
    for k,v in zip(kind_lam.keys(),kind_lam.values()):
        kind_html += '.'+str(k)+str(v[0])+'\n'


    #;white-space: nowrap
    # table-layout:fixed; word-break:break-all;height:auto;

    uml = f'''
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, maximum-scale=1.0, minimum-scale=1.0">
        
        <title>test</title>
    
        <style>
    
        @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@700&display=swap');
        body {{font-family: 'Nanum Gothic', sans-serif;font-size:0.5rem}}
        
        table {{ width:120%;white-space: nowrap}}

        td {{text-align: right;}}
        th {{text-align: center;  vertical-align : center; background-color:18D7CB}}

        td,ht {{border-top:solid 2px White}}
        td,th {{border-right:solid 2px White}}

        {kind_html}
        
        .거%양{{background-color:Pink; color:Black; font-weight:bold}}
        .거%음{{background-color:Blue; color:White; font-weight:bold}}
        
        </style>
        </head>
        <body>
        '''

    dml = '''
        </body>
        </html>
        
        '''

    #tdf = tdf[org_list+['필터']]
    
    tdf = tdf[~tdf['섹터_B'].str.contains('|'.join(['제외','제외2','몰라']))]

    mml = ''
    for ky in list(k_dict.keys()):
        #print(k_dict.get(ky)[0],k_dict.get(ky)[1])
        try:tempdf = tdf.sort_values(by=k_dict.get(ky)[0], ascending=k_dict.get(ky)[1]).head(15)
        except:tempdf = tdf.head(3)  #수정

        # tempdf =tempdf.applymap(lambda x: f'<div class="{org_css.get(ky,"???")}">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 0)) else x) #
        # tempdf =tempdf.applymap(lambda x: f'<div class="{org_css.get(ky,"???")}">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 0)) else x) #

        for col in [x for x in tempdf.columns if (x in org_list) and (str(CSS표현.get(str(x),'-')).find('정수')>-1)]:
            #print(col)
            tempdf[col] = tempdf[col].astype('int')



        for col in tempdf.columns:
            서식리스트 = str(CSS서식.get(col,'/')).split('/')
            #print(col,서식리스트,list(kind_lam.keys())[0])
            for tp in [ x for x in 서식리스트 if x in [y for y in kind_lam.keys()]]:
                #tempdf[tp[0]] = tempdf[tp[0]].apply(kind_lam.get())
                #print(tp,col,kind_lam.get(tp))
                tempdf[[col]] =tempdf[[col]].applymap(kind_lam.get(tp)[1])


        tempdf = tempdf[org_list]
        tempdf.rename(columns=CSS컬럼, inplace=True)

        tempml = str(tempdf.to_html(border = False, index=False,table_id='mst2 '+str(ky)))
        tempml = tempml.replace('&lt;','<')\
            .replace('&gt;','>').replace('class="dataframe"','class='+'mst2 '+str(ky))

        mml += '<h2>'+str(ky) +'<h2>'+ '<br>'
        mml += tempml + '<br>' + '<br>'

        #print(mml)




    ahtml = uml + '\n' +mml + '\n' + dml

    #print(ahtml)

    print(시작시간)
    return HttpResponse(f'{ahtml}')


def m2(request,max_gg=100):
    uml = f'''
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, maximum-scale=1.0, minimum-scale=1.0">
        
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@700&display=swap');
        
        body {{font-family: 'Nanum Gothic', sans-serif;font-size:1rem}}
        </style>

        </head>
        <body>
        '''

    dml = '''
        </body>
        </html>
        
        '''



    m2_html = ''
    #tdf = pd.read_pickle("C:/Users/Jinu/Desktop/작업쓰레기/__쓸모있음/MOVE_EX1.pickle")
    try:
        with open(f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/MST2/{str(datetime.now())[:10]}.txt', 'r',encoding='UTF-8') as File:
            data = File.read()
    except:
        with open(f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/MST2/{str(datetime.now()-timedelta(days=1))[:10]}.txt', 'r',encoding='UTF-8') as File:
            data = File.read()

    dl = str(data)
    dl = dl.split('\n')

    mml = ''
    
    cntgg = 0
    for d in dl:
        if cntgg > max_gg-1:
            break
        cntgg += str(d).count('@')


        con = re.findall("\((.*?)\)",d)

        dre = str(re.findall("\((.*?)\)",d)).replace('[','').replace(']','')
        dre2 = str(re.findall("\[(.*?)\]",d)).replace('[','').replace(']','')

        d = re.sub("\((.*?)\)",'',d).replace('PM','오후').replace('PM','오전')


        if len(con) ==1:
            mml += f'<a href={dre}>{d}</a><br>'+'\n'
        else:
            mml += f'{d}<br>' +'\n'



    mml = mml.replace('@','\n')




    mml =f'''
    {mml}
    '''

    m2_html = uml + '\n' +mml + '\n' + dml
    print(m2_html)


    return HttpResponse(f'{m2_html}')


def m3(request):

    ntdf = pd.read_pickle(f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_NOTE/{str(datetime.now())[:10]}.pickle')

    #
    # ntdf.head(100).to_excel('m3.xlsx')
    # os.system('m3.xlsx')
    # print(ntdf.head())

    m3_html = NOTE_today(ntdf,2)


    return return HttpResponse(f'{m3_html}')

def m4(request):
    col=25
    row=13

    # m4df = pd.read_clipboard()
    # m4df.to_pickle(os.path.join(r'C:\Users\Jinu\PycharmProjects\WEB\WINT\temp/','temp_m4_msg'+'.pickle'))

    m4df = pd.read_pickle(os.path.join(r'C:\Users\Jinu\PycharmProjects\WEB\WINT\temp/','temp_m4_msg'+'.pickle'))
    #m4df['내용'] = m4df['번호'].astype('str') + m4df['내용'].astype('str')
    m4d = list(m4df['내용'])



    stt = f'''
    <html>
    <body>
        <form action='/reply2/' method="post"><br>
            
            <br><textarea name='cond_kind' rows={1} cols={int(col/3)}>1</textarea><input type='submit'>
            
            <br>
            <br><textarea name='cond_{1}' rows={row} cols={col}>{m4d[1-1]}</textarea>
                <textarea name='cond_{2}' rows={row} cols={col}>{m4d[2-1]}</textarea>
                <textarea name='cond_{3}' rows={row} cols={col}>{m4d[3-1]}</textarea>
            <br>
            <br>
                <textarea name='cond_{4}' rows={row} cols={col}>{m4d[4-1]}</textarea>
                <textarea name='cond_{5}' rows={row} cols={col}>{m4d[5-1]}</textarea>
                <textarea name='cond_{6}' rows={row} cols={col}>{m4d[6-1]}</textarea>
            <br>
            <br>
                <textarea name='cond_{7}' rows={row} cols={col}>{m4d[7-1]}</textarea>
                <textarea name='cond_{8}' rows={row} cols={col}>{m4d[8-1]}</textarea>
                <textarea name='cond_{9}' rows={row} cols={col}>{m4d[9-1]}</textarea>            
            <br>
            <br>
                <textarea name='cond_{10}' rows={row} cols={col}>{m4d[10-1]}</textarea>
                <textarea name='cond_{11}' rows={row} cols={col}>{m4d[11-1]}</textarea>
                <textarea name='cond_{12}' rows={row} cols={col}>{m4d[12-1]}</textarea>
            <br>
            <br>
                <textarea name='cond_{13}' rows={row} cols={col}>{m4d[13-1]}</textarea>
                <textarea name='cond_{14}' rows={row} cols={col}>{m4d[14-1]}</textarea>
                <textarea name='cond_{15}' rows={row} cols={col}>{m4d[15-1]}</textarea>
            

            
        </form>
    </body>
    </html>
    
    '''

    #print(stt)


    return HttpResponse(f'{stt}')


def m5(request):
    tdf = pd.read_pickle("C:/Users/Jinu/Desktop/작업쓰레기/__쓸모있음/MOVE_EX1.pickle")
    return HttpResponse(f'{len(tdf)}')
def m6(request):
    tdf = pd.read_pickle("C:/Users/Jinu/Desktop/작업쓰레기/__쓸모있음/MOVE_EX1.pickle")
    return HttpResponse(f'{len(tdf)}')

@csrf_exempt
def read(request):
    if request.method == "GET":
        con_send = '''
        <form action='/read/' method="post">
            <input type='text' name='stock_name'>
            <input type='submit'>
        </form>
        '''
        return HttpResponse(Templ(con_send))

    elif request.method == "POST":
        #some = str(request.POST['stock_name'])
        #fl = os.listdir('/BU')

        tams = '_'+str(request.POST['stock_name'])+'_'
        fls = os.listdir(os.path.join(Path(__file__).resolve().parent.parent,'static'))
        resfl = [ x for x in fls if str(x).find(tams) > -1][0]


        # try:ressrc = os.path.join('BU',str(resfl))
        # except:ressrc = '1'
        #
        # reshtml = f'''
        # <img src="{ressrc}" alt={str(request.POST['stock_name'])} width="80%">
        # <h6>{ressrc}</h6>
        # '''

        try:ressrc = os.path.join('static',str(resfl))
        except:ressrc = '1'


        reshtml = f'''
        <img src="{ressrc}" alt={str(request.POST['stock_name'])} width="80%">
        <h6>{fls}<br>{ressrc}</h6>
        '''

        return HttpResponse(Templ(str(reshtml)))


def index(request):
    mdict = {
        'm4':'reply2'
    ,'m2': 'MST3'
    ,'m3': 'NOTE'
    ,'m1': 'PLOG_MST12'

    }

    tgs = ''
    for i in range(1,7):
        tgs += f'<br><a href="/{"m"+str(i)}">{ mdict.get("m"+str(i),"?") }</a>'

    con_send = f''' 
    <a href="/read">읽기</a>
    {tgs}
    '''


    return HttpResponse(Templ(con_send))

def pdd(request):

    tempdf = '1'
    tat = len(tempdf)

    text = ''

    for i in tempdf.index:
        text += str(tempdf.at[i,'제목'])+ '</br>>'

    return HttpResponse(text)


def NOTE_today(rdf,todaycri):
    TODAY = rdf[rdf['날짜간격'] <= todaycri - 1]
    TODAY = TODAY.reset_index(drop=True)
    TODAY[TODAY.select_dtypes('category').columns] = TODAY[TODAY.select_dtypes('category').columns].astype('object')
    TODAY = TODAY.fillna(98765)
    TODAY[['1현재폭', '1고저폭', '20현재폭', '20고저폭', '90현재폭', '90고저폭', '변경율', '변등', 'REP간']] = TODAY[['1현재폭', '1고저폭', '20현재폭', '20고저폭', '90현재폭', '90고저폭', '변경율', '변등', 'REP간']].astype('int')
    TODAY['1일_총합'] = np.around(TODAY['1일_총합'], 1)
    TODAY = TODAY.replace(98765, '')

    TODAY = TODAY.sort_values(by=['7일_상승변등이후','1일_변등평','1일_총합','20일_변경율평', '7일_변경합', '1일_변경합', '20일_변경합','종목명', '날짜'],
                              ascending=[False, False, False, False, False, False, False, False, False])
    TODAY = TODAY.reset_index(drop=True)

    col_list = '변등,별명_B,등락율_M,투자의견,의견변경,주가변경,변경율,REP간,베스트,회사명,7일_변등평,업사,날짜간격,오늘,REP사이날짜,1현재폭,1고저폭,20현재폭,20고저폭,90현재폭,90고저폭,코드_P'.split(',')

    TODAY = TODAY[col_list]
    TODAY['링크'] = TODAY['코드_P'].apply(lambda x :  f"<a href='{'https://finance.naver.com/item/main.naver?code='+str(x).replace('A','')}'>{str(x)}</a>" )
    #TODAY['링크'] = TODAY['코드_P'].apply(lambda x :  f"'{'https://finance.naver.com/item/main.naver?code='+str(x).replace('A','')}'{str(x)}")

    TODAY = TODAY.drop(['코드_P'], axis=1)
    TDOAY = TODAY.applymap(lambda x: '' if str(x) == '0' else x)

    #
    # TDOAY.to_excel('text.xlsx')
    # os.system('text.xlsx')

    TODAY_html = str(TDOAY.to_html(border = False, index=False,table_id='NOTE_today',escape=False))



    global basic_uml,basic_dml

    FINAL_html = basic_uml + TODAY_html + basic_dml

    print(FINAL_html)


@csrf_exempt
def reply2_main(request):
    #print(request)

    if request.method == "GET":
        res = m4(request)
        res = '겟겟'
        
        return HttpResponseRedirect("/m4/")

    elif request.method == "POST":

        new_dict = {}
        for i in range(1,16):
            con = str(request.POST[f'cond_{i}'])#.replace('\n','<br>')
            # print(con)
            # print('============')
            new_dict[i] = [i,con]


        new_df = pd.DataFrame(new_dict).T;  new_df.columns = ['번호','내용']

        new_df.to_pickle(os.path.join(r'C:\Users\Jinu\PycharmProjects\WEB\WINT\temp/','temp_m4_msg'+'.pickle'))
        #
        # rdf = pd.read_pickle(f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_reply2/cond.pickle')
        # print(rdf.info())

        tmsg = request.POST[f'cond_{request.POST["cond_kind"]}']

        res = str(tmsg)

        # print(tmsg)
        # print('---')
        # print(str(tmsg))
        #
        reply2.main(str(tmsg),'123')
        reply2.Multi_png(str(tmsg))

        #
        #
        binary_file = open(r"C:\Users\Jinu\PycharmProjects\CYB\practice\cond.xlsx", 'rb')
        response = HttpResponse(binary_file.read(), content_type="application/octet-stream; charset=utf-8")
        response['Content-Disposition'] = f'attachment; filename="cond_"+{str(datetime.now()).split(".")[0]+"_"+request.POST["cond_kind"]}.xlsx'
        #response.get()

        return response
        #return HttpResponse(f'{res}')

        #return HttpResponseRedirect("/m4/")

        #return render(response,f'{res}')
        #return HttpResponseRedirect("/m4/")


# @
# 섹터,제외$바이오$미분류,미포함
# 시총,0.15,이상
# 7대평,20,이상
# @발표,7대평,30수,14거%,30현,
# @2@0@대금돌@300



start = time.time()  # 시작 시간 저장

m4(1)

print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간




