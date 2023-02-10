import pandas as pd
import glob
import tqdm
import streamlit as st

@st.cache(suppress_st_warning=True)
def convert_inference_to_table(inference_path):
    inference_path+="/labels"
    txt_files = glob.glob(inference_path+"/*.txt")
    results_list = []

    for file in tqdm.tqdm(txt_files):
        df = pd.read_csv(file, sep=" ")
        filename = file.replace(inference_path+"\\", "").replace(".txt", "")
        for _, row in df.iterrows():
            results_list.append([filename, row[0], row[4]])
        
    df = pd.DataFrame(results_list, columns=["number", "plane_id", "confidence"])
    return df


if __name__ == "__main__":
    results_df = convert_inference_to_table("yolov7/runs/detect/exp6")
    results_df.to_csv("results.csv")