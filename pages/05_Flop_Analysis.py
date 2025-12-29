import streamlit.components.v1 as components
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import numpy as np

st.set_page_config(page_title='Flop Analysis', page_icon="💪", layout="wide")

st.header('Flop Analysis') 

ktsy=0
a=5
dummy2=[]
dummy=[]
number=[]
liste=[5]
container=[]
#print('------------------------------------------------------')
for i in range(2,40):
 #print(i)
 liste.append(a)
 dummy.append(i)
 #dummy.append(liste.copy())
 
 liste_hesap=liste.copy()
 #ortalama kaybetme
 for ort in range(1,i):
  liste_hesap[ort]=0
  sapma= np.std(liste_hesap,ddof=0) 
 
  ortalama=np.mean(liste_hesap)
  
  cv2= sapma/ortalama
  cv2=cv2.round(4)
  cv2=cv2*1000
  cv2=cv2.round(0)
  dummy.append(cv2)
 container.append(dummy)
 #print(container)
 dummy=[] 
container=pd.DataFrame(container)

#-------------------------------------
#try: 
counter=0
linko='https://www.euroleaguebasketball.net//euroleague/teams//'
#1
#klüp bilgilerini al 


page = requests.get(linko)

soup = BeautifulSoup(page.content,"html.parser")

kk = soup.find(id="__NEXT_DATA__" )

for i in kk:
 soup=i

site_json=json.loads(soup.string)

kk=site_json['props']['pageProps']['clubs']['clubs']
df_clubs=pd.json_normalize(kk)


