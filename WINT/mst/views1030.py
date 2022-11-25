from django.shortcuts import render, HttpResponse
import pandas as pd
import os,sys, time

from pathlib import Path

from django.views.decorators.csrf import csrf_exempt

# Create your views here.


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
    tdf = pd.read_pickle('C:/Users/Jinu/PycharmProjects/CYB/JAMU/Source/PLOG_EX_ALL.pickle')

    CSS참 = pd.read_excel('CSS참고.xlsx')
    CSS컬럼 = CSS참[['컬럼','변경']].set_index('컬럼',drop=True).squeeze().to_dict()
    CSS표현 = CSS참[['컬럼','표현']].set_index('컬럼',drop=True).squeeze().to_dict()

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

    org_css = {'7일평단대비' : '/양/음',
                '30일평단대비':'/양/음'}


    #;white-space: nowrap

    uml = '''
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>test</title>
    
        <style>
    
        @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@700&display=swap');
        body {font-family: 'Nanum Gothic', sans-serif;}
        
        table { width:110%; table-layout:fixed; word-break:break-all;height:auto;white-space: nowrap}

        td {text-align: right;}
        th {text-align: center;  vertical-align : center; background-color:18D7CB}

        td,ht {border-top:solid 2px White}
        td,th {border-right:solid 2px White}

        .양{background-color:Pink; color:Black; font-weight:bold}
        .음{background-color:Blue; color:White; font-weight:bold}
        
        .거%양{background-color:Pink; color:Black; font-weight:bold}
        .거%음{background-color:Blue; color:White; font-weight:bold}
        
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
        print(k_dict.get(ky)[0],k_dict.get(ky)[1])
        try:tempdf = tdf.sort_values(by=k_dict.get(ky)[0], ascending=k_dict.get(ky)[1]).head(15)
        except:tempdf = tdf.head(3)  #수정

        # tempdf =tempdf.applymap(lambda x: f'<div class="{org_css.get(ky,"???")}">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 0)) else x) #
        # tempdf =tempdf.applymap(lambda x: f'<div class="{org_css.get(ky,"???")}">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 0)) else x) #

        for col in [x for x in tempdf.columns if (x in org_list) and (str(CSS표현.get(str(x),'-')).find('정수')>-1)]:
            #print(col)
            tempdf[col] = tempdf[col].astype('int')



        for col in tempdf.columns:
            try:tempdf.loc[:,col] =tempdf.loc[:,col].apply(lambda x: f'<div class="양">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 0)) and (org_css.get(col,"???").find('/양')>-1) else x)
            except:1
            try:tempdf.loc[:,col] =tempdf.loc[:,col].apply(lambda x: f'<div class="음">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x < 0)) and (org_css.get(col,"???").find('/음')>-1) else x)
            except:1




        tempdf = tempdf[org_list]
        tempdf.rename(columns=CSS컬럼, inplace=True)

        tempml = str(tempdf.to_html(border = False, index=False,table_id='mst2 '+str(ky)))
        tempml = tempml.replace('&lt;','<')\
            .replace('&gt;','>').replace('class="dataframe"','class='+'mst2 '+str(ky))

        mml += '<h2>'+str(ky) +'<h2>'+ '<br>'
        mml += tempml + '<br>' + '<br>'


    ahtml = uml + '\n' +mml + '\n' + dml

    print(ahtml)
    time.sleep(999)
    return HttpResponse(f'{ahtml}')


def m2(request):
    tdf = pd.read_pickle("C:/Users/Jinu/Desktop/작업쓰레기/__쓸모있음/MOVE_EX1.pickle")
    return HttpResponse(f'{len(tdf)}')
def m3(request):
    tdf = pd.read_pickle("C:/Users/Jinu/Desktop/작업쓰레기/__쓸모있음/MOVE_EX1.pickle")
    return HttpResponse(f'{len(tdf)}')
def m4(request):
    tdf = pd.read_pickle("C:/Users/Jinu/Desktop/작업쓰레기/__쓸모있음/MOVE_EX1.pickle")
    return HttpResponse(f'{len(tdf)}')
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

    tgs = ''
    for i in range(1,7):
        tgs += f'<br><a href="/{"m"+str(i)}">{"m"+str(i)}</a>'

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

m1(1)