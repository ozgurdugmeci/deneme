import streamlit.components.v1 as components
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import plotly.express as px
import pandas as pd


st.set_page_config(page_title='Team Comparison', page_icon="🏀", layout="wide",initial_sidebar_state ='collapsed')




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
 euro_img='https://media-cdn.incrowdsports.com/23610a1b-1c2e-4d2a-8fe4-ac2f8e400632.svg'
 st.image(euro_img,width=120)
except:
 pass 
#st.title('Productive Five') -------- ----
' '
' ' 
box1= df_clubs['name'].values.tolist()



col1,col3,col2 = st.columns([3,6,3])

with col3:
 value1= st.slider(label='Last Games', min_value=1, max_value=38,step=1, key="l1")
 printox='Last ' + str(value1)+ ' games.' 
 if value1==1:
  
  printox='Last ' + str(value1)+ ' game.' 
 #printox
with col1:
 option = st.selectbox(
    'Select the team',
    (box1), key='1',index=None)


#------	
if option !=None:
  
 printo= option + ' seçilen'

 takm1=df_clubs.loc[df_clubs['name']==option].copy() 
 takm1=takm1['tvCode'].values.tolist()[0]
 
 #printo
 resm=df_clubs.loc[df_clubs['name']==option].copy()
 resm=resm['crest'].values.tolist()
 with col1:
  st.image (resm[0],width=120)

 df_parca= df_clubs.loc[df_clubs['name']==option].copy()
 df_parca = df_parca['url'].values.tolist()[0]
 df_parca= df_parca.replace('roster','games')
 df_parca=df_parca.replace('/','//')
 
 
 #2 
 #sezon bilgisini al qq
 #fikstür bilgisini al
 
 
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
 
 #with col1:
 # option2 = st.selectbox(
 #    'Select the season',
 #    (box2), key='2')'''
 
 df_team1=[]
 df_team1=pd.DataFrame(df_team1)
 df_team2=[]
 df_team2=pd.DataFrame(df_team2)

 linko_results= 'https://www.euroleaguebasketball.net'+ df_parca + '?season='+ str(box2[0])	
 
 page = requests.get(linko_results)
 
 soup = BeautifulSoup(page.content,"html.parser")
 
 kk = soup.find(id="__NEXT_DATA__" )
 
 for i in kk:
  soup=i
 
 site_json=json.loads(soup.string)
 	
 	
 df_results= pd.json_normalize(site_json['props']['pageProps']['results']['results'])
 df_results['home.score']= df_results['home.score'].astype(str)
 df_results['away.score'] = df_results['away.score'].astype(str)
 
 
 df_results['yeni'] = df_results['home.abbreviatedName'] + ' '+  df_results['home.score'] + ' - ' + df_results['away.abbreviatedName']+ ' ' +  df_results['away.score']  
 
 #df_results['yeni'] = df_results['home.score']+ '-' +df_results['away.score']
 #df_results.loc[(df_results['home.name']== option),'yeni2'] = 'vs-> ' +df_results['away.name'] +' ' + df_results['yeni']
 #df_results.loc[(df_results['home.name']!= option),'yeni2'] = 'at-> ' + df_results['home.name'] + ' ' +df_results['yeni']
 #df_results['yeni'] = df_results['yeni2']+ ' ' +df_results['away.score']
 box3= df_results['yeni'].values.tolist()

 #box3' ün son 5 sonucunu dök---------------------------------------
 #with col1:
 #box3
 deplasman=0 
 saha=0 
 uzunluk=len(box3)
 if value1> uzunluk:
  pass
 else:
  uzunluk=value1 
 away_win=0
 home_win=0
 for r in range(0,uzunluk):
  
  #st.dataframe(df_results)
  raw_game= df_results.loc[df_results['yeni']==box3[r]].copy() 
  link_game = raw_game['url'].values.tolist()
  #raw_game
  #'results'
  #link_game[0]	 
  link_game = link_game[0]
  link_game =link_game.replace('/','//')
  link_game= 'https://www.euroleaguebasketball.net' + link_game 
  page = requests.get(link_game)
  
  soup = BeautifulSoup(page.content,"html.parser")
  
  nn = soup.find(id="__NEXT_DATA__" )
  
  #-------
  for i in nn:
   soup=i
  #devamcddddddddddddddddddd ------------------------
  site_json=json.loads(soup.string)
  nn=site_json['props']
  
  nn=nn['pageProps']
  
  nn=nn['mappedData']
  name1=nn['rawGameInfo']['home']['name']
  name2=nn['rawGameInfo']['away']['name']
  name11=nn['rawGameInfo']['home']['abbreviatedName']
  name22=nn['rawGameInfo']['away']['abbreviatedName']
  df_h=nn['rawGameInfo']['home']['stats']
  df_a= nn['rawGameInfo']['away']['stats']
  
  
  
  #['code', 'name', 'abbreviatedName'] ----------- -----------
  df_h=pd.json_normalize(df_h)
  df_a=pd.json_normalize(df_a)

  df_h['Team1'] = name1
  df_h['Team'] = name11
  df_a['Team1'] = name2
  df_a['Team'] = name22
  if option == name1:
   #'home'
   scorey=raw_game['away.score'].values.tolist()[0]
   df_h['Points-']=scorey
   df_team1= pd.concat([df_team1, df_h])
   scorea=raw_game['home.score'].values.tolist()[0]
   saha=saha+1
   if scorea>scorey:
    home_win=home_win+1
	  
  else:
   #'away'
   deplasman=deplasman+1
   scorey=raw_game['home.score'].values.tolist()[0]
   scorea=raw_game['away.score'].values.tolist()[0]
   df_a['Points-']=scorey
   df_team1= pd.concat([df_team1, df_a])    
   if scorea>scorey:
     away_win=away_win+1
 top=saha+deplasman
 metin1= 'Home Games: ' + str(saha)
 metin2= 'Away Games: '  + str(deplasman)
 metin3= 'Home Wins: ' + str(home_win)
 metin4= 'Away Wins: ' + str(away_win)
 with col1:
  metin1
  metin2
  metin3
  metin4
 #if deplasman>0 :   
 #away_win=away_win/uzunluk
 #away_win=round(away_win,2)-------
  
  #away_win = "%" + str(away_win*100)
 #with col1:
 #'Away Wins%'
 #away_win
 #else:
 #with col1:
 #'Away Wins%'----------
 #'No away games.' 
 df_team1['All']='All'
 df_team1= df_team1[['points','Points-','assists','totalRebounds','turnovers','accuracyAttempted']].copy()
 df_team1.columns=['Points','Points-','Assists','Rebounds','Turnovers','TotalAttempt']
 df_team1['Points-']=df_team1['Points-'].astype(float)
 #st.dataframe(df_team1)

 df_team1['All'] = 'All'
 
 df_team1 = pd.pivot_table(df_team1, values=['Points','Points-','Assists','Rebounds','Turnovers','TotalAttempt'], index=['All'] ,aggfunc="sum") 
 df_team1 = df_team1.reset_index()                #index to columns ------------------  -------------------------------
 df_team1.drop(['All'], inplace=True, axis=1)
 
 uzunluk2=len(df_team1.columns) 
 
 for i in range(0,uzunluk2):
   
  df_team1[df_team1.columns[i]]= df_team1[df_team1.columns[i]]/uzunluk
  df_team1[df_team1.columns[i]]=df_team1[df_team1.columns[i]].round(0)

 
 
 #st.dataframe(df_team1)
 
