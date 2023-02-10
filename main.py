import streamlit as st
from util import convert_inference_to_table

run_path = "yolov7/runs/detect/exp"
planes_list = ["A10", "A400M", "AG600", "AV8B", "B1", "B2", "B52", "Be200", "C130", "C17", "C5", "E2", "EF2000", "F117", "F14", "F15", "F16", "F18", "F22", "F35", "F4", "JAS39", "J20", "MQ9", "Mig31", "Mirage2000", "RQ4", "Rafale", "SR71", "Su34", "Su57", "Tornado", "Tu160", "Tu95", "U2", "US2", "V22", "Vulcan", "XB70", "YF23"]

st.header("Chercher un avion :")
selection = st.multiselect("Type d'avion sur la photo", planes_list)
slider = st.slider("Niveau de confiance minimum", 0.0, 1.0, step=0.05)
agg_method = st.radio(
    "Méthodes d'aggrégation des résultats",
    ('OU', 'ET'))

selected_id = []
for selected in selection:
    selected_id.append(planes_list.index(selected))

df_results = convert_inference_to_table(run_path)

df_results = df_results[df_results.confidence >= slider]
df_results = df_results[df_results.plane_id.isin(selected_id)]
#st.table(df_results)
if agg_method == "ET":
    df_indexes = df_results.groupby('number')['plane_id'].nunique() == len(selected_id)
    #st.table(df_indexes[df_indexes].index)
    numbers_to_show = list(df_indexes[df_indexes].index) 

else:
    df_results = df_results.drop_duplicates(subset=['number'])
    numbers_to_show = df_results["number"]


images_to_show = []
for number in numbers_to_show:
    img_path = f"{run_path}/{number}.jpg"
    images_to_show.append(img_path)

st.text(f"{len(images_to_show)} résultats")
st.image(images_to_show)