try:
 df_roster=[]
 df_roster=pd.DataFrame(df_roster)
 
 df_roster_dummy=[]
 df_roster_dummy=pd.DataFrame(df_roster_dummy)
 
 linko='https://www.euroleaguebasketball.net//euroleague/teams//'
  #1
  #klüp bilgilerini al 
  
 dummy_puan=[]
 df_hesap=[]
 #df_hesap=pd.DataFrame(df_hesap) 
 df_all=[]
 df_all=pd.DataFrame(df_all)
 page = requests.get(linko)
 
 soup = BeautifulSoup(page.content,"html.parser")
 
 kk = soup.find(id="__NEXT_DATA__" )
 
 for i in kk:
  soup=i
 
 site_json=json.loads(soup.string)
 
 kk=site_json['props']['pageProps']['clubs']['clubs']
 df_clubs=pd.json_normalize(kk)
 try:
  euro_img='https://media-cdn.incrowdsports.com/23610a1b-1c2e-4d2a-8fe4-ac2f8e400632.svg'
  st.image(euro_img,width=120)
  klup_list=df_clubs['crest'].values.tolist()
  
 except:
  pass 
 ' '
 ' ' 
 box1= df_clubs['name'].values.tolist()
 
 
 
 col1,col2 = st.columns([2.5,1])
 
 with col1:
  option = st.selectbox(
     'Select the team',
     (box1), key='1',index=None)
 
 
 if option !=None:
  
  resm=df_clubs.loc[df_clubs['name']==option].copy()
  resm=resm['crest'].values.tolist()
  st.image (resm[0],width=100)
  
  df_parca= df_clubs.loc[df_clubs['name']==option].copy()
  df_parca = df_parca['url'].values.tolist()[0]
  #df_parca= df_parca.replace('roster','games')
  #df_parca=df_parca.replace('/','//')
  
  
  linko_sezon= 'https://www.euroleaguebasketball.net'+ df_parca + '?season=2023-24'	
   
   
  page = requests.get(linko_sezon)
  
  soup = BeautifulSoup(page.content,"html.parser")
  
  kk = soup.find(id="__NEXT_DATA__" )
  
  
  for i in kk:
   soup=i
  
  site_json=json.loads(soup.string)
  
  #dict_keys(['hero', 'results', 'seasons', 'clubCode', 'clubName', 'club'])
  #dict_keys(['featuredGame', 'results', 'upcomingGames'])
  
  df_sezon= pd.json_normalize(site_json['props']['pageProps']['seasons'])
  
  box2=df_sezon['text'].values.tolist()
  test=box2[0]
  
  linko_results= 'https://www.euroleaguebasketball.net'+ df_parca + '?season='+ str(box2[0])	
  
  #1
  #klüp bilgilerini al 
  #linko='https://www.euroleaguebasketball.net/euroleague/teams/anadolu-efes-istanbul/roster/ist/?season=2022-23'
  
  
  page = requests.get(linko_results)
  
  soup = BeautifulSoup(page.content,"html.parser")
  
  kk = soup.find(id="__NEXT_DATA__" )
  
  for i in kk:
   soup=i
  
  site_json=json.loads(soup.string)
  #liste uzunluğu 5
  #son 2 liste numarası teknik ekip
  
  for tt in range(0,3): 
  
   kk=site_json['props']['pageProps']['roster'][tt]['players']
   pos= site_json['props']['pageProps']['roster'][tt]['groupTitle']
    
   for i in kk:
    df_roster_dummy=pd.json_normalize(i)
    df_roster_dummy['pos']=pos
    #df_roster= df_roster.append(df_roster_dummy)
    df_roster = pd.concat([df_roster, df_roster_dummy])  
  df_roster['namo']= df_roster['firstName']+ ' ' + df_roster['lastName'] + ' - ' + df_roster['pos']
  #st.dataframe(df_roster)
  
  box3= df_roster['namo'].values.tolist()
  #box3
  for oyuncu in box3:
   df_roster_parca= df_roster.loc[df_roster['namo']== oyuncu].copy()
   
   #st.dataframe(df_roster_parca)
   ilave= df_roster_parca['url'].values.tolist()[0]
   resm= df_roster_parca['cutoutImage'].values.tolist()[0]
   linko='https://www.euroleaguebasketball.net'+ ilave
   
   
   #1
   #klüp bilgilerini al 
   
   
   page = requests.get(linko)
   
   soup = BeautifulSoup(page.content,"html.parser")
   
   kk = soup.find(id="__NEXT_DATA__" )
   
   for i in kk:
    soup=i
   
   site_json=json.loads(soup.string)
   
   try:
    kk=site_json['props']['pageProps']['data']['stats']['currentSeason']['gameStats']
    
    ekle=[]
    
    
    #'alt başlık'
    #kk[0]['table']['sections'][0]['headings']
    
    
    for tt in range(0,6):
     dummy= kk[0]['table']['sections'][tt]['headings']
     ekle.append(dummy)
    
    #ekle
    dummy=[]
    
    
    
    
    for i in ekle:
     if len (i) != 1:
      for tt in i:
       dummy.append(tt)
     else :
      dummy.append(i[0])
        
    #dummy
    #'hafta rakip takım'
    #rakip takım 
    df_games=[]
    df_games=pd.DataFrame(df_games)
    #haftalar
    df_games2=[]
    df_games2=pd.DataFrame(df_games2)
    
    
    #zaman ve skor
    df_games3=[]
    
    #rebaund
    df_games4=[]
    
    #assists,steal,turnover
    df_games5=[]
    
    #blocks
    df_games6=[]
    
    #fauls
    df_games7=[]
    
    #pir
    df_games8=[]
       #df_games3=pd.DataFrame(df_games3)
    
    
    df_dummy=[]
    df_dummy=pd.DataFrame(df_dummy)
    uzunluk = len(kk[0]['table']['headSection']['stats'])
    
    for i in range(0,uzunluk-2):
     
     bir= kk[0]['table']['headSection']['stats'][i]['statSets']
     typo=bir[0]
     df_dummy=pd.json_normalize(typo)
     #df_games2=df_dummy.append(df_games2)
     df_games2 = pd.concat([df_dummy, df_games2])
    df_dummy=[] 
     
    for i in range(0,uzunluk-2):
     
     
     
     bir= kk[0]['table']['headSection']['stats'][i]['statSets']
     typo=bir[1]
     df_dummy=pd.json_normalize(typo)
     #df_games=df_dummy.append(df_games)
     df_games = pd.concat([df_dummy, df_games])
    
    df_games2.columns=['Round']
    
    df_games.drop(['statType'], inplace=True, axis=1)
    df_games.columns= ['Against']
    df_games=pd.concat([df_games2, df_games], axis=1)
    df_games['Round']=df_games['Round'].astype(int)
    
    df_games=df_games.sort_values(by='Round', ascending=True)
    
    #'ilk istatistik'
    #linko
    
    df_dummy.values.tolist()
    df_dummy=[] 
    
    
    
    #süre ve zaman
    
    uzunluk= len(kk[0]['table']['sections'][0]['stats'])
    
    for i in range(0,uzunluk-2):
     bir=kk[0]['table']['sections'][0]['stats'][i]['statSets']
     for tt in bir:
      x= list(tt.values())
      df_dummy.append(x[0])
     df_games3.append(df_dummy)
     df_dummy=[]
     
    df_games3=pd.DataFrame(df_games3) 
    df_games3.columns= kk[0]['table']['sections'][0]['headings']
    df_dummy=[]
    
    #rebaund
    
    uzunluk= len(kk[0]['table']['sections'][1]['stats'])
    
    for i in range(0,uzunluk-2):
     bir=kk[0]['table']['sections'][1]['stats'][i]['statSets']
     for tt in bir:
      x= list(tt.values())
      df_dummy.append(x[0])
     df_games4.append(df_dummy)
     df_dummy=[]
     
    df_games4=pd.DataFrame(df_games4) 
    df_games4.columns= kk[0]['table']['sections'][1]['headings']
    df_dummy=[]
    
    
    
    #Assist,steal,turnover
    
    uzunluk= len(kk[0]['table']['sections'][2]['stats'])
    
    for i in range(0,uzunluk-2):
     bir=kk[0]['table']['sections'][2]['stats'][i]['statSets']
     for tt in bir:
      x= list(tt.values())
      df_dummy.append(x[0])
     df_games5.append(df_dummy)
     df_dummy=[]
     
    df_games5=pd.DataFrame(df_games5) 
    df_games5.columns= kk[0]['table']['sections'][2]['headings']
    df_dummy=[]
    
    
    #Blocks
    uzunluk= len(kk[0]['table']['sections'][3]['stats'])
    
    
    for i in range(0,uzunluk-2):
     bir=kk[0]['table']['sections'][3]['stats'][i]['statSets']
     for tt in bir:
      x= list(tt.values())
      df_dummy.append(x[0])
     df_games6.append(df_dummy)
     df_dummy=[]
     
    df_games6=pd.DataFrame(df_games6) 
    df_games6.columns=kk[0]['table']['sections'][3]['headings']
    df_dummy=[]
    
    
    #Fauls
    uzunluk= len(kk[0]['table']['sections'][4]['stats'])
    
    
    for i in range(0,uzunluk-2):
     bir=kk[0]['table']['sections'][4]['stats'][i]['statSets']
     for tt in bir:
      x= list(tt.values())
      df_dummy.append(x[0])
     df_games7.append(df_dummy)
     df_dummy=[]
     
    df_games7=pd.DataFrame(df_games7) 
    df_games7.columns=kk[0]['table']['sections'][4]['headings']
    df_dummy=[]
    
    
    #PIR
    uzunluk= len(kk[0]['table']['sections'][4]['stats'])
    
    
    for i in range(0,uzunluk-2):
     bir=kk[0]['table']['sections'][5]['stats'][i]['statSets']
     for tt in bir:
      x= list(tt.values())
      df_dummy.append(x[0])
     df_games8.append(df_dummy)
     df_dummy=[]
     
    df_games8=pd.DataFrame(df_games8) 
    df_games8.columns=kk[0]['table']['sections'][5]['headings']
    df_dummy=[]
    df_games.reset_index(drop=True, inplace=True)
    df_games3.reset_index(drop=True, inplace=True)
    df_games4.reset_index(drop=True, inplace=True)
    df_games5.reset_index(drop=True, inplace=True)
    df_games6.reset_index(drop=True, inplace=True)
    df_games7.reset_index(drop=True, inplace=True)
    df_games8.reset_index(drop=True, inplace=True)
    
    
    
    df_games=pd.concat([df_games, df_games8], axis=1)
    
    df_games=pd.concat([df_games, df_games3], axis=1)
    df_games=pd.concat([df_games, df_games4], axis=1)
    df_games=pd.concat([df_games, df_games5], axis=1)
    df_games=pd.concat([df_games, df_games6], axis=1)
    df_games=pd.concat([df_games, df_games7], axis=1)
    
    df_games['Player']= oyuncu
    #st.dataframe(df_games)
    
    
    df_games['dakka']=df_games['Min'].astype(str).str[:2]
    df_games['dakka']=df_games['dakka'].replace(':','',regex=True)
    df_games['saniye']=df_games['Min'].astype(str).str[-2]
    df_games['dakka']=df_games['dakka'].astype(int)
    df_games['saniye']=df_games['saniye'].astype(int)
    df_games['Sure']= (df_games['dakka']*60+df_games['saniye'])/60
    df_games['Sure']= df_games['Sure'].astype(float)
    df_games['Sure']= df_games['Sure'].round(0)
    df_games=df_games[['Player','Sure','PIR']].copy()
    df_games.columns = ['Player','Minutes','PIR'] 
    df_games['PIR']=df_games['PIR'].astype(float)
    df_all=pd.concat([df_all, df_games])
    sapma= df_games['PIR'].std(ddof=0)
    ortalma= df_games['PIR'].mean()
    ortalma=round(ortalma,0)
    sapma=round(sapma,0)
    #st.dataframe(df_games)
    #ortalma
    #sapma  
    sapma_min= df_games['Minutes'].std(ddof=0)
    ortalma_min= df_games['Minutes'].mean()
    ortalma_min=round(ortalma_min,0)
    sapma_min=round(sapma_min,0)
    #st.dataframe(df_games)
    #ortalma_min
    #sapma_min  
    maxy=df_games['PIR'].max()
    top=len(df_games)
    z0=ortalma-(sapma/4)
    z1=ortalma-sapma
    z12=ortalma-(sapma/2)
    z11=ortalma-(sapma*1.5)
    df_games_last5= df_games.tail(5)
    df_games_last5=df_games_last5['PIR'].values.tolist()
    played=len(df_games)
    cv=sapma/ortalma
    cv=cv*1000
    cv=cv.round(0)
    
    container2=container.loc[container[container.columns[0]]==played].copy()
    st.dataframe(container2)
    #st.stop()
    if ortalma/sapma<2:
     df_games_est=df_games.loc[df_games['PIR']>=z11].copy()
    else:
     df_games_est=df_games.loc[df_games['PIR']>=z12].copy()
    ortalma_estimation= df_games_est['PIR'].mean()
    ortalma_estimation=round(ortalma_estimation)
    if ortalma/sapma>3:
     df_games=[]
     max_flop= ''
    elif ortalma/sapma<2:
     df_games=df_games.loc[df_games['PIR']<z12].copy()
     max_flop=z12 
    else:
     df_games=df_games.loc[df_games['PIR']<z1].copy()
     max_flop=z1
    #st.dataframe(df_games)
    #sapma
    
    flop=(len(df_games)/top)*100
    flop=round(flop)
    dummy_puan.append(oyuncu)
    dummy_puan.append(played)
    dummy_puan.append(sapma_min)
    dummy_puan.append(ortalma_min)
    dummy_puan.append(sapma)
    dummy_puan.append(ortalma)
    dummy_puan.append(flop)
    dummy_puan.append(cv)
    dummy_puan.append(ortalma_estimation)
    dummy_puan.append(df_games_last5)
    dummy_puan.append(max_flop)
    dummy_puan.append(maxy)
    
    df_hesap.append(dummy_puan)
    
    dummy_puan=[]
    
    
    #st.stop()
   except: 
    pass
  #df_hesap.sort_values(by=['PIR_Estimation'],ascending=False)
  df_hesap=pd.DataFrame(df_hesap) 
  df_hesap.columns=['Player','Played','Dakka_sd','Minute(Avrg)','PIR_sd','PIR(Avrg)','%Flop','cv','PIR_Expected','Last5_Games','PIR_Flop','PIR_Max']
  #df_hesap['PIR_Min']=df_hesap['PIR(Avrg)']-df_hesap['PIR_sd']
  #df_hesap['PIR_Max']=df_hesap['PIR(Avrg)']+df_hesap['PIR_sd']
  #df_hesap['PIR_Min']=df_hesap['PIR_Min'].astype(str)
  #df_hesap['PIR_Max']=df_hesap['PIR_Max'].astype(str)


  df_hesap=df_hesap[['Player','Played','Minute(Avrg)','PIR(Avrg)','%Flop','cv','PIR_Expected','PIR_Flop','PIR_Max','Last5_Games']].copy()
  #df_hesap['Oran']= df_hesap['PIR(Avrg)']/df_hesap['PIR_sd']
  #df_hesap['Oran']=df_hesap['Oran'].round(2)
  df_hesap=df_hesap.sort_values(by='PIR_Expected', ascending=False)
  st.dataframe(df_hesap)
  '%Flop        : Possibility of the player critically gains less PIR than usual.' 
  'PIR_Expected : Expected PIR when the player does not flop. '
  'PIR_Flop     : Upper PIR limit when the player flops. '
except:
 
 'An error occured. Check internet connecion and refresh the link.' 

takip= """
<!-- Default Statcounter code for flop_analysis
https://euroleaguestats.streamlit.app/ -->
<script type="text/javascript">
var sc_project=13185996; 
var sc_invisible=1; 
var sc_security="e2d9903d"; 
</script>
<script type="text/javascript"
src="https://www.statcounter.com/counter/counter.js"
async></script>
<noscript><div class="statcounter"><a title="Web Analytics
Made Easy - Statcounter" href="https://statcounter.com/"
target="_blank"><img class="statcounter"
src="https://c.statcounter.com/13185996/0/e2d9903d/1/"
alt="Web Analytics Made Easy - Statcounter"
referrerPolicy="no-referrer-when-downgrade"></a></div></noscript>
<!-- End of Statcounter Code -->
"""
#st.markdown(takip, unsafe_allow_html=True)  
components.html(takip,width=200, height=200)  
