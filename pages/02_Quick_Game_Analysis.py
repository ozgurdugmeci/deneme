import streamlit.components.v1 as components
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import plotly.express as px
st.set_page_config(page_title='Game Analysis', page_icon="🥇", layout="wide")
#------------------------------------------------
#try: 
counter=0
linko='https://www.euroleaguebasketball.net//euroleague/teams//'
#1
#klüp bilgilerini al 

df_home=[]
df_home=pd.DataFrame(df_home)
df_away=[]
df_away=pd.DataFrame(df_away)

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
 
 #kol1,kol2,kol3,kol4,kol5,kol6,kol7,kol8,kol9 = st.columns(9)
 
 #tasarım1
 
 klup_list=df_clubs['crest'].values.tolist()
 #with kol1:
 # st.image(klup_list[0],width=30) 
 # st.image(klup_list[1],width=30)
   
 #with kol2:
 # st.image(klup_list[3],width=30) 
 # st.image(klup_list[4],width=30)
  
 #with kol3:
 # st.image(klup_list[6],width=30) 
 # st.image(klup_list[7],width=30)
  
 #with kol4:
 # st.image(klup_list[9],width=30) 
 # st.image(klup_list[10],width=30)
  
 #with kol5:
 # st.image(klup_list[12],width=30) 
 # st.image(klup_list[13],width=30)
  
 #with kol6:
 # st.image(klup_list[15],width=30) 
 # st.image(klup_list[16],width=30)
 
 #with kol7:
 # st.image(klup_list[2],width=30)
 # st.image(klup_list[5],width=30)
 #with kol8:
 # st.image(klup_list[8],width=30)
 # st.image(klup_list[11],width=30)
 #with kol9:
 # st.image(klup_list[17],width=30)
 # st.image(klup_list[14],width=30)
except:
 pass 
