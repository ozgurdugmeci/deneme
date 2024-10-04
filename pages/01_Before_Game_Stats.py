
 linko_sezon= 'https://www.euroleaguebasketball.net'+ df_parca + '?season=2023-24'	
 'hey'
 
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
