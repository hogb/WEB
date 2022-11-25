from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import pandas as pd
import os,sys, time
import numpy as np

from pathlib import Path

from django.views.decorators.csrf import csrf_exempt

from datetime import datetime, timedelta
import re
from IPython.display import display

from xlsx2html import xlsx2html
# Create your views here.


sys.path.append('C:/Users/Jinu/PycharmProjects/CYB')
sys.path.append('C:/Users/Jinu/PycharmProjects/CYB/practice')
sys.path.append('C:/Users/Jinu/PycharmProjects/CYB/JAMU')
sys.path.append('C:/Users/Jinu/PycharmProjects/CYB/NEW22')

import reply2
import zipfile
import urllib
import shutil

global basic_uml,basic_dml
global kind_lam,kind_html

global mst
mst = pd.read_pickle(r"C:\Users\Jinu\PycharmProjects\CYB\BATCH\MST_Batch.pickle")

sec_dict_raw = mst[['섹터_B','섹터_대분류_B']].drop_duplicates()
sec_dict = { x : y for x,y in zip(sec_dict_raw['섹터_B'],sec_dict_raw['섹터_대분류_B'])}


kind_lam = \
    {

        #<form id="정유" action="/kr_sec/" method="POST" onclick="document.getElementById('정유').submit();"><input type="hidden" name="정유" value="정유">정유</form>

        #'반도체대분류':('{background-color:D2042D; color:Black; font-weight:bold}',lambda x: str(x).replace('<','').split('form id="')[-1].split('"')[0])


        '반도체대분류':('{background-color:D2042D; color:Black; font-weight:bold}',lambda x: f'<div class="반도체대분류">'+str(x)+'</div>' if (sec_dict.get(str(str(x).replace('<','').split('form id="')[-1].split('"')[0]),'-').count('반도')>0)  else x)
        ,'은행대분류':('{background-color:D3D3D3; color:Black; font-weight:bold}',lambda x: f'<div class="은행대분류">'+str(x)+'</div>' if (sec_dict.get(str(str(x).replace('<','').split('form id="')[-1].split('"')[0]),'-').count('은행')>0)  else x)
        ,'전기차대분류':('{background-color:00FFFF; color:Black; font-weight:bold}',lambda x: f'<div class="전기차대분류">'+str(x)+'</div>' if (sec_dict.get(str(str(x).replace('<','').split('form id="')[-1].split('"')[0]),'-').count('전기')>0)  else x)
        ,'에너지대분류':('{background-color:8B4000; color:Black; font-weight:bold}',lambda x: f'<div class="에너지대분류">'+str(x)+'</div>' if (sec_dict.get(str(str(x).replace('<','').split('form id="')[-1].split('"')[0]),'-').count('에너지')>0)  else x)
        ,'PCB대분류':('{background-color:FF69B4; color:Black; font-weight:bold}',lambda x: f'<div class="PCB대분류">'+str(x)+'</div>' if (sec_dict.get(str(str(x).replace('<','').split('form id="')[-1].split('"')[0]),'-').count('PCB')>0)  else x)
        ,'항공대분류':('{background-color:00FF00; color:Black; font-weight:bold}',lambda x: f'<div class="항공대분류">'+str(x)+'</div>' if (sec_dict.get(str(str(x).replace('<','').split('form id="')[-1].split('"')[0]),'-').count('항공')>0)  else x)
        
        ,'등락상':('{background-color:f7d6e4; color:Black; font-weight:bold}',lambda x: f'<div class="등락상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x >= 1))  else x)
        ,'등락상상':('{background-color:pink; color:Black; font-weight:bold}',lambda x: f'<div class="등락상상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x >= 3))  else x)
        ,'등락상상상':('{background-color:FF0000; color:White; font-weight:bold}',lambda x: f'<div class="등락상상상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x >= 7))  else x)
        ,'등락하':('{background-color:bedcf0; color:Black; font-weight:bold}',lambda x: f'<div class="등락하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x <= -1)) else x)
        ,'등락하하':('{background-color:00D8FF; color:Black; font-weight:bold}',lambda x: f'<div class="등락하하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x <= -3)) else x)
        ,'등락하하하':('{background-color:Blue; color:White; font-weight:bold}',lambda x: f'<div class="등락하하하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x <= -7)) else x)

        ,'거율상':('{background-color:abe1af; color:000000; font-weight:bold}',lambda x: f'<div class="거율상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x >= 8))  else x)
        ,'거율상상':('{background-color:30e83e; color:000000; font-weight:bold}',lambda x: f'<div class="거율상상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x >= 16))  else x)
        ,'거율상상상':('{background-color:01960c; color:FFFFFF; font-weight:bold}',lambda x: f'<div class="거율상상상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x >= 24))  else x)

        ,'거율하':('{background-color:e3c9e9; color:000000; font-weight:bold}',lambda x: f'<div class="거율하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x <= -8))  else x)
        ,'거율하하':('{background-color:d566ec; color:000000; font-weight:bold}',lambda x: f'<div class="거율하하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x <= -16))  else x)
        ,'거율하하하':('{background-color:5c026f; color:FFFFFF; font-weight:bold}',lambda x: f'<div class="거율하하하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x <= -24))  else x)

        ,'수급상':('{background-color:F599EC; color:000000; font-weight:bold}',lambda x: f'<div class="수급상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 0.9))  else x)
        ,'수급상상':('{background-color:FF3386; color:FFFFFF; font-weight:bold}',lambda x: f'<div class="수급상상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 2))  else x)
        ,'수급하':('{background-color:83DCFC; color:000000; font-weight:bold}',lambda x: f'<div class="수급하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x < -0.9))  else x)
        ,'수급하하':('{background-color:314DD8; color:FFFFFF; font-weight:bold}',lambda x: f'<div class="수급하하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x < -2))  else x)

        ,'체강상':('{background-color:F599EC; color:000000; font-weight:bold}',lambda x: f'<div class="체강상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 150))  else x)
        ,'체강상상':('{background-color:FF3386; color:FFFFFF; font-weight:bold}',lambda x: f'<div class="체강상상">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x > 200))  else x)
        ,'체강하':('{background-color:83DCFC; color:000000; font-weight:bold}',lambda x: f'<div class="체강하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x <= 65))  else x)
        ,'체강하하':('{background-color:314DD8; color:FFFFFF; font-weight:bold}',lambda x: f'<div class="체강하하">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x <= 45))  else x)

        ,'노트상':('{background-color:Pink; color:Black; font-weight:bold}',lambda x: f'<div class="노트상">'+str(x)+'</div>' if (str(x).count('상')>0)  else x)
        ,'노트하':('{background-color:00D8FF; color:Black; font-weight:bold}',lambda x: f'<div class="노트하">'+str(x)+'</div>' if (str(x).count('하')>0)  else x)

        ,'컨상':('{background-color:Pink; color:Black; font-weight:bold}',lambda x: f'<div class="컨상">'+str(x)+'</div>' if (str(x).count('컨상')>0)  else x)
        ,'컨하':('{background-color:00D8FF; color:Black; font-weight:bold}',lambda x: f'<div class="컨하">'+str(x)+'</div>' if (str(x).count('컨하')>0)  else x)

        ,'총점1위':('{background-color:b70000; color:FFFFFF; font-weight:bold}',lambda x: f'<div class="총점1위">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x >= 15))  else x)
        ,'총점2위':('{background-color:fa8315; color:000000; font-weight:bold}',lambda x: f'<div class="총점2위">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x >= 10))  else x)
        ,'총점3위':('{background-color:fadf15; color:000000; font-weight:bold}',lambda x: f'<div class="총점3위">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x >= 5))  else x)
        ,'총점4위':('{background-color:b6b6b6; color:000000; font-weight:bold}',lambda x: f'<div class="총점4위">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x < 0))  else x)

        ,'대금1':('{background-color:ffff02; color:000000; font-weight:bold}',lambda x: f'<div class="대금1">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x >= 80))  else x)
        ,'대금2':('{background-color:eff1c7; color:000000; font-weight:bold}',lambda x: f'<div class="대금2">'+str(x)+'</div>' if ((type(x) != type('s')) and ( x >= 25))  else x)



        ,'기둥':('{background-color:9F9F9F; color:9F9F9F; font-weight:bold}',lambda x: f'<div class="기둥">'+str(x)+'</div>' if 1  else x)

    }

kind_html = ''
for k,v in zip(kind_lam.keys(),kind_lam.values()):
    kind_html += '.'+str(k)+str(v[0])+'\n'




def index(request):
    mdict = {
        'm0':'리스트'
        ,'m1':'reply2'
        ,'m2': 'BOT3'
        ,'m3': 'PLOG_MST12'
        ,'m4': 'NOTE'
        ,'m5': '야후'
        ,'m6': '뉴스'

    }

    tgs = ''
    for i in range(0,7):
        tgs += f'<h1><br><a href="/{"m"+str(i)}">{ mdict.get("m"+str(i),"?") }</a><h1>'

    #<h1><a href="/read">읽기</a><h1>
    con_send = f''' 
    {tgs}
    '''


    return HttpResponse(Templ(con_send))


#<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, maximum-scale=2.0, minimum-scale=0.5">

# 등락 거% 체강

# 폭 수급 수종
# 거래 개인 시총 대금 재무 레포트 공매도 퍼
# 스토 대차??

#;white-space: nowrap
# table-layout:fixed; word-break:break-all;height:auto;
#table {{table-layout: fixed;overflow: auto}}
#th z-index: 1
def basic_uml(cont=None,cont2=None):
    th_padding = 1
    bsc_uml = f'''
    <html lang="en">
    <head>
    <meta charset="UTF-8">   

    <script>
    
    function Hello()
    {{alert('이벤트 발생함')}}
    
    
    </script>        

    <style>
    
    
    form{{display:inline}}


    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic&display=swap');
    
    
    body {{font-family: 'Nanum Gothic',sans-serif;font-size:0.5rem}}
    
    <!-- col {{width="relative_length"}} -->
    
    table {{border-collapse:collapse}}
    
    
    <!--table {{overflow:auto}} -->   
    
    th {{position: sticky;    top: 0  ; z-index: 9999}}
    
    th {{ text-align: center;  vertical-align : center; background-color:18D7CB}}
    th {{padding-left:{th_padding/100}rem;padding-right:{th_padding/100}rem;}}
    th {{border-right:solid {0.02}rem gray}}
    
    td {{text-align: right;}}
    
    tr {{border-bottom:{0.02}rem solid lightgray;}}
    col {{border-bottom:{1}rem solid Red;}}    
    
    td {{border-top:solid {0.0}rem White}}
    td {{border-right:solid {0.00}rem lightgray}}
    td {{border-left:solid {0.0}rem White}}
    td {{border-bottom:solid {0.0}rem White}}
      
    
    .right정렬 {{text-align: right;}}
    .center정렬 {{text-align: center;}}
    .left정렬 {{text-align: left;}}
    
    .넓 {{padding-left:{th_padding*1.3}rem ; white-space: nowrap}}
    .지킴 {{ white-space: nowrap}}
    
    .la_time {{font-size:1rem;color:Red;white-space:pre}}
    .rem2 {{font-size:2rem}}
    
    ????#plog_newdf {{min-width:130rem}}
    #plog_newdf {{word-break:nowrap}}
    
    td {{
    width: 1%;
    white-space: nowrap;
    }}
    
    {cont}
    
    {cont2}
    
    </style>
    <body>'''

    return bsc_uml

def basic_dml(cont=None):
    bsc_uml = f'''
    </body>
    </html>
    '''
    return bsc_uml


@csrf_exempt
def read(request):
    if request.method == "GET":
        con_send = '''
        <form action='/read/' method="post">
            <input type='text' name='stock_name'>
            <input type='submit' value='추출'>
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

def Templ(con=None):
    tat = '뀨'
    return(f'''
        <html>
        <body>
            <h1><br><br></h1>
            {con}
        </body>
        </html>
    ''')

def m0(request):
    col=25
    row=13

    # m1df = pd.read_clipboard()
    # m1df.to_pickle(os.path.join(r'C:\Users\Jinu\PycharmProjects\WEB\WINT\temp/','temp_m1_msg'+'.pickle'))

    m1df = pd.read_pickle(os.path.join(r'C:\Users\Jinu\PycharmProjects\WEB\WINT\temp/','temp_m1_msg'+'.pickle'))
    #m1df['내용'] = m1df['번호'].astype('str') + m1df['내용'].astype('str')
    m1d = list(m1df['내용'])

    #<br><textarea name='cond_kind' rows={1} cols={int(col/3)}>1</textarea>

    cond_kind_list = ''
    for x in range(1,16):
        cond_kind_list += f'<option value="{x}">{x}</option>'

    stt = f'''
    <html>
    <body>
        <form action='/reply2_list/' method="post"><br>
            <input type='submit' value='리스트추출' style="width:12rem; font-size:1rem; height:2rem">
            <br><br>
            
            <input type="radio" name="chart_sc" value="SUM" checked> SUM
            <input type="radio" name="chart_sc" value="DAILY_300"> D300
            
            <select name="cond_kind">
                {cond_kind_list}
		    </select>
            
            <br>
            <br><textarea name='cond_{1}' rows={row} cols={col}>{m1d[1-1]}</textarea>
                <textarea name='cond_{2}' rows={row} cols={col}>{m1d[2-1]}</textarea>
                <textarea name='cond_{3}' rows={row} cols={col}>{m1d[3-1]}</textarea>
            <br>
            <br>
                <textarea name='cond_{4}' rows={row} cols={col}>{m1d[4-1]}</textarea>
                <textarea name='cond_{5}' rows={row} cols={col}>{m1d[5-1]}</textarea>
                <textarea name='cond_{6}' rows={row} cols={col}>{m1d[6-1]}</textarea>
            <br>
            <br>
                <textarea name='cond_{7}' rows={row} cols={col}>{m1d[7-1]}</textarea>
                <textarea name='cond_{8}' rows={row} cols={col}>{m1d[8-1]}</textarea>
                <textarea name='cond_{9}' rows={row} cols={col}>{m1d[9-1]}</textarea>            
            <br>
            <br>
                <textarea name='cond_{10}' rows={row} cols={col}>{m1d[10-1]}</textarea>
                <textarea name='cond_{11}' rows={row} cols={col}>{m1d[11-1]}</textarea>
                <textarea name='cond_{12}' rows={row} cols={col}>{m1d[12-1]}</textarea>
            <br>
            <br>
                <textarea name='cond_{13}' rows={row} cols={col}>{m1d[13-1]}</textarea>
                <textarea name='cond_{14}' rows={row} cols={col}>{m1d[14-1]}</textarea>
                <textarea name='cond_{15}' rows={row} cols={col}>{m1d[15-1]}</textarea>
            
        </form>
    </body>
    </html>
    
    '''

    #print(stt)


    return HttpResponse(f'{stt}')


def m1(request):
    col=25
    row=13

    # m1df = pd.read_clipboard()
    # m1df.to_pickle(os.path.join(r'C:\Users\Jinu\PycharmProjects\WEB\WINT\temp/','temp_m1_msg'+'.pickle'))

    m1df = pd.read_pickle(os.path.join(r'C:\Users\Jinu\PycharmProjects\WEB\WINT\temp/','temp_m1_msg'+'.pickle'))
    #m1df['내용'] = m1df['번호'].astype('str') + m1df['내용'].astype('str')
    m1d = list(m1df['내용'])

    cond_kind_list = ''
    for x in range(1,16):
        cond_kind_list += f'<option value="{x}">{x}</option>'

    stt = f'''
    <html>
    <body>
        <form action='/reply2/' method="post"><br>
            <input type='submit' value='엑셀추출' style="width:10rem; font-size:1rem; height:2rem">
            <br><br>
            
            <select name="cond_kind">
                {cond_kind_list}
		    </select>
            
            <br>
            <br><textarea name='cond_{1}' rows={row} cols={col}>{m1d[1-1]}</textarea>
                <textarea name='cond_{2}' rows={row} cols={col}>{m1d[2-1]}</textarea>
                <textarea name='cond_{3}' rows={row} cols={col}>{m1d[3-1]}</textarea>
            <br>
            <br>
                <textarea name='cond_{4}' rows={row} cols={col}>{m1d[4-1]}</textarea>
                <textarea name='cond_{5}' rows={row} cols={col}>{m1d[5-1]}</textarea>
                <textarea name='cond_{6}' rows={row} cols={col}>{m1d[6-1]}</textarea>
            <br>
            <br>
                <textarea name='cond_{7}' rows={row} cols={col}>{m1d[7-1]}</textarea>
                <textarea name='cond_{8}' rows={row} cols={col}>{m1d[8-1]}</textarea>
                <textarea name='cond_{9}' rows={row} cols={col}>{m1d[9-1]}</textarea>            
            <br>
            <br>
                <textarea name='cond_{10}' rows={row} cols={col}>{m1d[10-1]}</textarea>
                <textarea name='cond_{11}' rows={row} cols={col}>{m1d[11-1]}</textarea>
                <textarea name='cond_{12}' rows={row} cols={col}>{m1d[12-1]}</textarea>
            <br>
            <br>
                <textarea name='cond_{13}' rows={row} cols={col}>{m1d[13-1]}</textarea>
                <textarea name='cond_{14}' rows={row} cols={col}>{m1d[14-1]}</textarea>
                <textarea name='cond_{15}' rows={row} cols={col}>{m1d[15-1]}</textarea>
            
        </form>
    </body>
    </html>
    
    '''

    #print(stt)


    return HttpResponse(f'{stt}')

def m2(request):

    css_add = '''
    table {{}}
    '''

    bot3_html,la_time = bot3()
    utml = basic_uml(kind_html)
    dtml = basic_dml()
    la_time = f'<div class="la_time"><h1>{la_time}</h1></div>'

    m2_html = la_time + utml + bot3_html + dtml

    #print(m2_html)
    #return
    return HttpResponse(f'{m2_html}')

def m3(request):

    css_add = '''
    table {{}}
    
    '''

    plog_html,la_time = plog()
    utml = basic_uml(kind_html)
    dtml = basic_dml()
    la_time = f'<div class="la_time"><h1>{la_time}</h1></div>'

    m3_html = la_time + utml + plog_html + dtml

    #print(m2_html)
    #return
    return HttpResponse(f'{m3_html}')


@csrf_exempt
def m4(request):

    utml = basic_uml(kind_html)
    dtml = basic_dml()

    #comp = f'<fort size="300"><a href="https://comp.fnguide.com/SVO2/ASP/SVD_Report_Summary.asp?pGB=1&gicode=A005930&cID=&MenuYn=Y&ReportGB=&NewMenuID=901&stkGb=701"> 요약써머리</a></font>'

    comp = '''
    <form action='/m44/' method="post">
            <input type='text' name='report' style="height:3rem; width:9rem; font-size:2rem; text-align: center" />
            <input type='submit' value='레포트' style="height:3rem; width:9rem; font-size:2rem; text-align: center" />
    </form>
    <br>
    '''

    comp1 = '''<button type="button" style="width:12rem; font-size:2rem;height:3rem" 
        onclick="location.href=\'https://comp.fnguide.com/SVO2/ASP/SVD_Report_Summary.asp?pGB=1&gicode=A005930&cID=&MenuYn=Y&ReportGB=&NewMenuID=901&stkGb=701\'">요약써머리</button>'''

    comp2 = '''
    <form action='/m4/' method="get">
            <input type='submit' value='원본' style="height:3rem; width:6rem; font-size:2rem; text-align: center" />
    </form>
    '''

    comp3 = '''
    <form action='/m4/' method="post">
            <input type="hidden" name="note_ctr" value=0 />
            <input type="hidden" name="note_chg" value=0 />
            <input type="hidden" name="note_plus" value=0 />
            <input type='submit' value='오늘' style="height:3rem; width:6rem; font-size:2rem; text-align: center" />
    </form>
    '''

    comp4 = '''
    <form action='/m4/' method="post">
            <input type="hidden" name="note_ctr" value=999 />
            <input type="hidden" name="note_chg" value=1 />
            <input type="hidden" name="note_plus" value=3 />
            <input type='submit' value='변경' style="height:3rem; width:6rem; font-size:2rem;text-align: center " />
    </form>
    '''

    comp5 = '''
    <form action='/m4/' method="post">
            <input type="hidden" name="note_ctr" value=0 />
            <input type="hidden" name="note_chg" value=1 />
            <input type="hidden" name="note_plus" value=0 />
            <input type='submit' value='오늘변경' style="height:3rem; width:12rem; font-size:2rem;text-align: center " />
    </form>
    '''




    note_sort_list = ''

    for i in '7일_상승변등이후,7일_변등평,20일_변등평,60일_변등평,7일_변경율평,20일_변경율평,60일_변경율평,7일_카운트,20일_카운트,60일_카운트'.split(','):
        note_sort_list += f'<option value="{i}">  {i}  </option>'

    comp6 =f'''
    <br><br>
            <select name="note_sort" style="font-size:1.5rem;text-align: center ">
                {note_sort_list}
		    </select>
    
    '''



    if request.method == "GET":
        note_html,la_time = NOTE_today(999,0,0,'-')
        la_time = f'<div class="la_time" onclick="Hello();"><h1>{la_time} </h1></div>'
        m4_html = utml + la_time +comp +'<br>'+comp1 + comp2 + comp3 + comp4+ comp5+comp6 +'<br><br><br>'+  note_html + dtml
        return HttpResponse(f'{m4_html}')

    elif request.method == "POST":
        note_html,la_time = NOTE_today(int(request.POST['note_ctr']),int(request.POST['note_chg']),int(request.POST['note_plus']),request.POST['note_sort'])
        la_time = f'<div class="la_time" onclick="Hello();"><h1>{la_time} </h1></div>'
        #m4_html = la_time +comp + comp2 + comp3 + comp4 +'<br>'+ utml + note_html + dtml
        m4_html = utml + la_time +comp +'<br>'+comp1 + comp2 + comp3 + comp4 + comp5+comp6+'<br><br><br>'+  note_html + dtml
        return HttpResponse(f'{m4_html}')
    else:
        1




@csrf_exempt
def m44(request):
    rsc = 'C:/REPORT/rep_raw'

    if request.method == "GET":
         test='겟'

         return HttpResponse(test)

    elif request.method == "POST":
    #if 1:
        #test='금호석유,30,7'
        test = request.POST['report']

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

        # print(list(rdf['날짜간격']))
        # print(list(rdf['날짜']))
        # time.sleep(9999)

        file_list = list(rdf['파일경로'])[0:limit_cnt]

        print(file_list)
        with zipfile.ZipFile(r"C:\Users\Jinu\PycharmProjects\WEB\WINT\mst/레포트.zip", 'w') as my_zip:
            for i in file_list:
                파일명 = str(i).replace(rsc,'').replace('.pdf','').replace('/','')

                if len(파일명.split('_')) == 3:
                    new_name = f'{파일명.split("_")[2][:8]}_{파일명.split("_")[2][8:]}_{파일명.split("_")[1]}_{파일명.split("_")[0]}.pdf'
                elif len(파일명.split('_')) == 4:
                    new_name = f'{파일명.split("_")[2][:8]}_{파일명.split("_")[2][8:]}_{파일명.split("_")[1]}_{파일명.split("_")[0]}.pdf'
                else:
                    new_name = '힝힝'

                my_zip.write(i,new_name)
        my_zip.close()

        fname = (f'report_"+{str(datetime.now()).split(".")[0]+"_"+str(stox)}_{limit_day}_{limit_cnt}')
        fname = urllib.parse.quote(fname.encode('utf-8'))
        #fname = fname.encode('utf-8')

        binary_file = open(r"C:\Users\Jinu\PycharmProjects\WEB\WINT\mst/레포트.zip", 'rb')
        response = HttpResponse(binary_file.read(), content_type="application/octet-stream; charset=utf-8")
        #response['Content-Disposition'] = f'attachment; filename="레포트_"+{str(datetime.now()).split(".")[0]+"_"+str(test)}.zip'
        #response['Content-Disposition'] = f'attachment; filename*=UTF-8""{fname}.zip'
        response['Content-Disposition'] =  'attachment;filename*=UTF-8\'\'%s.zip' % fname


        return response

    else:
        111



def m5(request):
    css_add = '''
    table {{}}
    
    '''

    yahoo_html,la_time = YAHOO()

    utml = basic_uml(kind_html)
    dtml = basic_dml()
    la_time = f'<div class="la_time"><h1>{la_time}</h1></div>'

    m5_html = la_time + utml + yahoo_html + dtml

    #print(m5_html)
    return HttpResponse(f'{m5_html}')

def m6(request):
    css_add = '''
    table {{}}
    
    '''

    m5_html = ''

    news_html,la_time = news()
    utml = basic_uml(kind_html)
    dtml = basic_dml()
    la_time = f'<div class="la_time"><h1>{la_time}</h1></div>'

    m6_html = la_time + utml + news_html + dtml

    return HttpResponse(f'{m6_html}')



@csrf_exempt
def reply2_main(request):
    #print(request)

    if request.method == "GET":
        res = m1(request)
        res = '겟겟'

        return HttpResponseRedirect("/m1/")

    elif request.method == "POST":

        new_dict = {}
        for i in range(1,16):
            con = str(request.POST[f'cond_{i}'])#.replace('\n','<br>')
            # print(con)
            # print('============')
            new_dict[i] = [i,con]


        new_df = pd.DataFrame(new_dict).T;  new_df.columns = ['번호','내용']

        new_df.to_pickle(os.path.join(r'C:\Users\Jinu\PycharmProjects\WEB\WINT\temp/','temp_m1_msg'+'.pickle'))
        #
        # rdf = pd.read_pickle(f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_reply2/cond.pickle')
        # print(rdf.info())

        tmsg = request.POST[f'cond_{request.POST["cond_kind"]}']

        res = str(tmsg)#.split('\r\n')

        # print(tmsg)
        # print('---')
        # print(str(tmsg))
        #
        reply2.main(str(tmsg),1,0)


        #        #
        binary_file = open(r"C:\Users\Jinu\PycharmProjects\CYB\practice\cond.xlsx", 'rb')
        response = HttpResponse(binary_file.read(), content_type="application/octet-stream; charset=utf-8")
        response['Content-Disposition'] = f'attachment; filename="cond_"+{str(datetime.now()).split(".")[0]+"_"+request.POST["cond_kind"]}.xlsx'
        #response.get()

        #return HttpResponse(f'{res}')
        return response



def bot3(mrow=100):
    try:
        fl = f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_MST2/MST_AL.pickle'
        data = pd.read_pickle(fl)
        last_time = datetime.fromtimestamp(os.path.getmtime(fl)).strftime('%m/%d     %H:%M')
    except:
        fl = f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_MST2/MST_AL.pickle'
        data = pd.read_pickle(fl)
        last_time = datetime.fromtimestamp(os.path.getmtime(fl)).strftime('%m/%d     %H:%M')

    mml = ''
    cntgg = 0

    #data.head(500).to_excel('xx_mst.xlsx')

    data['링크'] = data['종토링크'].apply(lambda x :  f"<a href='{str(x)}'>{'링크'}</a>" )

    col = ['알람@','등락','ST_등락','종목명_P','링크','체강구간_끝','체강','1고현폭','1현재폭','5고현폭','5현재폭','20고현폭','20현재폭','90고현폭','90현재폭','특표']
    col = ['알람@','등락','ST_등락','종목명_P','링크','체강구간_끝','체강','1고현폭','1현재폭']
    tcol = ['프로그램%','잠정외인%','잠정기관%','잠정법인%','총점_J','실적이슈','발표간격','7일외기법%','7일평단대비','30일외기법%','30일평단대비','섹터_B','섹터등급_B','진대','예대','특표','필터','양주체들_SE','음주체들_SE']

    #'외국계%'

    col = col + tcol

    BOT3 = data[col].head(mrow)


    BOT3 = df_style(BOT3)

    BOT3_html = str(BOT3.to_html(index=False,table_id='BOT3',escape=False))

    #print(BOT3)
    return [BOT3_html,last_time]

def plog_rest():
    fl = r'C:/Users/Jinu/PycharmProjects/CYB/JAMU/Source/PLOG_EX_ALL.pickle'
    #tdf = pd.read_pickle("C:/Users/Jinu/Desktop/작업쓰레기/__쓸모있음/MOVE_EX1.pickle")
    tdf = pd.read_pickle(fl)
    last_time = datetime.fromtimestamp(os.path.getmtime(fl)).strftime('%m/%d     %H:%M')

def plog():
    plog_html = ''
    global kind_lam
    global mst


    시작시간 = datetime.now()

    fl = r'C:/Users/Jinu/PycharmProjects/CYB/JAMU/Source/PLOG_EX_ALL.pickle'
    #tdf = pd.read_pickle("C:/Users/Jinu/Desktop/작업쓰레기/__쓸모있음/MOVE_EX1.pickle")
    tdf = pd.read_pickle(fl)
    #tdf.head(2).to_excel('xx_plog.xlsx')

    last_time = datetime.fromtimestamp(os.path.getmtime(fl)).strftime('%m/%d     %H:%M')

    tdf = tdf[(tdf['예대'] > 10)|(tdf['7일_대금평균'] > 15)]

    tdf = tdf[tdf['섹터등급_B'] != '제몰미']
    tdf = tdf[tdf['섹터등급_B'] != '6등급']


    tdf = pd.merge(tdf,mst[['종목명_P','코드_P','fn링크','종토링크','링크']].add_suffix('_mst'),left_on='종목명_P',right_on='종목명_P_mst', how='left')
    tdf['종목명+링크'] = tdf.apply(lambda x :  f"<a href='{str(x['링크_mst'])}'>{str('LINK')}</a>" , axis=1)
    tdf['종목명+fn링크'] = tdf.apply(lambda x :  f"<a href='{str(x['fn링크_mst'])}'>{str('LINK')}</a>" , axis=1)
    tdf['종목명+종토링크'] = tdf.apply(lambda x :  f"<a href='{str(x['종토링크_mst'])}'>{str('LINK')}</a>" , axis=1)

    k_dict = {

        '섹등':[['ST_등락','예대'], [False,False]],
        '섹롱폭':['ST_롱폭', False],

        '체상':['체결강도_M', False],
        '체하':['체결강도_M', True],

        '에너지':['에너지', False],
        '진/30':['진대/30일', False],
        '롱폭':['롱폭', False],
        '설현폭':['설현폭', False],
        '설순위':['설기간합', False],
        '설/30':['설기간합/30일', False],

        '외국계':['외국계$$/30일', False],
        '세투상':['필터에너지합순위_SE', True],

        '14수종':['14수종', False],
        '30수종':['30수종', False],

        '수급7일':['7일_외기법_시총대비_외기법', False],
        '수급30일':['30일_외기법_시총대비_외기법', False],

        '총점':[ ['총점_J','30수종'], [False,False] ],
        '발표':[ ['발표간격','30수종'], [True,False] ],

        '0등급':['진대', False],
        '1등급':['진대', False],
        '진대순위':['진대', False],

        '바텀':['30일_외기법_시총대비_외기법', False]
        # 컨상컨하
    }


    tdf[['1고현폭','1현재폭']] = tdf[['1고현폭','1현재폭']].replace(0,'')


    tgtg = {
            '체상':5,'체하':3,'섹등':2,'외국계':0.3,
        '진/30':0.5,'설/30':0.5,'섹롱폭':0.3,'롱폭':0.3,'설현폭':1,
        '14수종':2,'30수종':2,'수급7일':0.5,'수급30일':0.5,'세투상':0,
            '진대순위':0.1,'설순위':0.5,'에너지':0.2,'0등급':3,'1등급':0.2,
            '컨상':0,'컨하':0,'총점':0,'발표':0,'바텀':0.1
            }
    cuscol = ['종목명+종토링크','섹터_B','총점_J','실적이슈','종목명_P','1고현폭','1현재폭','예대','ST_등락','등락율_M','체결강도_M','체강구간_끝','외국계%','잠정기관%','프로그램%','발표간격','시총','필터점수']
    
    new_df = pd.DataFrame(columns = cuscol+list(tgtg.keys()))
    tdf['뉴인덱스'] = tdf['종목명_P'].copy()
    fil_df = tdf[tdf['필터']!=''].sort_values(by='필터점수', ascending=False).set_index('뉴인덱스',drop=True).head(120)


    for stx in fil_df.index:
        for tg in fil_df.loc[stx,'필터'].split(','):
            if tg in tgtg.keys():
                try:
                    #tfdf = fil_df[fil_df['필터'].str.contains(tg)]

                    #new_df.loc[stx,tg] = tgtg.get(tg,0)
                    new_df.loc[stx,tg] = tg
                except:
                    new_df.loc[stx,tg] = 9


    for stx in fil_df.index:
        for col in cuscol:
            new_df.loc[stx,col] = fil_df.loc[stx,col]




    new_df = new_df.fillna('').reset_index(drop=True)
    new_df['필터점수'] = np.round(new_df['필터점수'].astype(float),1)

    newdf = df_style(new_df)

    newdfml = str(newdf.to_html(index=False,table_id='plog_newdf',escape=False))

    plog_html += newdfml + '<br>'+'<br>'+'<br>'+'<br>'


    dicdf = pd.DataFrame(k_dict).T
    dicdf.columns = ['종류','옵션']

    #
    org_list = ['종목명+종토링크','섹터_B','총점_J','실적이슈','종목명_P','1고현폭','1현재폭'
        ,'예대','ST_등락','등락율_M','체결강도_M','체강구간_끝','7일평단대비','30일평단대비','외국계%','잠정기관%','프로그램%','7일외기법%','30일외기법%'
        ,'7일_외기법_시총대비_외기법','30일_외기법_시총대비_외기법','발표간격','섹터등급_B','30STO표','시총'
        ]


    tdf = tdf[~tdf['섹터_B'].str.contains('|'.join(['제외','제외2','몰라']))]


    for ky in list(k_dict.keys()): #reversed(list(k_dict.keys()))
        #print(k_dict.get(ky)[0],k_dict.get(ky)[1])

        tempdf = tdf[tdf['필터'].str.contains(ky)]

        try:tempdf = tempdf.sort_values(by=k_dict.get(ky)[0], ascending=k_dict.get(ky)[1]).head(15)
        except:tempdf = tdf.head(3)  #수정

        try:
            if k_dict.get(ky)[0] not in org_list:
                tempdf = tempdf[org_list+[k_dict.get(ky)[0]]+['양주체들_SE','음주체들_SE']]
            else:
                tempdf = tempdf[org_list+['양주체들_SE','음주체들_SE']]
        except:
            tempdf = tempdf[org_list+['양주체들_SE','음주체들_SE']]

        tempdf = df_style(tempdf)

        tempml = str(tempdf.to_html(index=False,table_id='plog_newdf',escape=False))

        plog_html += f'<div><font size="6rem" color="blue"><b>{"<br>"}{ky}</b></font></div><br>'+tempml

    plog_html += '<br>'+'<br>'+'<br>'+'<br>'
    return [plog_html,last_time]

def NOTE_today(ctr=9999,chg=0,plus=0,note_sort='-'):

    try:
        fl = f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_NOTE/{str(datetime.now())[:10]}.pickle'
        rdf = pd.read_pickle(fl)
        last_time = datetime.fromtimestamp(os.path.getmtime(fl)).strftime('%m/%d     %H:%M')
    except:
        fl = f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_NOTE/{str(datetime.now()-timedelta(days=1))[:10]}.pickle'
        rdf = pd.read_pickle(fl)
        last_time = datetime.fromtimestamp(os.path.getmtime(fl)).strftime('%m/%d     %H:%M')

    global mst
    rdf = pd.merge(rdf,mst[['종목명_P','코드_P','fn링크','종토링크','링크']].add_suffix('_mst'),left_on='종목명',right_on='종목명_P_mst', how='left')

    rdf = rdf[rdf['날짜간격'] <= ctr]
    
    if chg == 1:
        rdf = rdf[(~rdf['의견변경'].isin(['유지','없','신규']))|(~rdf['주가변경'].isin(['유지','없','신규']))]


    요일수 = datetime.today().weekday()
    기준변동 = plus


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

    TODAY = rdf[rdf['날짜간격'] <= todaycri]
    TODAY = TODAY.reset_index(drop=True)
    TODAY[TODAY.select_dtypes('category').columns] = TODAY[TODAY.select_dtypes('category').columns].astype('object')
    TODAY = TODAY.fillna(98765)
    TODAY[['1현재폭', '1고저폭', '20현재폭', '20고저폭', '90현재폭', '90고저폭', '변경율', '변등', 'REP간']] = TODAY[['1현재폭', '1고저폭', '20현재폭', '20고저폭', '90현재폭', '90고저폭', '변경율', '변등', 'REP간']].astype('int')
    TODAY['1일_총합'] = np.around(TODAY['1일_총합'], 1)
    TODAY = TODAY.replace(98765, '')

    TODAY = TODAY.sort_values(by=['7일_상승변등이후','1일_변등평','1일_총합','20일_변경율평', '7일_변경합', '1일_변경합', '20일_변경합','종목명', '날짜'],
                              ascending=[False, False, False, False, False, False, False, False, False])

    #TODAY['종목명링크'] = TODAY['종목명'].apply(lambda x :  f"<a href='{'https://finance.naver.com/item/main.naver?code='+str(x).replace('A','')}'>{str(x)}</a>" )
    TODAY['종목명+링크'] = TODAY.apply(lambda x :  f"<a href='{str(x['링크_mst'])}'>{str(x['종목명'])}</a>" , axis=1)
    TODAY['종목명+fn링크'] = TODAY.apply(lambda x :  f"<a href='{str(x['fn링크_mst'])}'>{str(x['종목명'])}</a>" , axis=1)
    TODAY['종목명+종토링크'] = TODAY.apply(lambda x :  f"<a href='{str(x['종토링크_mst'])}'>{str(x['종목명'])}</a>" , axis=1)
    # TODAY.to_excel('xx.xlsx')
    # os.system('xx.xlsx')

    try:
        TODAY['순서'] = TODAY[note_sort]
        TODAY.sort_values(by='순서',ascending=False)
    except:
        TODAY['순서'] = TODAY['7일_상승변등이후']
        TODAY.sort_values(by='순서',ascending=False)


    TODAY = TODAY.reset_index(drop=True)

    col_list = '7일_변등평,종목명,등락율_M,회사명,베스트,변등,변경율,REP간,의견변경,주가변경,업사,투자의견,날짜간격,오늘,1현재폭,1고저폭,20현재폭,20고저폭,90현재폭,90고저폭,REP사이날짜,종목명+종토링크,제목,날짜,서브날짜,목표주가,서브목표주가,그날가격,서브그날가격,다음key,서브key,7일_총합,1일_총합,총점,7일_상승변등이후'.split(',')


    TODAY = TODAY[col_list]
    TODAY['등락율_M'] = TODAY['등락율_M'].apply(lambda x : np.round(x,1) if type(x) == type(2.3) else str(x)  )

    #TODAY['링크'] = TODAY['코드_P'].apply(lambda x :  f"<a href='{'https://finance.naver.com/item/main.naver?code='+str(x).replace('A','')}'>{str(x)}</a>" )




    #TODAY['링크'] = TODAY['코드_P'].apply(lambda x :  f"'{'https://finance.naver.com/item/main.naver?code='+str(x).replace('A','')}'{str(x)}")

    #TODAY = TODAY.drop(['코드_P'], axis=1)


    TODAY = TODAY.applymap(lambda x: '*' if str(x) == '0' else x)
    TODAY = TODAY.applymap(lambda x: '' if str(x) == '_' else x)


    TODAY = df_style(TODAY)

    today_fill = lambda x : ['background-color:yellow' if x['오늘'].count('◆')>0 else "" for i in x ]
    TODAY = TODAY.style.apply(today_fill,subset=TODAY.columns,axis=1)
    #TODAY.to_excel('xx_today.xlsx')

    #note_html = str(TODAY.to_html(index=False,table_id='note', escape=False))
    note_html = str(TODAY.hide_index().to_html(table_uuid='note'))

    return [note_html,last_time]

def YAHOO():
    yahoo_html = ''
    tnum = 25


    # gemp = pd.read_pickle("C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_YAHOO_REST/gemp.pickle")
    # temp = pd.read_pickle("C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_YAHOO_REST/temp.pickle")
    # aemp = pd.read_pickle("C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_YAHOO_REST/aemp.pickle")

    yall = pd.read_pickle('C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_YAHOO_REST/'+'NOW_ALL'+'.pickle')
    ysec_글로벌 = pd.read_pickle('C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_YAHOO_REST/'+'NOW_SEC_'+'글로벌'+'.pickle')
    ysec_아시아 = pd.read_pickle('C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_YAHOO_REST/'+'NOW_SEC_'+'아시아'+'.pickle')


    fl_글로벌 = pd.read_pickle('C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_YAHOO_REST/'+'tar_df_f_글로벌'+'.pickle')
    fl_아시아 = pd.read_pickle('C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_YAHOO_REST/'+'tar_df_f_아시아'+'.pickle')


    last_time = datetime.fromtimestamp(os.path.getmtime('C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_YAHOO_REST/'+'NOW_SEC_'+'글로벌'+'.pickle')).strftime('%m/%d     %H:%M')

    ylist = [[ysec_글로벌,fl_글로벌,'글로벌'],[ysec_아시아,fl_아시아,'아시아']]

    #print(ytdf)
    #print(ysec)


    info_cnt = 999
    info_errcnt = 999
    tardf_cnt = 999

    #+str(tardf_cnt)+' '+str(info_cnt)+'-'+str(info_errcnt)
    s_cate = {
        ' 오늘♥♥ ':['등락_절대',False,'ST_등락_0','등락_0_정수'] #+str(len(all_code))
        ,' 20평대비 ◎◎ ':['평대비_20_절대',False,'ST_평대비_20','평대비_20_정수']
    }

    for yy in ylist:
        ysec = yy[0]
        ytdf = yy[1]
        kind = yy[2]

        for c in s_cate.keys():

            temp_ysec = ysec.sort_values(by=s_cate.get(c)[2], ascending=False)#.reset_index(drop=True)

            secdetail_dict = {}
            for i in ysec['산업_G'].unique():
                temp_sec = ysec[ysec['산업_G'] == i]
                temp_sec = temp_sec.sort_values(by=s_cate.get(c)[0], ascending=s_cate.get(c)[1]).reset_index(drop=True)
                #print(temp_sec)
                secdetail = ''

                if (i not in ['?','미분류','의료','??','기타','-999',-999]) & (len(temp_sec)>1) & (temp_sec.at[0,s_cate.get(c)[0]] > 0)  : #& (temp_sec.at[0,'ST_등락'] > 0)
                    dcnt = 0
                    for j in temp_sec.index:
                        dcnt += 1
                        if dcnt <= min(7,len(temp_sec)):
                            if temp_sec.at[j,s_cate.get(c)[3]] >= 1:
                                secdetail += str(temp_sec.at[j,'별명_M'])[:10] + '<font color="red"><b> ' + str(temp_sec.at[j,s_cate.get(c)[3]]) + '</b></font>' + '<font color="white">' + '호..' + '</font>'
                            elif temp_sec.at[j,s_cate.get(c)[3]] <= -1:
                                secdetail += str(temp_sec.at[j,'별명_M'])[:10] + '<font color="blue"><b> ' + str(temp_sec.at[j,s_cate.get(c)[3]]) + '</b></font>' + '<font color="white">' + '호..' + '</font>'
                            else:
                                secdetail += str(temp_sec.at[j,'별명_M'])[:10] + '<font color="black"><b> ' + str(temp_sec.at[j,s_cate.get(c)[3]]) + '</b></font>' + '<font color="white">' + '호..' + '</font>'

                    secdetail_dict[i] = secdetail

            temp_ysec['~~'] = '-'
            tg_col ='ST_등락_0_정수,ST_등락_1_정수,ST_등락_2_정수,ST_등락_3_정수,ST_등락_4_정수,~~,ST_평대비_5_정수,ST_평대비_20_정수,ST_평대비_60_정수,ST_평대비_120_정수,산업_G,ST_개수'.split(',')
            temp_ysec = temp_ysec[tg_col].drop_duplicates(keep='first')
            temp_ysec['디테일'] = temp_ysec['산업_G'].apply(lambda x: secdetail_dict.get(x,'-'))


            temp_ysec = temp_ysec[temp_ysec['ST_개수']>1]
            temp_ysec = temp_ysec[~temp_ysec['산업_G'].isin(['?','미분류','의료','??','기타','-999',-999])]

            if len(temp_ysec)>-1:

                temp_ysec = df_style(temp_ysec)

                temp_html = str(temp_ysec.to_html(index=False,table_id='yahoo',escape=False))

                yahoo_html += f'<div><font size="8rem"><b>{"<br>"}{str(kind)+"  "+c}</b></font></div>'+"<br>"+ temp_html+"<br>"

        cate = { #'#5평대비 거래변동상위':['5평대비_거래량',False]
            '#5평 대금상위':['평균대금_5',False]
            ,'#등락상위':['등락_0',False]
            , '#5평대비 등락상위':['평대비_5',False]
            , '#20평대비 등락상위':['평대비_20',False]
            , '#등락하위':['등락_0',True]
            , '#5평대비 등락하위':['평대비_5',True]
            , '#20평대비 등락하위':['평대비_20',True]
        }

        ytdf['~~'] = '-'
        tg_col = ['코드','등락_0_정수','등락_1_정수','등락_2_정수','등락_3_정수','등락_4_정수','~~','평대비_5_정수','평대비_20_정수','평대비_60_정수','평대비_120_정수'
            ,'현저_5_정수','고저_5_정수','고현_5_정수','현저_20_정수','고현_20_정수','현저_60_정수','고현_60_정수','현저_120_정수','고현_120_정수'
            ,'평균대금_5_정수','별명_M','산업_G','정보_M','최근날짜']

        #tg_col = ['코드','등락_0_정수','등락_1_정수','등락_2_정수','등락_3_정수','등락_4_정수','평대비_5_정수','평대비_20_정수','평대비_60_정수','평대비_120_정수'
        #    ,'현저_5_정수','고저_5_정수','현저_20_정수','고저_20_정수','현저_60_정수','고저_60_정수','평균대금_5_정수','최근날짜']

        final_dam = str(ytdf['날짜_0'].max()).replace('2022-','').replace('2023-','').replace('2024-','').replace('2025-','').replace('2026-','')

        #여
        for c in cate.keys():
            send_df = ytdf[ytdf['필터'].str.contains(str(c))]
            send_df = send_df.sort_values(by=cate.get(c)[0], ascending=cate.get(c)[1])
            send_df = send_df.head(tnum)

            send_df = send_df[tg_col]

            if len(send_df)>-1:

                send_df = df_style(send_df)

                temp_html = str(send_df.to_html(index=False,table_id='yahoo',escape=False))

                yahoo_html += f'<div><font size="8rem"><b>{"<br>"}{c}</b></font></div>'+"<br>"+ temp_html+"<br><br><br><br><br>"

    #print(yahoo_html)
    return [yahoo_html,last_time]

def news():
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

    nt = df_style(nt)
    NEWS23_html = str(nt.to_html(index=False,table_id='news', escape=False))

    
    n1['날짜'] = n1['날짜'].str.replace('2022.','').str.replace('2023.','').str.replace('2024.','').str.replace('2025.','').str.replace('2026.','')
    n1 = pd.merge(n1,mst[['종목명_P','코드_P','fn링크','종토링크','링크']].add_suffix('_mst'),left_on='종목명_N',right_on='종목명_P_mst', how='left')
    n1 = n1.sort_values(by=['날짜'], ascending=[False]).head(200).reset_index(drop = True)
    #n1['링크'] = n1['링크'].apply(lambda x :  f"<a href='{str(x)}'>{'링크'}</a>" )
    n1 = n1[n1['뉴스간격'] <= todaycri]


    n1['종목명+종토뉴스링크'] = n1.apply(lambda x :  f"<a href='{str(x['종토링크_mst'])}'>{str(x['종목명_N'])}</a>" , axis=1)
    n1['종목명+종토뉴스링크'] = n1['종목명+종토뉴스링크'].str.replace('board','news')

    n1 = n1[['종목명+종토뉴스링크','제목','뉴스간격','정보제공','날짜']]

    n1 = df_style(n1)
    NEWS1_html = str(n1.to_html(index=False,table_id='news', escape=False))



    NEWS_html += NEWS1_html +"<br><br><br><br>"+NEWS23_html
    return [NEWS_html,last_time]



def pdd(request):

    tempdf = '1'
    tat = len(tempdf)

    text = ''

    for i in tempdf.index:
        text += str(tempdf.at[i,'제목'])+ '</br>>'

    return HttpResponse(text)





def df_style(tdf):
    CSS참 = pd.read_pickle(r"C:\Users\Jinu\PycharmProjects\WEB\WINT\CSS참고.pickle")
    CSS컬럼 = CSS참[['컬럼','변경']].set_index('컬럼',drop=True).squeeze().to_dict()
    CSS표현 = CSS참[['컬럼','표현']].set_index('컬럼',drop=True).squeeze().to_dict()
    CSS서식 = CSS참[['컬럼','서식']].set_index('컬럼',drop=True).squeeze().to_dict()
    CSS정렬 = CSS참[['컬럼','정렬']].set_index('컬럼',drop=True).squeeze().to_dict()
    CSS넓이 = CSS참[['컬럼','넓이']].set_index('컬럼',drop=True).squeeze().to_dict()
    CSS클래스 = CSS참[['컬럼','클래스']].fillna('-').set_index('컬럼',drop=True).squeeze().to_dict()

    def int_change(x):
        try: y = int(float(x))
        except: y = x
        return y

    err_dict = {}
    for col in [x for x in tdf.columns if (str(CSS표현.get(str(x),'-')).find('정수')>-1)]:
        #print(col)
        #try:tdf[col] = tdf[col].astype('float').astype('int')
        tdf[[col]] = tdf[[col]].applymap(int_change)
        # try:tdf[[col]] = tdf[[col]].applymap(int_change)
        # except:err_dict[col] = 'err<br>'+str(CSS컬럼.get(col,''))

    for col in [x for x in tdf.columns if str(CSS클래스.get(str(x),'-')) not in ['-']]:
        tdf[col] = tdf[col].apply(lambda x: f'{CSS클래스.get(str(col)).replace("@",str(x))}'.replace("\n", "").replace("\t", ""))


    #<form id="정유" action="/kr_sec/" method="POST" onclick="document.getElementById('정유').submit();"><input type="hidden" name="정유" value="정유">정유</form>

    for col in tdf.columns:

        서식리스트 = str(CSS서식.get(col,'/')).split('/')
        #print(col,서식리스트,list(kind_lam.keys())[0])
        for tp in [ x for x in 서식리스트 if x in [y for y in kind_lam.keys()]]:
            #print(tp,col)
            #tdf[[col]].to_excel('xx.xlsx')
            #os.system('xx.xlsx')


            tdf[[col]] =tdf[[col]].applymap(kind_lam.get(tp)[1])
            #tdf[tp[0]] = tdf[tp[0]].apply(kind_lam.get())

            #print(tp,col,kind_lam.get(tp))
        #print(list(tdf[col]))
        #print(tdf[[col]].info())


    #잠시끔
    # for col in [x for x in tdf.columns if str(CSS정렬.get(str(x),'-')) in ['left','right','center']]:
    #     tdf[col] = tdf[col].apply(lambda x: f'<div class="{CSS정렬.get(str(col))}정렬">'+str(x)+'</div>')
    # for col in [x for x in tdf.columns if str(CSS넓이.get(str(x),'-')) in ['넓','좁','지킴','좌','우']]:
    #     tdf[col] = tdf[col].apply(lambda x: f'<div class="{CSS넓이.get(str(col))}">'+str(x)+'</div>')


    tdf.rename(columns=err_dict, inplace=True)
    tdf.rename(columns=CSS컬럼, inplace=True)

    return tdf



@csrf_exempt
def kr_stock(request):
    reshtml = ''


    mp = pd.read_pickle(r"C:\Users\Jinu\PycharmProjects\CYB\BATCH\MST_Batch.pickle")
    링딕 = mp[['종목명_P','종토링크','fn링크']].set_index('종목명_P').T.to_dict()

    # print(링딕.get('삼성전자').get('종토링크'))
    # return

    if request.method == "GET":
        test='겟'

        return HttpResponse(test)

    elif request.method == "POST":

        comp = f'''
    <form action='/m44/' method="post">
            <input type='hidden' name='report' value='{str(list(request.POST.keys())[0])+',150'+',10'}'>
            <input type='submit' value='레포트' style="font-size:2rem;witdh:6rem;;height:3rem">
    </form>
    <br>
    '''
        reshtml += comp + '<br>'



    #if 1:
        test = list(request.POST.keys())[0]
        #test = '금호석유'

        tams = '_'+str(test)+'_'


        jm = r"C:\Users\Jinu\PycharmProjects\CYB\JAMU\save\SUM" #SUM임
        fd = Path(__file__).resolve().parent.parent

        tlist = [ x for x in os.listdir(jm) if str(x).count(tams) > 0]

        if len(tlist) <=0 :
            fls = '--'
            ressrc = '--'
        else:
            # for jfl in tlist:
            #     shutil.copy(os.path.join(jm,jfl), os.path.join(fd,'static'))
            reshtml += f"""
                    <a class="rem2" href="{링딕.get(str(test)).get('fn링크')}"> {'fn링크  '}  </a>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <a class="rem2" href="{링딕.get(str(test)).get('종토링크')}""> {'종토  '}  </a>
                    <br><br><br><br><br>
                    """

            fls = os.listdir(r'C:\Users\Jinu\PycharmProjects\CYB\JAMU\save\SUM')
            #fls = os.listdir(os.path.join(fd,'mst','static','SUM'))
            for x in fls:
                if str(x).count(tams)>0:

                    try:ressrc = (f'../static/SUM/{str(x)}')
                    except:ressrc = '1'

                    reshtml += f'''
                    <img src="{ressrc}" alt={str(test)} width="80%">
                    '''

            # fls = os.listdir(r'C:\REPORT\rep_raw_web')
            # for x in fls:
            #     if str(x).count('하이닉스레포트')>0:
            #         try:ressrc = (f'../static/{str(x)}')
            #         except:ressrc = '1'
            #
            #
            #         #<img src="{ressrc}" alt={str(test)} width="80%">
            #         reshtml += f'''
            #         <embed src="{ressrc}" width="80%" />
            #        '''



        report_html = ''
        #레포트 리스트
        rsc = 'C:/REPORT/rep_raw'

        try:
            stox = test.split(',')[0]
            limit_day = int(test.split(',')[1])
            limit_cnt = int(test.split(',')[2])
        except:
            stox = test
            limit_day = 370
            limit_cnt = 50

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

        # print(list(rdf['날짜간격']))
        # print(list(rdf['날짜']))
        # time.sleep(9999)

        file_list = list(rdf['파일경로'])[0:limit_cnt]

        #여기
        for cnt,fl in enumerate(file_list):

            파일명 = fl.replace(rsc+"/","").replace('.pdf','')

            날짜 = 파일명.split('_')[2][2:8]
            시간 = 파일명.split('_')[2][8:12]
            종목명 = 파일명.split('_')[1]
            회사명 = 파일명.split('_')[0].replace('증권','').replace('투자','').replace('미래','')

            표시 = f'{날짜}_{회사명}_{시간}'

            report_html += f'<a href="../static/{str(fl).replace(rsc+"/","")}">{표시}</a>'+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
            if (cnt+1) % 4 == 0:
                report_html += '<br>'
            if (cnt+1) % 12 == 0:
                report_html += '<br>'

        report_html += '<br>' * 5

        utml = basic_uml(kind_html)
        dtml = basic_dml()

        #return HttpResponse(Templ(str(fd)+'<br>'+ressrc))
        return HttpResponse( utml  +'<br>'+ reshtml +'<br><br><br>'+ str(report_html) + dtml)


    else:
        111



@csrf_exempt
def kr_sec(request):
    reshtml = ''

    global mst


    if request.method == "GET":
        test='겟'

        return HttpResponse(test)

    elif request.method == "POST":

        comp = f'''
    '''
        reshtml += comp + '<br>'

        #if 1:
        test = list(request.POST.keys())[0]

        tmsg = f"""
@
섹터,{test}$호$호,포함
시총,0.1,이상
7대평,10,이상
@7대평,14수종,30수,14거%,30현,
@2@0@꾸잉@500
"""

        reply2.main(str(tmsg),0,1)

        #binary_file = pd.read_excel(r"C:\Users\Jinu\PycharmProjects\CYB\practice\cond_bef.xlsx")
        cond = pd.read_pickle(f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_reply2/cond.pickle')

        new = [x for x in cond.columns if x not in ['하이퍼']]
        cond = cond[new]

        binary_file = df_style(cond)

        reshtml = str(binary_file.to_html(index=False,table_id='kr_sec',escape=False))


        report_html = ''

        utml = basic_uml(kind_html)
        dtml = basic_dml()

        #return HttpResponse(Templ(str(fd)+'<br>'+ressrc))
        return HttpResponse( utml  +'<br>'+ reshtml +'<br><br><br>'+ str(report_html) + dtml)


    else:
        111




@csrf_exempt
def reply2_list(request):
    reshtml = ''
    if request.method == "GET":
        res = m0(request)
        res = '겟겟'
        return HttpResponseRedirect("/m0/")

    elif request.method == "POST":
        new_dict = {}
        for i in range(1,16):
            con = str(request.POST[f'cond_{i}'])#.replace('\n','<br>')
            # print(con)
            # print('============')
            new_dict[i] = [i,con]


        new_df = pd.DataFrame(new_dict).T;  new_df.columns = ['번호','내용']

        new_df.to_pickle(os.path.join(r'C:\Users\Jinu\PycharmProjects\WEB\WINT\temp/','temp_m1_msg'+'.pickle'))
        #
        # rdf = pd.read_pickle(f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_reply2/cond.pickle')
        # print(rdf.info())

        tmsg = request.POST[f'cond_{request.POST["cond_kind"]}']

        res = str(tmsg)#.split('\r\n')

        # print(tmsg)
        # print('---')
        # print(str(tmsg))
        #
        reply2.main(str(tmsg),1,1)


        chart_sc = request.POST['chart_sc']


        #tgdf = pd.read_excel(r"C:\Users\Jinu\PycharmProjects\CYB\practice\cond_bef.xlsx")
        tgdf = pd.read_pickle(f'C:/Users/Jinu/PycharmProjects/CYB/BATCH/MINE/WEB_reply2/cond.pickle')

        for sx in tgdf['종목']:
            tams = '_'+str(sx)+'_'

            jm = rf"C:\Users\Jinu\PycharmProjects\CYB\JAMU\save\{chart_sc}"
            fd = Path(__file__).resolve().parent.parent

            tlist = [ x for x in os.listdir(jm) if str(x).count(tams) > 0]

            if len(tlist) <=0 :
                fls = '--'
                ressrc = '--'
            else:

                fls = os.listdir(jm)
                for x in fls:
                    if str(x).count(tams)>0:
                        try:ressrc = (f'../static/{chart_sc}/{str(x)}')
                        except:ressrc = '1'

                        reshtml += f'''
                        <img src="{ressrc}" alt={str(sx)} width="80%">
                        <br><br><br><br><br><br><br><br><br><br>
                        '''


    return HttpResponse(reshtml)

@csrf_exempt
def one_report(request):
    rsc = 'C:/REPORT/rep_raw'

    if request.method == "GET":
        test='겟'
        return HttpResponse(test)

    elif request.method == "POST":
        #if 1:
        #test='금호석유'
        test = request.POST['report']

        rl = [ f for f in os.listdir(rsc) if (str(f).count('_'+str(test)+'_')>0) and (str(f).count('해당기업')<=0)]
        rdict = {}
        for r in rl:
            rdict[r] = [str(r).split('_')[0],str(r).split('_')[1],str(r).split('_')[2].replace('.pdf','')]

        rdf = pd.DataFrame(rdict).T.reset_index(drop=False)
        rdf.columns = ['파일명','회사명','종목','날짜']
        rdf = rdf.sort_values(by='날짜',ascending=False)
        rdf['파일경로'] = rdf['파일명'].apply(lambda x: rsc+"/"+str(x) )

        file_list = list(rdf['파일경로'])[0:1]
        print(file_list)
        with zipfile.ZipFile(r"C:\Users\Jinu\PycharmProjects\WEB\WINT\mst/레포트.zip", 'w') as my_zip:
            for i in file_list:
                my_zip.write(i,str(i).replace(rsc,''))
        my_zip.close()

        fname = (f'report_"+{str(datetime.now()).split(".")[0]+"_"+str(test)}')
        fname = urllib.parse.quote(fname.encode('utf-8'))
        #fname = fname.encode('utf-8')

        binary_file = open(r"C:\Users\Jinu\PycharmProjects\WEB\WINT\mst/레포트.zip", 'rb')
        response = HttpResponse(binary_file.read(), content_type="application/octet-stream; charset=utf-8")
        #response['Content-Disposition'] = f'attachment; filename="레포트_"+{str(datetime.now()).split(".")[0]+"_"+str(test)}.zip'
        #response['Content-Disposition'] = f'attachment; filename*=UTF-8""{fname}.zip'
        response['Content-Disposition'] =  'attachment;filename*=UTF-8\'\'%s.zip' % fname


        return response

    else:
        111




start = time.time()  # 시작 시간 저장

#plog()
#news()

#m3(1) #NOTE_today()
#YAHOO()
#NOTE_today(1)

#m44(1)

#kr_stock(1)

print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간



#plog()

#@csrf_exempt



#<img src="static\sum\0566_루트로닉__3000_4500.png" alt="루트로닉" width="80%">
#<img src="static\0245_성광벤드__3000_4500.png" alt="성광벤드" width="80%">
