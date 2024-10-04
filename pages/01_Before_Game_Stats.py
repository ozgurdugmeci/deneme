import streamlit.components.v1 as components
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

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



col1,col2 = st.columns([1,1])

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

 box3

#column2 -------------------------------------------------------------------------------------------------------------

with col2:
 option2 = st.selectbox(
    'Select the team',
    (box1), key='2',index=None)


	
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