# column2 starts-------------------------------

#try: 
counter=0


#st.title('Productive Five')
' '
' ' 
box1= df_clubs['name'].values.tolist()



#col1

with col2:
 optionto = st.selectbox(
  'Select the team',
  (box1), key='2',index=None)


	
if optionto !=None:
 
 printo= optionto + ' seçilen'
 #printo
 
 takm2=df_clubs.loc[df_clubs['name']==optionto].copy() 
 takm2=takm2['tvCode'].values.tolist()[0]

 
 resm=df_clubs.loc[df_clubs['name']==optionto].copy()
 resm=resm['crest'].values.tolist()
 with col2:
  st.image (resm[0],width=120)

 
 df_parca= df_clubs.loc[df_clubs['name']==optionto].copy()
 df_parca = df_parca['url'].values.tolist()[0]
 df_parca= df_parca.replace('roster','games')
 df_parca=df_parca.replace('/','//')
 
 
 #2 
 #sezon bilgisini al qq
 #fikstür bilgisini al
 
 
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
 
 #with col1:
 # option2 = st.selectbox(
 #    'Select the season',
 #    (box2), key='2')'''
 


 linko_results= 'https://www.euroleaguebasketball.net'+ df_parca + '?season='+ str(box2[0])	
 
 page = requests.get(linko_results)
 
 soup = BeautifulSoup(page.content,"html.parser")
 
 kk = soup.find(id="__NEXT_DATA__" )
 
 for i in kk:
  soup=i
 
 site_json=json.loads(soup.string)
 	
 	
 df_results= pd.json_normalize(site_json['props']['pageProps']['results']['results'])
 df_results['home.score']= df_results['home.score'].astype(str)
 df_results['away.score'] = df_results['away.score'].astype(str)
 
 
 df_results['yeni'] = df_results['home.abbreviatedName'] + ' '+  df_results['home.score'] + ' - ' + df_results['away.abbreviatedName']+ ' ' +  df_results['away.score']  
 
 #df_results['yeni'] = df_results['home.score']+ '-' +df_results['away.score']
 #df_results.loc[(df_results['home.name']== option),'yeni2'] = 'vs-> ' +df_results['away.name'] +' ' + df_results['yeni']
 #df_results.loc[(df_results['home.name']!= option),'yeni2'] = 'at-> ' + df_results['home.name'] + ' ' +df_results['yeni']
 #df_results['yeni'] = df_results['yeni2']+ ' ' +df_results['away.score']
 box3= df_results['yeni'].values.tolist()

 #col1 #box3' ün son 5 sonucunu dök-----------------------------------------------------
 #with col2:
 #box3
 deplasman=0   
 saha=0
 uzunluk=len(box3)
 away_win=0
 home_win=0
 if value1> uzunluk:
  pass
 else:
  uzunluk=value1 
 
 for r in range(0,uzunluk):
  
  #st.dataframe(df_results)
  raw_game= df_results.loc[df_results['yeni']==box3[r]].copy() 
  link_game = raw_game['url'].values.tolist()
  #raw_game
  #'results'
  #link_game[0]	 
  link_game = link_game[0]
  link_game =link_game.replace('/','//')
  link_game= 'https://www.euroleaguebasketball.net' + link_game 
  page = requests.get(link_game)
  
  soup = BeautifulSoup(page.content,"html.parser")
  
  nn = soup.find(id="__NEXT_DATA__" )
  
  #-------
  for i in nn:
   soup=i
  #devamcddddddddddddddddddd ------------------------
  site_json=json.loads(soup.string)
  nn=site_json['props']
  
  nn=nn['pageProps']
  
  nn=nn['mappedData']
  name1=nn['rawGameInfo']['home']['name']
  name2=nn['rawGameInfo']['away']['name']
  name11=nn['rawGameInfo']['home']['abbreviatedName']
  name22=nn['rawGameInfo']['away']['abbreviatedName']
  df_h=nn['rawGameInfo']['home']['stats']
  df_a= nn['rawGameInfo']['away']['stats']
  
  
  
  #['code', 'name', 'abbreviatedName'] ----------- -----------
  df_h=pd.json_normalize(df_h)
  df_a=pd.json_normalize(df_a)

  df_h['Team1'] = name1
  df_h['Team'] = name11
  df_a['Team1'] = name2
  df_a['Team'] = name22
  if optionto == name1:
   #'home'
   scorey=raw_game['away.score'].values.tolist()[0]
   df_h['Points-']=scorey
   df_team2= pd.concat([df_team2, df_h])
   scorea=raw_game['home.score'].values.tolist()[0]
   saha=saha+1
   if scorea>scorey:
     home_win=home_win+1
	 
  #df_team1 
  else:
   #'away'-------------------------
   deplasman=deplasman+1
   scorey=raw_game['home.score'].values.tolist()[0]
   scorea=raw_game['away.score'].values.tolist()[0]
   df_a['Points-']=scorey
   df_team2= pd.concat([df_team2, df_a])    
   if scorea>scorey:
     away_win=away_win+1
 
 top=saha+deplasman
 metin1= 'Home Games: ' + str(saha)
 metin2= 'Away Games: '  + str(deplasman)
 metin3= 'Home Wins: ' + str(home_win)
 metin4= 'Away Wins: ' + str(away_win)
 with col2: 
  metin1
  metin2
  metin3
  metin4
  
 #if deplasman>0 :
 #away_win=away_win/uzunluk
 #away_win=round(away_win,2) 
  
  
  #away_win = "%" + str(away_win*100)
  #with col2:
  #'Away Wins%'
  #away_win
 #else:
 #with col2:
 #'Away Wins%'
 #'No away games.' 
 df_team2['All']='All'
 df_team2= df_team2[['points','Points-','assists','totalRebounds','turnovers','accuracyAttempted']].copy()
 df_team2.columns=['Points','Points-','Assists','Rebounds','Turnovers','TotalAttempt']
 df_team2['Points-']=df_team2['Points-'].astype(float)
 #st.dataframe(df_team2)

 df_team2['All'] = 'All'
 
 df_team2 = pd.pivot_table(df_team2, values=['Points','Points-','Assists','Rebounds','Turnovers','TotalAttempt'], index=['All'] ,aggfunc="sum") 
 df_team2 = df_team2.reset_index()                #index to columns ----------
 df_team2.drop(['All'], inplace=True, axis=1)
 
 uzunluk2=len(df_team2.columns) 
 
 for i in range(0,uzunluk2):
   
  df_team2[df_team2.columns[i]]= df_team2[df_team2.columns[i]]/uzunluk
  df_team2[df_team2.columns[i]]=df_team2[df_team2.columns[i]].round(0)

