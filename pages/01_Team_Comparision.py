import streamlit.components.v1 as components
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import plotly.express as px
import pandas as pd
from euroleague_api.game_stats import GameStats as gs
from euroleague_api.team_stats import TeamStats as ts
from euroleague_api.standings import Standings as s
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(page_title='Team Comparison', page_icon="🏀", layout="wide",initial_sidebar_state ='collapsed')

#-------------------------------------
#try: 
df_stats=[]
df_stats=pd.DataFrame(df_stats)
df_stats2=[]
df_stats2=pd.DataFrame(df_stats2)
counter=0
sezon=2025
try:
 euro_img='https://media-cdn.incrowdsports.com/23610a1b-1c2e-4d2a-8fe4-ac2f8e400632.svg'
 st.image(euro_img,width=120)
except:
 pass 
#st.title('Productive Five') -------- ----
' '
' ' 
standinga = s("E")
df_clubs = standinga.get_standings(season= sezon, round_number= 1, endpoint= 'basicstandings')
#print(df_clubs.columns)
df_clubs= df_clubs[['club.name','club.editorialName','club.images.crest','club.tvCode','club.code']].copy()
print(df_clubs)

df_clubs=df_clubs.sort_values(by='club.name', ascending=True)

box1= df_clubs['club.name'].values.tolist()

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

 takm1=df_clubs.loc[df_clubs['club.name']==option].copy() 
 takm1=takm1['club.code'].values.tolist()[0]
 
 #printo
 resm=df_clubs.loc[df_clubs['club.name']==option].copy()
 resm=resm['club.images.crest'].values.tolist()
 with col1:
  st.image(resm[0],width=100)
 #---------Devam1
 
 team_stats=ts("E")
 game_stats = gs("E")
 df_results_all=team_stats.get_gamecodes_season(season=sezon) # results
 df_results1= df_results_all.loc[df_results_all['homecode']==takm1].copy()
 df_results2= df_results_all.loc[df_results_all['awaycode']==takm1].copy()
 df_results_team1= pd.concat([df_results1, df_results2])
 
 df_results_team1=df_results_team1.sort_values(by='gameCode', ascending=False)
 #df_results['yeni'] = df_results['hometeam'] + ' '+  df_results['homescore'] + ' - ' + df_results['awayteam']+ ' ' +  df_results['awayscore']  
 #st.dataframe(df_results)
 df_results_team1.loc[(df_results_team1['homecode']==takm1),'saha']= 'H' 
 df_results_team1.loc[(df_results_team1['homecode']!=takm1),'saha']= 'A'
 df_results_team1.loc[((df_results_team1['homecode']==takm1)& (df_results_team1['homescore']>df_results_team1['awayscore'])) ,'W/L']= '1'
 df_results_team1.loc[((df_results_team1['homecode']==takm1)& (df_results_team1['homescore']<df_results_team1['awayscore'])) ,'W/L']= '0'
 df_results_team1.loc[((df_results_team1['homecode']!=takm1)& (df_results_team1['homescore']>df_results_team1['awayscore'])) ,'W/L']= '0'
 df_results_team1.loc[((df_results_team1['homecode']!=takm1)& (df_results_team1['homescore']<df_results_team1['awayscore'])) ,'W/L']= '1' 
 df_results_team1.loc[(df_results_team1['saha']=='H'),'P+']= df_results_team1['homescore']  
 df_results_team1.loc[(df_results_team1['saha']=='A'),'P+']= df_results_team1['awayscore']
 
 df_results_team1.loc[(df_results_team1['saha']=='H'),'P-']= df_results_team1['awayscore']  
 df_results_team1.loc[(df_results_team1['saha']=='A'),'P-']= df_results_team1['homescore']
 #points_art= df_results_team1['P+'].sum()
 #points_eks= df_results_team1['P-'].sum()
 
 #st.dataframe(df_results_team1)
 
 deplasman=0 
 saha=0 
 uzunluk=len(df_results_team1)
 if value1> uzunluk:
  pass
 else:
  uzunluk=value1 
 away_win=0
 home_win=0
 df_results_team1= df_results_team1.head(uzunluk)
 game_codes= df_results_team1['gameCode'].values.tolist()
 durum= df_results_team1['W/L'].values.tolist()
 saha= df_results_team1['saha'].values.tolist()
 round= df_results_team1['Round'].values.tolist()
 points_eks= df_results_team1['P-'].values.tolist()
 mimle=0
 #burdan devam--------------------------------------------------
  
 #burda results teker teker analiz ediliyor.
 for r in game_codes:
  df2=game_stats.get_game_stats(season= sezon, game_code= r) #team stats 
  #team stats 
  
  if saha[mimle]== 'H':
   df2=df2[['local.total.points','local.total.accuracyMade','local.total.accuracyAttempted','local.total.totalRebounds','local.total.assistances','local.total.turnovers']].copy()
   df2.columns=['Points','Accuracy Made','Accuracy Attempted','Rebaunds','Assists','Turnovers']
   df2['Points-']= points_eks[mimle]
   df2['W/L']= durum[mimle]
   df2['H/A']=saha[mimle]
   df2['%Accuracy']=df2['Accuracy Made']/df2['Accuracy Attempted']
   df2['Round']=round[mimle]   
  else:
   df2=df2[['road.total.points','road.total.accuracyMade','road.total.accuracyAttempted','road.total.totalRebounds','road.total.assistances','road.total.turnovers']].copy()   
   df2.columns=['Points','Accuracy Made','Accuracy Attempted','Rebaunds','Assists','Turnovers']
   df2['Points-']= points_eks[mimle]
   df2['W/L']= durum[mimle]
   df2['H/A']=saha[mimle]
   df2['%Accuracy']=df2['Accuracy Made']/df2['Accuracy Attempted']
   df2['Round']=round[mimle]
   
  df_stats= pd.concat([df2,df_stats])
  mimle=mimle+1
 

 df_stats.loc[(df_stats['W/L']=='1'),'-W/L-']='W'
 df_stats.loc[(df_stats['W/L']=='0'),'-W/L-']='L'
 df_team1= df_stats.copy()
 df_team1['All']='All'
 df_team1 = pd.pivot_table(df_team1, values=['Points','Points-','Accuracy Attempted','Rebaunds','Assists','Turnovers'], index=['All'] ,aggfunc="sum") 
 df_team1 = df_team1.reset_index()                #index to columns ------------------  -------------------------------
 df_team1.drop(['All'], inplace=True, axis=1)
 
 df_team1= df_team1[['Points','Points-','Assists','Rebaunds','Turnovers','Accuracy Attempted']].copy()
 df_team1.columns=['Points','Points-','Assists','Rebounds','Turnovers','ScoreAttempt']
 #st.dataframe(df_team1)
 
 
 
 uzunluk2=len(df_team1.columns) 
 
 for i in range(0,uzunluk2):
   
  df_team1[df_team1.columns[i]]= df_team1[df_team1.columns[i]]/uzunluk
  df_team1[df_team1.columns[i]]=df_team1[df_team1.columns[i]].round(0)
 #st.dataframe(df_stats)
 #st.dataframe(df_team1)
 
 
