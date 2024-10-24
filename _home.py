import streamlit as st
import streamlit.components.v1 as components

st.title('Euroleague 2024-2025 Stats' )
'You can simply view the rare stats of Euroleage 2024-2025 season. '
'For a better view, open the app on a laptop or a desktop computer.'
st.subheader('1-Team Comparison')
#htp0='https://raw.githubusercontent.com/ozgurdugmeci/easy-app/main/media/model4.jpg'
biry= "- Select the teams you want to compare. <br> Analyse the radar graph for an easy comparision.<br> Overview the average team stats' tables. "

st.markdown(biry,unsafe_allow_html=True)
   

img1 ='https://raw.githubusercontent.com/ozgurdugmeci/deneme/main/comparison.jpg'
st.image(img1,width=500)

st.subheader('2-Finished Game Analysis & Productive5 Players')

biry= "- Select the team and choose the game. <br> Analyse the radar graph of the two teams.<br> Overview the stats and the game summary of the Productive5 Players.<br>\
You can change the Productive5 Players by changing Home/Away button."

st.markdown(biry,unsafe_allow_html=True)

img2 ='https://raw.githubusercontent.com/ozgurdugmeci/deneme/main/game_analysis1.jpg'
st.image(img2,width=500)
img3 ='https://raw.githubusercontent.com/ozgurdugmeci/deneme/main/game_analysis2.jpg'
st.image(img3,width=500)
st.subheader('3-Substitution Analysis')

biry= "- Select the team and choose the game. <br> Analyse the Substitution & Score Difference Graph.<br> Click on the bars of the graph \
to analyse the related 5 on the court.<br>\
You can change the team by clicking Home/Away button."

st.markdown(biry,unsafe_allow_html=True)

img2 ='https://raw.githubusercontent.com/ozgurdugmeci/deneme/main/graph2.jpg'
st.image(img2,width=500)
img2 ='https://raw.githubusercontent.com/ozgurdugmeci/deneme/main/graphx.jpg'
st.image(img2,width=500)
img3 ='https://raw.githubusercontent.com/ozgurdugmeci/deneme/main/team3.jpg'
st.image(img3,width=500)

st.subheader('4-Player Stats')
biry= "- Select the team and choose the player. <br> Analyse the stats of the selected player."

st.markdown(biry,unsafe_allow_html=True)

img3 ='https://raw.githubusercontent.com/ozgurdugmeci/deneme/main/player_stats.jpg'
st.image(img3,width=500)
takip= """
<!-- Default Statcounter code for Euro_stats_home
https://euroleaguestats.streamlit.app/ -->
<script type="text/javascript">
var sc_project=13046765; 
var sc_invisible=1; 
var sc_security="2abc5313"; 
</script>
<script type="text/javascript"
src="https://www.statcounter.com/counter/counter.js"
async></script>
<noscript><div class="statcounter"><a title="Web Analytics"
href="https://statcounter.com/" target="_blank"><img
class="statcounter"
src="https://c.statcounter.com/13046765/0/2abc5313/1/"
alt="Web Analytics"
referrerPolicy="no-referrer-when-downgrade"></a></div></noscript>
<!-- End of Statcounter Code -->
"""
#st.markdown(takip, unsafe_allow_html=True)  
components.html(takip,width=200, height=200)  
