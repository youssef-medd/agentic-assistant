import streamlit as st
import sqlite3
from datetime import datetime
from db.database import init_db
init_db()
DB_PATH = "./database.db"
st.set_page_config(page_title = "HAMUS Admin" , page_icon="◈" , layout = "wide")
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn 
conn = get_connection()
messages = conn.execute("SELECT * FROM messages ORDER BY timestamp DESC").fetchall()
files    = conn.execute("SELECT * FROM files ORDER BY uploaded_at DESC").fetchall()
searches = conn.execute("SELECT * FROM searches ORDER BY timestamp DESC").fetchall()
conn.close()
#header
st.header("HAMUS Admin Dashboard")
st.divider()
col1 , col2 , col3 = st.columns(3)
col1.metric("total messages" , len(messages))
col2.metric("files uploaded" , len(files))
col3.metric("searches made" , len(searches))
st.divider()
#messages table
st.subheader("messages")
if messages :
    for msg in messages :
        role = msg["role"]
        content = msg["content"]
        time = msg["timestamp"][0:16].replace("T"," ")
        if role == "user" :
            st.chat_message("user").markdown(f"**{time}**\n\n{content}")
        else :
            st.chat_message("assistant").markdown(f"**{time}**\n\n{content}")
else : 
    st.info("no message yet")
st.divider()
#files table
# files table
st.subheader("Uploaded Files")
if files:
    import pandas as pd
    df_files = pd.DataFrame([dict(f) for f in files])
    df_files = df_files[["filename", "filetype", "uploaded_at"]]
    df_files.columns = ["Filename", "Type", "Uploaded At"]
    df_files["Uploaded At"] = df_files["Uploaded At"].str[:16].str.replace("T", " ")
    st.dataframe(df_files, use_container_width=True)
else:
    st.info("No files uploaded yet.")
st.divider()
# searches table
st.subheader("Searches")
if searches:
    import pandas as pd
    df_searches = pd.DataFrame([dict(s) for s in searches])
    df_searches = df_searches[["query", "timestamp"]]
    df_searches.columns = ["Query", "Timestamp"]
    df_searches["Timestamp"] = df_searches["Timestamp"].str[:16].str.replace("T", " ")
    st.dataframe(df_searches, use_container_width=True)
else:
    st.info("No searches yet.")