with col2:
 optionto = st.selectbox(
    'Select the team',
    (box1), key='2',index=None)


#------	
if optionto !=None:
  
 printo= optionto + ' seçilen'

 takm2=df_clubs.loc[df_clubs['club.name']==optionto].copy() 
 takm2=takm2['club.code'].values.tolist()[0]
 
 #printo
 resm=df_clubs.loc[df_clubs['club.name']==optionto].copy()
 resm=resm['club.images.crest'].values.tolist()
 #devam -----------------------------------------
 with col2:
  st.image(resm[0],width=100)
 #---------Devam1
 team_stats=ts("E")
 game_stats = gs("E")
 df_results_all=team_stats.get_gamecodes_season(season=sezon) # results
 df_results1= df_results_all.loc[df_results_all['homecode']==takm2].copy()
 df_results2= df_results_all.loc[df_results_all['awaycode']==takm2].copy()
 df_results_team2= pd.concat([df_results1, df_results2])
 
 df_results_team2=df_results_team2.sort_values(by='gameCode', ascending=False)
 #df_results['yeni'] = df_results['hometeam'] + ' '+  df_results['homescore'] + ' - ' + df_results['awayteam']+ ' ' +  df_results['awayscore']  
 #st.dataframe(df_results)
 df_results_team2.loc[(df_results_team2['homecode']==takm2),'saha']= 'H' 
 df_results_team2.loc[(df_results_team2['homecode']!=takm2),'saha']= 'A'
 df_results_team2.loc[((df_results_team2['homecode']==takm2)& (df_results_team2['homescore']>df_results_team2['awayscore'])) ,'W/L']= '1'
 df_results_team2.loc[((df_results_team2['homecode']==takm2)& (df_results_team2['homescore']<df_results_team2['awayscore'])) ,'W/L']= '0'
 df_results_team2.loc[((df_results_team2['homecode']!=takm2)& (df_results_team2['homescore']>df_results_team2['awayscore'])) ,'W/L']= '0'
 df_results_team2.loc[((df_results_team2['homecode']!=takm2)& (df_results_team2['homescore']<df_results_team2['awayscore'])) ,'W/L']= '1' 
 df_results_team2.loc[(df_results_team2['saha']=='H'),'P+']= df_results_team2['homescore']  
 df_results_team2.loc[(df_results_team2['saha']=='A'),'P+']= df_results_team2['awayscore']
 
 df_results_team2.loc[(df_results_team2['saha']=='H'),'P-']= df_results_team2['awayscore']  
 df_results_team2.loc[(df_results_team2['saha']=='A'),'P-']= df_results_team2['homescore']
 
 #st.dataframe(df_results_team2)
 #df_results_team1
 deplasman=0 
 saha=0 
 uzunluk=len(df_results_team2)
 if value1> uzunluk:
  pass
 else:
  uzunluk=value1 
 away_win=0
 home_win=0
 df_results_team2= df_results_team2.head(uzunluk)
 game_codes= df_results_team2['gameCode'].values.tolist()
 durum= df_results_team2['W/L'].values.tolist()
 saha= df_results_team2['saha'].values.tolist()
 round= df_results_team2['Round'].values.tolist()
 points_eks=df_results_team2['P-'].values.tolist()
 mimle=0
 #burdan devam--------------------------------------------------
  
 #burda results teker teker analiz ediliyor.
 for r in game_codes:
  df2=game_stats.get_game_stats(season= sezon, game_code= r) #team stats 
  #team stats 
  
  if saha[mimle]== 'H':
   df2=df2[['local.total.points','local.total.accuracyMade','local.total.accuracyAttempted','local.total.totalRebounds','local.total.assistances','local.total.turnovers']].copy()
   df2.columns=['Points','Accuracy Made','Accuracy Attempted','Rebaunds','Assists','Turnovers']
   df2['Points-']= points_eks[mimle]
   df2['W/L']= durum[mimle]
   df2['H/A']=saha[mimle]
   df2['%Accuracy']=df2['Accuracy Made']/df2['Accuracy Attempted']
   df2['Round']=round[mimle]   
  else:
   df2=df2[['road.total.points','road.total.accuracyMade','road.total.accuracyAttempted','road.total.totalRebounds','road.total.assistances','road.total.turnovers']].copy()   
   df2.columns=['Points','Accuracy Made','Accuracy Attempted','Rebaunds','Assists','Turnovers']
   df2['Points-']= points_eks[mimle]
   df2['W/L']= durum[mimle]
   df2['H/A']=saha[mimle]
   df2['%Accuracy']=df2['Accuracy Made']/df2['Accuracy Attempted']
   df2['Round']=round[mimle]
   
  df_stats2= pd.concat([df2,df_stats2])
  mimle=mimle+1
 
 df_stats2.loc[(df_stats2['W/L']=='1'),'-W/L-']='W'
 df_stats2.loc[(df_stats2['W/L']=='0'),'-W/L-']='L'

 df_team2= df_stats2.copy()
 df_team2['All']='All'
 df_team2 = pd.pivot_table(df_team2, values=['Points','Points-','Accuracy Attempted','Rebaunds','Assists','Turnovers'], index=['All'] ,aggfunc="sum") 
 df_team2 = df_team2.reset_index()                #index to columns ------------------  -------------------------------
 df_team2.drop(['All'], inplace=True, axis=1)
 
 df_team2= df_team2[['Points','Points-','Assists','Rebaunds','Turnovers','Accuracy Attempted']].copy()
 df_team2.columns=['Points','Points-','Assists','Rebounds','Turnovers','ScoreAttempt']
 #st.dataframe(df_team1)
 
 
 
 uzunluk2=len(df_team2.columns) 
 
 for i in range(0,uzunluk2):
   
  df_team2[df_team2.columns[i]]= df_team2[df_team2.columns[i]]/uzunluk
  df_team2[df_team2.columns[i]]=df_team2[df_team2.columns[i]].round(0)
 #st.dataframe(df_stats2)
 #st.dataframe(df_team2)

