import streamlit as st
from langchain.chat_models import ChatOpenAI
import pandas as pd
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

st.set_page_config(page_title="RLHF labelling session", layout="wide")

if 'page_title' not in st.session_state:
    st.session_state['page_title'] = "🤠你的偏好会让世界更好！"
if 'counter' not in st.session_state:
    st.session_state['counter'] = 2
if 'qid' not in st.session_state:
    st.session_state["qid"] = []
    st.session_state["question"] = []
    st.session_state["answer"] = []
    st.session_state["亲和度"] = []
    st.session_state["知识准确度"] = []
    
    
st.title(st.session_state.page_title)

def title_shift():  
    if st.session_state['page_title'] == "🤠你的偏好会让世界更好！":
        st.session_state['page_title'] = "🈲 除非你是个变态 🈲"
    else:
        st.session_state['page_title'] = "🤠你的偏好会让世界更好！"

check_box_hide = st.checkbox('真的吗？那我试试', on_change=title_shift )

path = "medical_QA_rating.xlsx"

    
@st.cache_data
def read_excel_local(path:str):
    df = pd.read_excel(path)
    # rows = df.iterrows()
    return df

data = read_excel_local(path)

if "q_messages" not in st.session_state:
    # rows = data.iterrows()
    rows = data.iterrows()
    _, row = next(rows)
    st.session_state["q_messages"] = HumanMessage(content=row['question'].replace("\\n", ' '))
    st.session_state["qid"].append(row['qid'])
    st.session_state["question"].append(row['question'])
    st.session_state["answer"].append(row['answer'])
    n = data.shape[0]
    st.session_state["len"] = n
if "a_messages" not in st.session_state:
    st.session_state["a_messages"] = AIMessage(content=row['answer'].replace("\\n", ' '))

# st.dataframe(data_for_rating.style.highlight_max(axis=0))

with st.container():
    st.header("Human question")
    st.markdown(st.session_state["q_messages"].content)
    st.header('AI :blue[Answers] :sunglasses:')
    st.markdown(st.session_state["a_messages"].content)
    
option_1 = st.selectbox(
    '该回答在亲和力上的表现打分',
     ("⭐","⭐⭐","⭐⭐⭐","⭐⭐⭐⭐","⭐⭐⭐⭐⭐"))

'您的打分：', option_1

option_2 = st.selectbox(
    '该回答在知识准确度上的表现打分',
     ("⭐","⭐⭐","⭐⭐⭐","⭐⭐⭐⭐","⭐⭐⭐⭐⭐"))

'您的打分: ', option_2

result = pd.DataFrame()

    
# rows = st.session_state["generator"]
def next_save(option_1, option_2):
    # st.session_state["quality_1"] = len(option_1)
    # st.session_state["quality_2"] = len(option_2)
    st.session_state["亲和度"].append(len(option_1))
    st.session_state["知识准确度"].append(len(option_2))
    rows = data.iterrows()
    for i in range(st.session_state.counter):
        try:
            _, row = next(rows)
        except:
            return None
    st.session_state["q_messages"] = HumanMessage(content=row['question'].replace("\\n", ' '))
    st.session_state["a_messages"] = AIMessage(content=row['answer'].replace("\\n", ' '))
    st.session_state["qid"].append(row['qid'])
    st.session_state["question"].append(row['question'])
    st.session_state["answer"].append(row['answer'])
    # st.session_state["generator"] = rows
    return None

def final():
    # print(st.session_state)
    rating_data = pd.DataFrame({'qid':st.session_state["qid"],
                                'question':st.session_state["question"],
                                'answer':st.session_state["answer"],
                                '亲和度分数':st.session_state["亲和度"],
                                '准确度分数':st.session_state["知识准确度"],     
                                })
    return rating_data
    # st.write(rating_data)

if st.button('确认 -> 下一个评估：', on_click=next_save, args=[option_1,option_2]):
    # next_save(option_1, option_2)
    # st.balloons()
    st.session_state.counter += 1
    if st.session_state.counter <= st.session_state.len + 1:
        pass
    else:
        data = final()
        st.write(data)
        st.balloons()


# st.session_state
# data