#st.title('Productive Five')
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
 df_parca= df_parca.replace('roster','games')
 df_parca=df_parca.replace('/','//')
 
 
 #2 
 #sezon bilgisini al
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
 
 with col1:
  option3 = st.selectbox ('Select the game', box3, key='3', index=None)
 
	
 if option3 != None:	
 	
 	
 	
  link_game= df_results.loc[df_results['yeni']==option3].copy() 
  link_game = link_game['url'].values.tolist()
  link_game = link_game[0]
  link_game =link_game.replace('/','//')
  link_game= 'https://www.euroleaguebasketball.net' + link_game 
  
  
  
  page = requests.get(link_game)
  
  soup = BeautifulSoup(page.content,"html.parser")
  
  xx = soup.find(id="__NEXT_DATA__" )
  
  
  
  
  df_home=[]
  df_home=pd.DataFrame(df_home)
  df_away=[]
  df_away=pd.DataFrame(df_away)
  
  for i in xx:
   soup=i
  
  site_json=json.loads(soup.string)
  
  ##-----RADAR----------------------------------------------
  secy = st.radio("Choose :",('Home Team','Away Team'))
  nn=site_json['props']
  
  nn=nn['pageProps']
  
  nn=nn['mappedData']
  name1=nn['rawGameInfo']['home']['name']
  name2=nn['rawGameInfo']['away']['name']
  name11=nn['rawGameInfo']['home']['abbreviatedName']
  name22=nn['rawGameInfo']['away']['abbreviatedName']
  df_h=nn['rawGameInfo']['home']['stats']
  df_a= nn['rawGameInfo']['away']['stats']
  
  #['code', 'name', 'abbreviatedName']
  df_h=pd.json_normalize(df_h)
  df_h['Team1'] = name1
  df_h['Team'] = name11
  df_a['Team1'] = name2
  df_a['Team'] = name22
  df_a=pd.json_normalize(df_a)
  #df_radar= pd.concat([df_h, df_a])
  #df_radar.drop(['Team1'], inplace=True, axis=1)
  df_h= df_h[['points','assists','totalRebounds','turnovers','accuracyAttempted']].copy()
  df_h.columns=['Points','Assists','Rebounds','Turnovers','ScoreAttempt']
  df_h['Assists']= df_h['Assists']*8
  df_h['Rebounds']= df_h['Rebounds']*3
  df_h['Turnovers']= df_h['Turnovers']*6
  df_a= df_a[['points','assists','totalRebounds','turnovers','accuracyAttempted']].copy()
  df_a.columns=['Points','Assists','Rebounds','Turnovers','ScoreAttempt']
  df_a['Assists']= df_a['Assists']*8
  df_a['Rebounds']= df_a['Rebounds']*3
  df_a['Turnovers']= df_a['Turnovers']*6

  
  df_h= df_h.T
  df_h.columns=['points']
  df_h['Team'] = name11
  df_a= df_a.T
  df_a.columns=['points']
  df_a['Team'] = name22
  df_radar= pd.concat([df_h, df_a])
  df_radar = df_radar.reset_index()
  df_radar.columns=['Stats','Values','Teams']
  
  st.subheader('Comparison >> '+ name11 + ' vs '+ name22)
  
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
  
  fig.update_layout(paper_bgcolor="#494b5a",legend=dict(font=dict(size=12, color="white")))
  fig.update_layout(font=dict(size=12, color="white"))
  config = {'staticPlot': True}
  
  st.plotly_chart(fig,config=config)

  
  
  
  #----RADAR ENDS------------------------------------------------
  xx=site_json['props']
  
  xx=xx['pageProps']
  
  
  xx=xx['mappedData']
  
  
  
  
  
  #quarter bilgisini al
  #ilk5 bilgilerini al
  quarters= xx['rawGameInfo']
  home=quarters['home']['code']
  away = quarters['away']['code']
  
  home=home.strip()
  away=away.strip()
  
  df_home= pd.json_normalize(quarters['home']['players'])
  df_away= pd.json_normalize(quarters['away']['players'])
  
  #code
  df_home['dorsal']=df_home['dorsal'].replace(to_replace='00',value='789')
  df_away['dorsal']=df_away['dorsal'].replace(to_replace='00',value='789')
  
  
  #df_home.loc[(df_home['code']=='011212'), 'dorsal'] = '789'
  #df_away.loc[(df_away['code']=='011212'), 'dorsal'] = '789'
  #P006590
  
  #010588
  
  #df_home.loc[(df_home['code']=='010588'), 'dorsal'] = '790'
  #df_away.loc[(df_away['code']=='010588'), 'dorsal'] = '790'
  
  
  df_home_ilk5= df_home.loc[df_home['startFive']==True].copy()
  df_away_ilk5= df_away.loc[df_away['startFive']==True].copy()
  
  if len(df_home_ilk5)!=5 or len(df_away_ilk5)!=5:
   st.write('Strating five data is problematic. Source has errors.')
   st.write('You can look for another game')
   st.stop()
  
  
  
  df_home_ilk5=df_home_ilk5[['jerseyName','dorsal','positionName','imageUrls.headshot']] 
  df_home_ilk5.columns = ['jerseyName','playerDorsal','positionName','imageUrls.headshot']
  df_home_ilk5['playerDorsal']= df_home_ilk5['playerDorsal'].astype(int)
  df_home_ilk5=df_home_ilk5.sort_values(by=['playerDorsal'])
  df_home_ilk5['playerDorsal']= df_home_ilk5['playerDorsal'].astype(str)
  
  
  df_home=df_home[['jerseyName','dorsal','positionName','imageUrls.headshot']] 
  df_home.columns = ['jerseyName','playerDorsal','positionName','imageUrls.headshot']
  
  df_away=df_away[['jerseyName','dorsal','positionName','imageUrls.headshot']] 
  df_away.columns = ['jerseyName','playerDorsal','positionName','imageUrls.headshot']
  
  
  
  key=df_home_ilk5['playerDorsal'].values.tolist()
  key= ''.join(key)
  df_home_ilk5['key']=key
  #home
  #st.dataframe(df_home_ilk5)
  
  df_away_ilk5=df_away_ilk5[['jerseyName','dorsal','positionName','imageUrls.headshot']] 
  df_away_ilk5.columns = ['jerseyName','playerDorsal','positionName','imageUrls.headshot']
  df_away_ilk5['playerDorsal']= df_away_ilk5['playerDorsal'].astype(int)
  df_away_ilk5=df_away_ilk5.sort_values(by=['playerDorsal'])
  df_away_ilk5['playerDorsal']= df_away_ilk5['playerDorsal'].astype(str)
  
  key=df_away_ilk5['playerDorsal'].values.tolist()
  key=''.join(key)
  df_away_ilk5['key']=key
  #away
  #st.dataframe(df_away_ilk5)
  
  
  
  quarters=quarters['home']
  quarters=quarters['quarters']
  
  quarters = pd.json_normalize(quarters)
  quarters.fillna('-',inplace=True)
  quarters=quarters.T
  quarters=quarters.loc[quarters[0]!='-'].copy()
  quarters=quarters.T
  quarters= quarters.columns
  
  
  
   
  xx=xx['playByPlay']
  df_all_plays=[]
  df_all_plays=pd.DataFrame(df_all_plays) 
  
  
  for i in quarters:
   i=i.replace('ot1','ot')
   q_plays=xx[i]
   df_dummy= pd.json_normalize(q_plays)
   df_dummy['markerTime'].fillna( '00:00', inplace=True)
   if i == 'q1':
    df_dummy['ceyrek'] = 'q1'
    
   elif i == 'q2':
    df_dummy['ceyrek'] = 'q2'
   elif i == 'q3':
    df_dummy['ceyrek'] = 'q3'
   elif i == 'q4':
    df_dummy['ceyrek'] = 'q4'
   elif i == 'ot':
    df_dummy['ceyrek'] = 'ot'
   #df_all_plays= df_all_plays.append(df_dummy)
   df_all_plays = pd.concat([df_all_plays, df_dummy])  
  
  #df_all_plays.loc[(df_all_plays['playerCode']=='P011212'), 'playerDorsal'] = '789'
  df_all_plays['playerDorsal']=df_all_plays['playerDorsal'].replace(to_replace='00',value='789')
  
  #P010588
  #P006590
  
  #df_all_plays.loc[(df_all_plays['playerCode']=='P010588'), 'playerDorsal'] = '790'
   
  uzunluk= df_all_plays['playNumber'].values.tolist()
  
  
  df_all_plays['playerName'].fillna(0, inplace=True)
  
  if len(quarters) ==4 :
   time_home=40*60
   time_away=40*60
  
   for i in uzunluk: 
    slice=df_all_plays.loc[df_all_plays['playNumber']==i].copy()
    slice=slice.values.tolist()
   
    #playNumber 0	playType 1	playInfo 2	teamCode 3	teamName 4	playerCode 5	playerName 6	playerDorsal 7	minute 8	markerTime 9
    slice=slice[0]
    if slice[16] =='q1':
     time=slice[9]
     time1 = time[:2]
     time2 = time[3:5]
     time = (int(time1)+ 30)*60 + int(time2)
     df_all_plays.loc[(df_all_plays['playNumber']==i), 'Second'] = time
    elif slice[16] =='q2':
     time=slice[9]
     time1 = time[:2]
     time2 = time[3:5]
     time = (int(time1)+ 20)*60 + int(time2)
     df_all_plays.loc[(df_all_plays['playNumber']==i), 'Second'] = time
  
    elif slice[16] =='q3':
     time=slice[9]
     time1 = time[:2]
     time2 = time[3:5]
     time = (int(time1)+ 10)*60 + int(time2)
     df_all_plays.loc[(df_all_plays['playNumber']==i), 'Second'] = time
    
    elif slice[16] =='q4':
     time=slice[9]
     time1 = time[:2]
     time2 = time[3:5]
     time = int(time1)*60 + int(time2)
     df_all_plays.loc[(df_all_plays['playNumber']==i), 'Second'] = time
      
     
  elif len(quarters)==5:
   time_home=45*60
   time_away=45*60
   for i in uzunluk: 
    slice=df_all_plays.loc[df_all_plays['playNumber']==i].copy()
    slice=slice.values.tolist()
   
    #playNumber 0	playType 1	playInfo 2	teamCode 3	teamName 4	playerCode 5	playerName 6	playerDorsal 7	minute 8	markerTime 9
    slice=slice[0]
    if slice[16] =='q1':
     time=slice[9]
     time1 = time[:2]
     time2 = time[3:5]
     time = (int(time1)+ 35)*60 + int(time2)
     df_all_plays.loc[(df_all_plays['playNumber']==i), 'Second'] = time
    elif slice[16] =='q2':
     time=slice[9]
     time1 = time[:2]
     time2 = time[3:5]
     time = (int(time1)+ 25)*60 + int(time2)
     df_all_plays.loc[(df_all_plays['playNumber']==i), 'Second'] = time
  
    elif slice[16] =='q3':
     time=slice[9]
     time1 = time[:2]
     time2 = time[3:5]
     time = (int(time1)+ 15)*60 + int(time2)
     df_all_plays.loc[(df_all_plays['playNumber']==i), 'Second'] = time
    
    elif slice[16] =='q4':
     time=slice[9]
     time1 = time[:2]
     time2 = time[3:5]
     time = (int(time1)+ 5)*60 + int(time2)
     df_all_plays.loc[(df_all_plays['playNumber']==i), 'Second'] = time
    elif slice[16] == 'ot' :
     time=slice[9]
     time1 = time[:2]
     time2 = time[3:5]
     time = int(time1)*60 + int(time2)
     df_all_plays.loc[(df_all_plays['playNumber']==i), 'Second'] = time
  
   
  else: 
   'Data misleading the stats, please chhose a different gamae'
   st.stop() 
  
  
  
  
  
  
  
  
  container_home=[]
  container_home=pd.DataFrame(container_home)
  
  
  container_away=[]
  container_away=pd.DataFrame(container_away)
  sub_home=0
  sub_away=0
  
  #Top_Puan
  top_puan_home=0
  top_puan_away=0
  
  df_home['Top_Puan']=0
  df_away['Top_Puan']=0
  df_home_ilk5['Top_Puan']=0
  df_away_ilk5['Top_Puan']=0
  
  #Sub_No
  df_home['Sub_No']=0
  df_away['Sub_No']=0
  df_home_ilk5['Sub_No']=0
  df_away_ilk5['Sub_No']=0
  
  
  #Süre
  df_home['Sure']=0
  df_away['Sure']=0
  df_home['markerTime']='10:00'
  df_away['markerTime']='10:00'
  df_home['Ceyrek']='q1'
  df_away['Ceyrek']='q1'
  
  
  df_home_ilk5['Sure']=0
  df_away_ilk5['Sure']=0
  df_home_ilk5['markerTime']='10:00'
  df_away_ilk5['markerTime']='10:00'
  df_home_ilk5['Ceyrek']='q1'
  df_away_ilk5['Ceyrek']='q1'
  
  
  #Score1
  df_home['Score1']='0-0'
  df_away['Score1']='0-0'
  df_home_ilk5['Score1']='0-0'
  df_away_ilk5['Score1']='0-0'
  
  
  #Score2
  df_home['Score2']='0-0'
  df_away['Score2']='0-0'
  df_home_ilk5['Score2']='0-0'
  df_away_ilk5['Score2']='0-0'
  
  
  
  #Difference
  df_home['Dif']=0
  df_away['Dif']=0
  df_home_ilk5['Dif']=0
  df_away_ilk5['Dif']=0
  
  #Difference
  df_home['Dif2']=0
  df_away['Dif2']=0
  df_home_ilk5['Dif2']=0
  df_away_ilk5['Dif2']=0
  
  
  
  #Score+
  df_home['Score+']=0
  df_away['Score+']=0
  df_home_ilk5['Score+']=0
  df_away_ilk5['Score+']=0
  
  #Score-
  df_home['Score-']=0
  df_away['Score-']=0
  df_home_ilk5['Score-']=0
  df_away_ilk5['Score-']=0
  score_neg_home=0
  score_neg_away=0
  
  score_home=0
  score_away=0
  
  #Blok
  df_home['Blok']=0
  df_away['Blok']=0
  df_home_ilk5['Blok']=0
  df_away_ilk5['Blok']=0
  
  
  
  #Steal
  df_home['Steal']=0
  df_away['Steal']=0
  df_home_ilk5['Steal']=0
  df_away_ilk5['Steal']=0
  
  
  #TurnOver
  df_home['TurnOver']=0
  df_away['TurnOver']=0
  df_home_ilk5['TurnOver']=0
  df_away_ilk5['TurnOver']=0
  
  #Rebaund
  df_home['Rebaund']=0
  df_away['Rebaund']=0
  df_home_ilk5['Rebaund']=0
  df_away_ilk5['Rebaund']=0
  
  #Assist
  df_home['Assist']=0
  df_away['Assist']=0
  df_home_ilk5['Assist']=0
  df_away_ilk5['Assist']=0
  
  
  
  #container_home=container_home.append(df_home_ilk5)
  #container_away=container_away.append(df_away_ilk5)
  container_home = pd.concat([container_home, df_home_ilk5])  
  container_away = pd.concat([container_away, df_away_ilk5]) 
  
  #df_home, df_home_ilk5 sütunlarını stats'lere göre ayarla
  
  for i in uzunluk:
   slice=df_all_plays.loc[df_all_plays['playNumber']==i].copy()
   slice=slice.values.tolist()
   
   #playNumber 0	playType 1	playInfo 2	teamCode 3	teamName 4	playerCode 5	playerName 6	playerDorsal 7	minute 8	markerTime 9
   slice=slice[0]
   
   #if type in ['BP','EG','EP','3FGM','2FGM','2FGA','3FGA','FTA','FTM','D','O','FV','AS','ST','TO','IN','OUT']:
   if slice[1] in ['IN'] :
    
    if slice[3].strip() == home:
     
     top_puan_home=0
     df_ekle= df_home.loc[df_home['playerDorsal']==slice[7]].copy()
     #df_home_ilk5= df_home_ilk5.append(df_ekle)
     df_home_ilk5 = pd.concat([df_home_ilk5, df_ekle])
     if len(df_home_ilk5)==5:
      sub_home=sub_home+1
      df_home_ilk5['Sub_No']=sub_home
      df_home_ilk5['playerDorsal']= df_home_ilk5['playerDorsal'].astype(int)
      df_home_ilk5=df_home_ilk5.sort_values(by=['playerDorsal'])
      df_home_ilk5['playerDorsal']= df_home_ilk5['playerDorsal'].astype(str)
      key=df_home_ilk5['playerDorsal'].values.tolist()
      key= ''.join(key)
      df_home_ilk5['key']=key
      #container_home=container_home.append(df_home_ilk5)
      container_home = pd.concat([container_home, df_home_ilk5])
      #st.dataframe(df_home_ilk5)
      #str(sub_home) + ' '+ home+ ' ' +str(slice[6]) + ' in'
  	
    else:
     
     top_puan_away=0
     df_ekle= df_away.loc[df_away['playerDorsal']==slice[7]].copy()
     #df_away_ilk5= df_away_ilk5.append(df_ekle)
     df_away_ilk5 = pd.concat([df_away_ilk5, df_ekle])
     if len(df_away_ilk5)==5:
      sub_away=sub_away+1
      df_away_ilk5['Sub_No']=sub_away	
      df_away_ilk5['playerDorsal']= df_away_ilk5['playerDorsal'].astype(int)
      df_away_ilk5=df_away_ilk5.sort_values(by=['playerDorsal'])
      df_away_ilk5['playerDorsal']= df_away_ilk5['playerDorsal'].astype(str)
      key=df_away_ilk5['playerDorsal'].values.tolist()
      key=''.join(key)
      df_away_ilk5['key']=key
      #container_away=container_away.append(df_away_ilk5)
      container_away = pd.concat([container_away, df_away_ilk5])
      #st.dataframe(df_away_ilk5)
      #str(sub_away) + ' ' + away + ' ' + str(slice[6]) + ' in' 
  	
   elif slice[1] in ['OUT']:
    if slice[3].strip() == home:
     
     top_puan_home=0
     df_home_ilk5= df_home_ilk5.loc[df_home_ilk5['playerDorsal']!=slice[7]].copy()
     if len(df_home_ilk5)==5:
      sub_home=sub_home+1
      df_home_ilk5['Sub_No']=sub_home
      df_home_ilk5['playerDorsal']= df_home_ilk5['playerDorsal'].astype(int)
      df_home_ilk5=df_home_ilk5.sort_values(by=['playerDorsal'])
      df_home_ilk5['playerDorsal']= df_home_ilk5['playerDorsal'].astype(str)
      key=df_home_ilk5['playerDorsal'].values.tolist()
      key= ''.join(key)
      df_home_ilk5['key']=key
      #container_home=container_home.append(df_home_ilk5)
      container_home = pd.concat([container_home, df_home_ilk5])
      #st.dataframe(df_home_ilk5)
      #str(sub_home) + ' '+ home+ ' ' +str(slice[6]) + ' out'
  	
    else:
     
     top_puan_away=0
     df_away_ilk5= df_away_ilk5.loc[df_away_ilk5['playerDorsal']!=slice[7]].copy()
     if len(df_away_ilk5)==5:
      sub_away=sub_away+1
      df_away_ilk5['Sub_No']=sub_away	
      df_away_ilk5['playerDorsal']= df_away_ilk5['playerDorsal'].astype(int)
      df_away_ilk5=df_away_ilk5.sort_values(by=['playerDorsal'])
      df_away_ilk5['playerDorsal']= df_away_ilk5['playerDorsal'].astype(str)
      key=df_away_ilk5['playerDorsal'].values.tolist()
      key=''.join(key)
      df_away_ilk5['key']=key
      #container_away=container_away.append(df_away_ilk5)
      container_away = pd.concat([container_away, df_away_ilk5])
      #st.dataframe(df_away_ilk5)
      #str(sub_away) + ' ' + away + ' ' + str(slice[6]) + ' out'
  
  
    
  df_home_ilk5= container_home.loc[container_home['Sub_No']==0].copy()	
  df_away_ilk5= container_away.loc[container_away['Sub_No']==0].copy()	
  
  dummyy_sub_home=0
  dummyy_sub_away=0
  
  sub_counter_home=0
  sub_counter_away=0
  
  container_final_home=[]
  container_final_home= pd.DataFrame(container_final_home)
  container_final_away=[]
  container_final_away= pd.DataFrame(container_final_away)
  
  
  	
  #dongu_= container_home['Sub_No'].max()
  for i in uzunluk:
   slice=df_all_plays.loc[df_all_plays['playNumber']==i].copy()
   slice=slice.values.tolist()
   
   #playNumber 0	playType 1	playInfo 2	teamCode 3	teamName 4	playerCode 5	playerName 6	playerDorsal 7	minute 8	markerTime 9 ceyrek 16 Second 17
   slice=slice[0]
   
   #if type in ['BP','EG','EP','3FGM','2FGM','2FGA','3FGA','FTA','FTM','D','O','FV','AS','ST','TO','IN','OUT']:
   
   if slice[1].strip() in ['3FGM'] :
    if slice[3].strip()== home:
     score_home=score_home+3
     score_neg_away=score_neg_away+3
     df_away_ilk5['Score-']=score_neg_away   
     top_puan_home=top_puan_home+3
     df_home_ilk5['Top_Puan']=top_puan_home
     pick=slice[7]
     try:
      dilim=df_home_ilk5.loc[df_home_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'Score+']
      df_home_ilk5.loc[(df_home_ilk5['playerDorsal']==pick),'Score+']= score_add+3
     except:
      pass
    else:
     score_away=score_away+3
     score_neg_home=score_neg_home+3
     df_home_ilk5['Score-']= score_neg_home   
     top_puan_away=top_puan_away+3
     df_away_ilk5['Top_Puan']=top_puan_away
     pick=slice[7]
     try:
      dilim=df_away_ilk5.loc[df_away_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'Score+']
      df_away_ilk5.loc[(df_away_ilk5['playerDorsal']==pick),'Score+']= score_add+3
     except:
      pass 
  
   
   elif slice[1].strip() in ['2FGM'] :
    if slice[3].strip()== home:
     score_home=score_home+2
     score_neg_away=score_neg_away+2
     df_away_ilk5['Score-']=score_neg_away  
     top_puan_home=top_puan_home+2
     df_home_ilk5['Top_Puan']=top_puan_home
     pick=slice[7]
     try:
      dilim=df_home_ilk5.loc[df_home_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'Score+']
      df_home_ilk5.loc[(df_home_ilk5['playerDorsal']==pick),'Score+']= score_add+2
     except:
      pass
    else:
     score_away=score_away+2
     score_neg_home=score_neg_home+2
     df_home_ilk5['Score-']= score_neg_home   
     top_puan_away=top_puan_away+2
     df_away_ilk5['Top_Puan']=top_puan_away
     pick=slice[7].strip()
     try:
      dilim=df_away_ilk5.loc[df_away_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'Score+']
      df_away_ilk5.loc[(df_away_ilk5['playerDorsal']==pick),'Score+']= score_add+2
     except:
      pass 
  
   elif slice[1].strip() in ['FTM'] :
    if slice[3].strip()== home:
     score_home=score_home+1
     score_neg_away=score_neg_away+1
     df_away_ilk5['Score-']=score_neg_away  
     top_puan_home=top_puan_home+1
     df_home_ilk5['Top_Puan']=top_puan_home
     pick=slice[7]
     try:
      dilim=df_home_ilk5.loc[df_home_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'Score+']
      df_home_ilk5.loc[(df_home_ilk5['playerDorsal']==pick),'Score+']= score_add+1
     except:
      pass
    else:
     score_away=score_away+1
     score_neg_home=score_neg_home+1
     df_home_ilk5['Score-']= score_neg_home   
     top_puan_away=top_puan_away+1
     df_away_ilk5['Top_Puan']=top_puan_away
     pick=slice[7]
     try:
      dilim=df_away_ilk5.loc[df_away_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'Score+']
      df_away_ilk5.loc[(df_away_ilk5['playerDorsal']==pick),'Score+']= score_add+1
     except:
      pass 
   
   elif slice[1].strip() in ['FV'] :
    if slice[3]== home: 
     top_puan_home=top_puan_home+1
     df_home_ilk5['Top_Puan']=top_puan_home
     pick=slice[7]
     try:
      dilim=df_home_ilk5.loc[df_home_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'Blok']
      df_home_ilk5.loc[(df_home_ilk5['playerDorsal']==pick),'Blok']= score_add+1
     except:
      pass
    else:
     top_puan_away=top_puan_away+1
     df_away_ilk5['Top_Puan']=top_puan_away
     pick=slice[7]
     try:
      dilim=df_away_ilk5.loc[df_away_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'Blok']
      df_away_ilk5.loc[(df_away_ilk5['playerDorsal']==pick),'Blok']= score_add+1
     except:
      pass
  
    
   elif slice[1].strip() in ['ST'] :
    if slice[3]== home: 
     top_puan_home=top_puan_home+1
     df_home_ilk5['Top_Puan']=top_puan_home
     pick=slice[7]
     try:
      dilim=df_home_ilk5.loc[df_home_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'Steal']
      df_home_ilk5.loc[(df_home_ilk5['playerDorsal']==pick),'Steal']= score_add+1
     except:
      pass
    else:
     top_puan_away=top_puan_away+1
     df_away_ilk5['Top_Puan']=top_puan_away
     pick=slice[7]
     try:
      dilim=df_away_ilk5.loc[df_away_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'Steal']
      df_away_ilk5.loc[(df_away_ilk5['playerDorsal']==pick),'Steal']= score_add+1
     except:
      pass
   
   elif slice[1].strip() in ['TO'] :
    if slice[3]== home: 
     top_puan_home=top_puan_home-1
     df_home_ilk5['Top_Puan']=top_puan_home
     pick=slice[7]
     try:
      dilim=df_home_ilk5.loc[df_home_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'TurnOver']
      df_home_ilk5.loc[(df_home_ilk5['playerDorsal']==pick),'TurnOver']= score_add+1
     except:
      pass
    else:
     top_puan_away=top_puan_away-1
     df_away_ilk5['Top_Puan']=top_puan_away
     pick=slice[7]
     try:
      dilim=df_away_ilk5.loc[df_away_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'TurnOver']
      df_away_ilk5.loc[(df_away_ilk5['playerDorsal']==pick),'TurnOver']= score_add+1
     except:
      pass
   
   
   elif slice[1].strip() in ['O','D'] :
    if slice[3]== home: 
     top_puan_home=top_puan_home+1
     df_home_ilk5['Top_Puan']=top_puan_home
     pick=slice[7]
     try:
      dilim=df_home_ilk5.loc[df_home_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'Rebaund']
      df_home_ilk5.loc[(df_home_ilk5['playerDorsal']==pick),'Rebaund']= score_add+1
     except:
      pass
    else:
     top_puan_away=top_puan_away+1
     df_away_ilk5['Top_Puan']=top_puan_away
     pick=slice[7]
     try:
      dilim=df_away_ilk5.loc[df_away_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'Rebaund']
      df_away_ilk5.loc[(df_away_ilk5['playerDorsal']==pick),'Rebaund']= score_add+1
     except:
      pass
  
   
   elif slice[1].strip() in ['AS'] :
    if slice[3].strip()== home: 
     top_puan_home=top_puan_home+1
     df_home_ilk5['Top_Puan']=top_puan_home
     pick=slice[7]
     try:
      dilim=df_home_ilk5.loc[df_home_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'Assist']
      df_home_ilk5.loc[(df_home_ilk5['playerDorsal']==pick),'Assist']= score_add+1
     except:
      pass
    else:
     top_puan_away=top_puan_away+1
     df_away_ilk5['Top_Puan']=top_puan_away
     pick=slice[7]
     try:
      dilim=df_away_ilk5.loc[df_away_ilk5['playerDorsal']== pick ].copy()
      indy=list(dilim.index)[0]
      score_add= dilim.at [indy,'Assist']
      df_away_ilk5.loc[(df_away_ilk5['playerDorsal']==pick),'Assist']= score_add+1
     except:
      pass
   elif slice[1].strip() in ['IN'] :
    if slice[3] == home:	
     dummyy_sub_home=dummyy_sub_home + 1
     if dummyy_sub_home==0:
      #sub_counter_home
      
      
      sure=time_home-slice[17]
      time_home= slice[17]
      df_home_ilk5['Sure']= sure
      df_home_ilk5['Dif2'] = score_home-score_away
      df_home_ilk5['Score2'] = str(score_home)+ '-' + str(score_away)
      df_home_ilk5['Top_Puan']= df_home_ilk5['Top_Puan']- df_home_ilk5['Score-']
      
      #st.dataframe(df_home_ilk5)
      sub_counter_home=sub_counter_home+1
      #container_final_home=container_final_home.append(df_home_ilk5)
      container_final_home = pd.concat([container_final_home, df_home_ilk5])
      df_home_ilk5= container_home.loc[container_home['Sub_No']== sub_counter_home].copy()
      df_home_ilk5['markerTime']= slice[9]
      df_home_ilk5['Ceyrek']= slice[16]
      df_home_ilk5['Dif'] = score_home-score_away	 
      df_home_ilk5['Score1'] = str(score_home)+ '-' + str(score_away)
      top_puan_home=0
      score_neg_home=0
      
    else :
     dummyy_sub_away=dummyy_sub_away + 1
     if dummyy_sub_away==0:
      #sub_counter_away
      
      
      sure=time_away-slice[17]
      time_away= slice[17]
      df_away_ilk5['Sure']= sure
      df_away_ilk5['Dif2'] = score_away-score_home
      df_away_ilk5['Score2'] = str(score_home)+ '-' + str(score_away)
      df_away_ilk5['Top_Puan']= df_away_ilk5['Top_Puan']- df_away_ilk5['Score-']
      #st.dataframe(df_away_ilk5)
      sub_counter_away=sub_counter_away+1
      #container_final_away=container_final_away.append(df_away_ilk5)
      container_final_away = pd.concat([container_final_away, df_away_ilk5])
      df_away_ilk5= container_away.loc[container_away['Sub_No']== sub_counter_away].copy()
      df_away_ilk5['markerTime']= slice[9]
      df_away_ilk5['Ceyrek']= slice[16]
      df_away_ilk5['Dif'] = score_away-score_home
      df_away_ilk5['Score1'] = str(score_home)+ '-' + str(score_away)	
      top_puan_away=0
      score_neg_away=0
      
      
   elif slice[1].strip() in ['OUT'] :
    if slice[3]== home:	
     dummyy_sub_home=dummyy_sub_home - 1
     if dummyy_sub_home==0:
      #sub_counter_home
      
      
      sure=time_home-slice[17]
      time_home= slice[17]
      df_home_ilk5['Sure']= sure
      df_home_ilk5['Dif2'] = score_home-score_away
      df_home_ilk5['Score2'] = str(score_home)+ '-' + str(score_away)
      df_home_ilk5['Top_Puan']= df_home_ilk5['Top_Puan']- df_home_ilk5['Score-']
      
      #st.dataframe(df_home_ilk5)
      sub_counter_home=sub_counter_home+1
      #container_final_home=container_final_home.append(df_home_ilk5)
      container_final_home = pd.concat([container_final_home, df_home_ilk5])
 	 
      df_home_ilk5= container_home.loc[container_home['Sub_No']== sub_counter_home].copy()
      df_home_ilk5['markerTime']= slice[9]
      df_home_ilk5['Ceyrek']= slice[16]
      df_home_ilk5['Dif'] = score_home-score_away
      df_home_ilk5['Score1'] = str(score_home)+ '-' + str(score_away)	
      top_puan_home=0
      score_neg_home=0
      
      
    else :
     dummyy_sub_away=dummyy_sub_away - 1
     if dummyy_sub_away==0:
      #sub_counter_away
      
      
      sure=time_away-slice[17]
      time_away= slice[17]
      df_away_ilk5['Sure']= sure
      df_away_ilk5['Dif2'] = score_away-score_home
      df_away_ilk5['Score2'] = str(score_home)+ '-' + str(score_away)
      df_away_ilk5['Top_Puan']= df_away_ilk5['Top_Puan']- df_away_ilk5['Score-']
      #st.dataframe(df_away_ilk5)
      sub_counter_away=sub_counter_away+1
      #container_final_away=container_final_away.append(df_away_ilk5)
      container_final_away = pd.concat([container_final_away, df_away_ilk5])
      df_away_ilk5= container_away.loc[container_away['Sub_No']== sub_counter_away].copy()
      df_away_ilk5['markerTime']= slice[9]
      df_away_ilk5['Ceyrek']= slice[16]
      df_away_ilk5['Dif'] = score_away-score_home	
      df_away_ilk5['Score1'] = str(score_home)+ '-' + str(score_away)	
      top_puan_away=0
      score_neg_away=0
  	 
   elif slice[1].strip() in ['EG'] :
    if counter==0:
     counter=counter+1
     #sub_counter_home
     #df_home_ilk5['markerTime']= 'Last'
     #df_home_ilk5['Ceyrek']= slice[16]
     df_home_ilk5['Sure']= time_home
     df_home_ilk5['Dif2']=score_home-score_away
     df_home_ilk5['Score2'] = str(score_home)+ '-' + str(score_away)
     df_home_ilk5['Top_Puan']= df_home_ilk5['Top_Puan']- df_home_ilk5['Score-']
     #container_final_home=container_final_home.append(df_home_ilk5)  
     container_final_home = pd.concat([container_final_home, df_home_ilk5])
     #st.dataframe(df_home_ilk5)
    
     #sub_counter_away
     #df_away_ilk5['markerTime']= 'Last'
     #df_away_ilk5['Ceyrek']= slice[16]
     df_away_ilk5['Sure']= time_away
     df_away_ilk5['Dif2']=score_away-score_home
     df_away_ilk5['Score2'] = str(score_home)+ '-' + str(score_away)
     df_away_ilk5['Top_Puan']= df_away_ilk5['Top_Puan']- df_away_ilk5['Score-']
     #container_final_away=container_final_away.append(df_away_ilk5)
     container_final_away = pd.concat([container_final_away, df_away_ilk5]) 	
     #st.dataframe(df_away_ilk5)
    
    
    
  #secy = st.radio("Choose :",('Home Team','Away Team'))
  
  
  if secy=='Home Team':
   resm=df_clubs.loc[df_clubs['code']==home].copy()
   resm=resm['crest'].values.tolist()
   st.image (resm[0],width=40) 
   no=container_final_home['Top_Puan'].max()
   shining_home= container_final_home.loc[container_final_home['Top_Puan']==no].copy()  
  
  if secy=='Away Team':
   resm=df_clubs.loc[df_clubs['code']==away].copy()
   resm=resm['crest'].values.tolist()
   st.image (resm[0],width=40) 
   no=container_final_away['Top_Puan'].max()
   shining_home= container_final_away.loc[container_final_away['Top_Puan']==no].copy()  
  
    
  st.header ('Productive 5') 
  
  
  shining_home=shining_home.tail(5) 
  
  foto=shining_home['imageUrls.headshot'].values.tolist()
  namo=shining_home['jerseyName'].values.tolist()
  pos=shining_home['positionName'].values.tolist()
  markero=shining_home['markerTime'].max()
  dif2=shining_home['Dif2'].values.tolist()
  dif1=shining_home['Dif'].values.tolist()
  bas= shining_home['Score1'].values.tolist()
  son= shining_home['Score2'].values.tolist()
  
  
  
  
  shining_home['Ceyrek']=shining_home['Ceyrek'].replace(to_replace='q1',value='first quarter')
  shining_home['Ceyrek']=shining_home['Ceyrek'].replace(to_replace='q2',value='second quarter')
  shining_home['Ceyrek']=shining_home['Ceyrek'].replace(to_replace='q3',value='third quarter')
  shining_home['Ceyrek']=shining_home['Ceyrek'].replace(to_replace='q4',value='fourth quarter')
  shining_home['Ceyrek']=shining_home['Ceyrek'].replace(to_replace='ot',value='over time')
  q=shining_home['Ceyrek'].values.tolist()
  secondo=shining_home['Sure'].max()
  shining_home['Score+']=shining_home['Score+'].astype(int)
  scorly=shining_home['Score+'].sum() 
  shining_home['Score+']=shining_home['Score+'].astype(str)
  score_oponent=scoro=shining_home['Score-'].max()
  tot=shining_home['Top_Puan'].max()
  
  'Starting from ' + str(markero) +  ' with the result: ' +str(bas[0]) +' during ' + str(q[0]) + ', they stayed on the court ' + str(round(secondo/60,1)) + ' minutes, scored '+ str(scorly) + ' points and let opponent score '+ str(score_oponent) + ' points; \
  finally produced ' + str(tot) + ' contribution points, ending their time with the result: ' +son[0]
  
  sutun1,sutun2,sutun3,sutun4,sutun5 = st.columns (5)
  
  with sutun1:
    try:
     st.image(foto[0],caption=namo[0]+', '+pos[0] ,width=140)
    except:
     pass
  with sutun2:
   try:
    st.image(foto[1],caption=namo[1]+', '+pos[1],width=140)
   except: 
    pass 
  with sutun3:
   try:
    st.image(foto[2],caption=namo[2]+', '+pos[2],width=140)
   except:
    pass  
  with sutun4:
   try:
    st.image(foto[3],caption=namo[3]+', '+pos[3],width=140)
   except:
    pass
  with sutun5:
   try:
    st.image(foto[4],caption=namo[4]+', '+pos[4],width=140)
   except:
    pass
    
  shining_home= shining_home[['jerseyName','Score+','Assist','Rebaund','Blok','Steal','TurnOver']]
  shining_home.columns=['Player Name','Score','Assist','Rebaund','Block','Steal','Turnover']
  shining_home=shining_home.reset_index(drop=True)
  st.dataframe(shining_home)
  
  
   	
 #except:
 #'New season has not started yet.'	
 #'Please check your connection and refresh the link.'	
   
   
takip= """
<!-- Default Statcounter code for Euro_stats_productive
https://euroleaguestats.streamlit.app/ -->
<script type="text/javascript">
var sc_project=13046774; 
var sc_invisible=1; 
var sc_security="f80506ba"; 
</script>
<script type="text/javascript"
src="https://www.statcounter.com/counter/counter.js"
async></script>
<noscript><div class="statcounter"><a title="Web Analytics
Made Easy - Statcounter" href="https://statcounter.com/"
target="_blank"><img class="statcounter"
src="https://c.statcounter.com/13046774/0/f80506ba/1/"
alt="Web Analytics Made Easy - Statcounter"
referrerPolicy="no-referrer-when-downgrade"></a></div></noscript>
<!-- End of Statcounter Code -->
"""
#st.markdown(takip, unsafe_allow_html=True)  
components.html(takip,width=200, height=200)   