if option != None and optionto != None :
 df_team1_orj= df_team1.copy()
 df_team2_orj= df_team2.copy()

 df_team1_orj['Offense Accuracy']=df_team1_orj['Points']/df_team1_orj['ScoreAttempt']
 df_team2_orj['Offense Accuracy']=df_team2_orj['Points']/df_team2_orj['ScoreAttempt']
 
 df_team2_orj['Offense Accuracy']= df_team2_orj['Offense Accuracy']*100
 df_team1_orj['Offense Accuracy']= df_team1_orj['Offense Accuracy']*100
 df_team2_orj['Offense Accuracy']= df_team2_orj['Offense Accuracy'].round(0)
 df_team1_orj['Offense Accuracy']= df_team1_orj['Offense Accuracy'].round(0)
	
 df_team1_orj['Offense Accuracy']= '%'+ df_team1_orj['Offense Accuracy'].astype(str)	
 df_team2_orj['Offense Accuracy']= '%'+df_team2_orj['Offense Accuracy'].astype(str)	
 df_team1_orj= df_team1_orj.T
 df_team1_orj.columns=['Average']

 
 df_team2_orj= df_team2_orj.T
 df_team2_orj.columns=['Average']

 with col1:
  st.dataframe(df_team1_orj)
 with col2:
  st.dataframe(df_team2_orj)

 df_team1['Offense Accuracy']=df_team1['Points']/df_team1['ScoreAttempt']
 df_team2['Offense Accuracy']=df_team2['Points']/df_team2['ScoreAttempt']
 
 df_team2['Offense Accuracy']= df_team2['Offense Accuracy']*100
 df_team1['Offense Accuracy']= df_team1['Offense Accuracy']*100
 df_team2['Offense Accuracy']= df_team2['Offense Accuracy'].round(0)
 df_team1['Offense Accuracy']= df_team1['Offense Accuracy'].round(0)

 	

 df_team1['Assists']= df_team1['Assists']*8
 df_team1['Rebounds']= df_team1['Rebounds']*3
 df_team1['Turnovers']= df_team1['Turnovers']*6
 df_team1['Offense Accuracy']= df_team1['Offense Accuracy']*1.5
	
 df_team2['Assists']= df_team2['Assists']*8
 df_team2['Rebounds']= df_team2['Rebounds']*3
 df_team2['Turnovers']= df_team2['Turnovers']*6
 df_team2['Offense Accuracy']= df_team2['Offense Accuracy']*1.5	
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
    legend=dict(
        font=dict(size=8, color="white"),
        itemsizing='constant',
        itemwidth=30,
        tracegroupgap=0,
        orientation="h",          # Horizontal layout (saves vertical space)
        x=0.5,                    # Center it horizontally
        xanchor="center",         # Anchor point for x
        y=-0.1,                   # Push it below the chart
        yanchor="top"             # Anchor point for y
    ),
    font=dict(size=12, color="white"),
    width=480,
    height=320)
 
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
 
