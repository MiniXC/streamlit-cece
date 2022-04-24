import streamlit as st
import pymongo
from time import sleep

pwd = st.secrets["DB_PASSWORD"]

client = pymongo.MongoClient(f"mongodb+srv://root:{pwd}@cece.ldq20.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.cece
messages = db.messages

st.header("Cece Printer Interface")
st.write("This app writes a message to a database, then waits for 5 seconds for it to be printed, then deletes it again.")
to = st.selectbox('send message to',['stouf'])
text = st.text_input('message')
if st.button('send'):
    msg_result = messages.insert_one({"for": to, "text": text, "printed": False})
    st.success("sent message to printer")
    _id = msg_result.inserted_id
    sleep(5)
    msg_printed = messages.find_one({"_id": _id})
    if msg_printed["printed"]:
        st.success("successfully printed message")
    else:
        st.error("printing failed, printer might be offline")
    messages.delete_one({"_id": _id})
    st.info("message deleted")