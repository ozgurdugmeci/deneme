import plotly.graph_objects as go
import streamlit.components.v1 as components
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import plotly.express as px
from streamlit_plotly_events import plotly_events

try:
 fig = go.Figure()
 config = {'staticPlot': True}
 
 df_roster=[]
 df_roster=pd.DataFrame(df_roster)
 
 df_roster_dummy=[]
 df_roster_dummy=pd.DataFrame(df_roster_dummy)
 
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
  
  with col1:
   option3 = st.selectbox(
      'Select the player',
      (box3), key='3', index=None)
  
  if option3 != None:
   df_roster_parca= df_roster.loc[df_roster['namo']== option3].copy()
   
   
   ilave= df_roster_parca['url'].values.tolist()[0]
   resm= df_roster_parca['cutoutImage'].values.tolist()[0]
   # takım ve takıma göre oyuncu seçimi yapan seçim kutularını hazırla
   
   
   
   
    
   #------------------------------------------------
   linko='https://www.euroleaguebasketball.net'+ ilave
   
   
   #1
   #klüp bilgilerini al 
   
   
   page = requests.get(linko)
   
   soup = BeautifulSoup(page.content,"html.parser")
   
   kk = soup.find(id="__NEXT_DATA__" )
   
   for i in kk:
    soup=i
   
   site_json=json.loads(soup.string)
   
   kk=site_json['props']['pageProps']['data']['stats']['currentSeason']['gameStats']
   
   
   
   #üst başlıklar
   #kk[0]['table']['sections'][5]
   
   ekle=[]
   
   #'alt başlık'
   #kk[0]['table']['sections'][0]['headings']
   
   
   for tt in range(0,6):
    dummy= kk[0]['table']['sections'][tt]['headings']
    ekle.append(dummy)
   
   dummy=[]
   
   
   
   
   for i in ekle:
    if len (i) != 1:
     for tt in i:
      dummy.append(tt)
    else :
     dummy.append(i[0])
       
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
   df_graph=df_games.copy()
   df_graph.drop(['Against'], inplace=True, axis=1)
   df_graph.columns= ['Round','Player Index Rating']
   df_games=pd.concat([df_games, df_games3], axis=1)
   df_games=pd.concat([df_games, df_games4], axis=1)
   df_games=pd.concat([df_games, df_games5], axis=1)
   df_games=pd.concat([df_games, df_games6], axis=1)
   df_games=pd.concat([df_games, df_games7], axis=1)
   
   df_round=[]
   for i in range(1,35):
    df_round.append(i)
   
   df_round= pd.DataFrame(df_round) 
   df_round.columns=['Round'] 
   
   df_graph=pd.merge(df_round,df_graph,on=['Round'],how='left')
   df_graph.fillna(0,inplace=True)
   df_graph['Player Index Rating']=df_graph['Player Index Rating'].astype(int)
   
   st.subheader('Rating Graph')
   
   fig = px.bar(df_graph, x='Round', y='Player Index Rating',width=470, height=350  )  
   
   bol1,bol2,bol3 = st.columns([1,0.4,1])
   
   with bol1:
    st.plotly_chart(fig,config=config) 
   
   with bol3:
    try:
     st.image(resm,width=190,caption=option3 )
     
    except:
     pass 
   
   df_games=df_games.sort_values(by='Round', ascending=False)
     
   st.subheader('Game Stats') 
   st.dataframe(df_games, 800, 3000)
  
except:
  'Player has no stats.'
  #'An error occured. Check internet connecion and refresh the link.' 
 
 
takip= """
<!-- Default Statcounter code for playerrating
https://euroleagueplayerratings.streamlit.app/ -->
<script type="text/javascript">
var sc_project=12842016; 
var sc_invisible=1; 
var sc_security="0f9a4c8e"; 
</script>
<script type="text/javascript"
src="https://www.statcounter.com/counter/counter.js"
async></script>
<noscript><div class="statcounter"><a title="Web Analytics
Made Easy - Statcounter" href="https://statcounter.com/"
target="_blank"><img class="statcounter"
src="https://c.statcounter.com/12842016/0/0f9a4c8e/1/"
alt="Web Analytics Made Easy - Statcounter"
referrerPolicy="no-referrer-when-downgrade"></a></div></noscript>
<!-- End of Statcounter Code -->

"""
#st.markdown(takip, unsafe_allow_html=True)  
components.html(takip,width=200, height=200)  