if option != None and optionto != None :
 df_team1_orj= df_team1.copy()
 df_team2_orj= df_team2.copy()
 
 df_team1_orj= df_team1_orj.T
 df_team1_orj.columns=['Average']

 
 df_team2_orj= df_team2_orj.T
 df_team2_orj.columns=['Average']
 with col1:
  st.dataframe(df_team1_orj)
 with col2:
  st.dataframe(df_team2_orj)

 
 df_team1['Assists']= df_team1['Assists']*8
 df_team1['Rebounds']= df_team1['Rebounds']*3
 df_team1['Turnovers']= df_team1['Turnovers']*6

 df_team2['Assists']= df_team2['Assists']*8
 df_team2['Rebounds']= df_team2['Rebounds']*3
 df_team2['Turnovers']= df_team2['Turnovers']*6
 df_team1= df_team1.T
 df_team1.columns=['points']
 df_team1['Team'] = takm1
 
 df_team2= df_team2.T
 df_team2.columns=['points']
 df_team2['Team'] = takm2
 
 df_radar= pd.concat([df_team1, df_team2])
 df_radar = df_radar.reset_index()
 df_radar.columns=['Stats','Values','Teams']
 with col3:
  st.subheader('Comparison of '+printox)

 fig = px.line_polar(df_radar, r="Values",
                    theta="Stats",
                    color="Teams",
                    line_close=True,
                    color_discrete_sequence=["#00eb93", "#4ed2ff"],
                    template="plotly_dark" )

 fig.update_polars(angularaxis_showgrid=False,
                  radialaxis_gridwidth=0,
                  gridshape='linear',
                  bgcolor="#494b5a",
                  radialaxis_showticklabels=False
                  )

 fig.update_layout(
     paper_bgcolor="#494b5a",
     legend=dict(font=dict(size=12, color="white")),
     font=dict(size=12, color="white"),
     width=560,  # Set the width of the graph
     height=500)  # Set the height of the graph)
 
 with  col3:  
  config = {'staticPlot': True}
  st.plotly_chart(fig,config=config)

takip = """
<!-- Default Statcounter code for Euro_stats_compare
https://euroleaguestats.streamlit.app/ -->
<script type="text/javascript">
var sc_project=13046770; 
var sc_invisible=1; 
var sc_security="ee0f4109"; 
</script>
<script type="text/javascript"
src="https://www.statcounter.com/counter/counter.js"
async></script>
<noscript><div class="statcounter"><a title="Web Analytics"
href="https://statcounter.com/" target="_blank"><img
class="statcounter"
src="https://c.statcounter.com/13046770/0/ee0f4109/1/"
alt="Web Analytics"
referrerPolicy="no-referrer-when-downgrade"></a></div></noscript>
<!-- End of Statcounter Code -->"""
#st.markdown(takip, unsafe_allow_html=True)  
components.html(takip,width=200, height=200)  
