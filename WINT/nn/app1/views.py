from django.shortcuts import render, HttpResponse
import pandas as pd
import os,sys


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
    tdf = pd.read_pickle("C:/Users/Jinu/Desktop/MOVE_EX1.pickle")
    return HttpResponse(f'{len(tdf)}')
def m2(request):
    tdf = pd.read_pickle("C:/Users/Jinu/Desktop/MOVE_EX1.pickle")
    return HttpResponse(f'{len(tdf)}')
def m3(request):
    tdf = pd.read_pickle("C:/Users/Jinu/Desktop/MOVE_EX1.pickle")
    return HttpResponse(f'{len(tdf)}')
def m4(request):
    tdf = pd.read_pickle("C:/Users/Jinu/Desktop/MOVE_EX1.pickle")
    return HttpResponse(f'{len(tdf)}')
def m5(request):
    tdf = pd.read_pickle("C:/Users/Jinu/Desktop/MOVE_EX1.pickle")
    return HttpResponse(f'{len(tdf)}')
def m6(request):
    tdf = pd.read_pickle("C:/Users/Jinu/Desktop/MOVE_EX1.pickle")
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
        fls = os.listdir(str(os.path.realpath(__file__)).replace('views.py','BU'))
        resfl = [ x for x in fls if str(x).find(tams) > -1][0]

        fls2 = os.listdir(r"C:\Users\Jinu\Desktop")
        resfl2 = [x for x in fls if str(x).find(tams) > -1][0]



        # try:ressrc = os.path.join('BU',str(resfl))
        # except:ressrc = '1'
        #
        # reshtml = f'''
        # <img src="{ressrc}" alt={str(request.POST['stock_name'])} width="80%">
        # <h6>{ressrc}</h6>
        # '''

        try:ressrc = os.path.join('static',str(resfl))
        except:ressrc = '1'

        try:ressrc2 = os.path.join(r"C:\Users\Jinu\Desktop",str(resfl2))
        except:ressrc2 = '2'

        reshtml = f'''
        <img src="{ressrc}" alt={str(request.POST['stock_name'])} width="80%">
        <h6>{fls}<br>{ressrc}</h6>
        <h6>{fls2}<br>{ressrc2}</h6>
        <img src="{ressrc2}" alt={str(request.POST['stock_name'])} width="80%">
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

    tempdf = pd.read_pickle(r"C:\Users\Jinu\Desktop\파이튜브\엔믹스\2022-10-26_엔믹스.pickle")
    tat = len(tempdf)

    text = ''

    for i in tempdf.index:
        text += str(tempdf.at[i,'제목'])+ '</br>>'

    return HttpResponse(text)

