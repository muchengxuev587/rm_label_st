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
    st.session_state['page_title'] = "🤠请选择你认为更好的回答"
if 'counter' not in st.session_state:
    st.session_state['counter'] = 2
if 'qid' not in st.session_state:
    st.session_state["qid"] = []
    st.session_state["question"] = []
    # st.session_state["answer"] = []
    st.session_state["response_j"] = []
    st.session_state["response_k"] = []
    st.session_state["choice"] = []
    
    
st.title(st.session_state.page_title)

path = "pages/medical_QA_paired_source.xlsx"
# pages\medical_QA_paired_source.xlsx

@st.cache_data
def read_excel_local(path:str):
    df = pd.read_excel(path)
    return df

if 'data' not in st.session_state:
    data = read_excel_local(path)
    st.session_state["data"] = data

if "q_messages" not in st.session_state:
    # rows = data.iterrows()
    rows = data.iterrows()
    _, row = next(rows)
    st.session_state["q_messages"] = HumanMessage(content=row['question(string)'].replace("\\n", ' '))
    st.session_state["qid"].append(row['qid'])
    st.session_state["question"].append(row['question(string)'])
    # st.session_state["answer_j"].append(row['response_j'])
    # st.session_state["answer_k"].append(row['response_k'])
    n = data.shape[0]
    st.session_state["len"] = n
if "a_messages_j" not in st.session_state:
    st.session_state["a_messages_j"] = AIMessage(content=row['response_j'].replace("\\n", ' '))
    st.session_state["a_messages_k"] = AIMessage(content=row['response_k'].replace("\\n", ' '))

# st.dataframe(data_for_rating.style.highlight_max(axis=0))

with st.container():
    st.header("你觉得下面两种AI的回答哪个更好？")
    st.header("Human question")
    st.markdown(st.session_state["q_messages"].content)
    st.header('AI :red[Answer 1] :sunglasses:')
    st.markdown(st.session_state["a_messages_j"].content)
    st.header('AI :blue[Answers 2] :sunglasses:')
    st.markdown(st.session_state["a_messages_k"].content)
    
option_1 = st.selectbox(
    '该回答在亲和力上的表现打分',
     ("回答一", "回答二"))

'更好的回答是：', option_1
 
# rows = st.session_state["generator"]
def next_save(option_1):
    # st.session_state["quality_1"] = len(option_1)
    # st.session_state["quality_2"] = len(option_2)
    data = st.session_state.data
    # st.session_state["知识准确度"].append(len(option_2))
    rows = data.iterrows()
    if option_1 == "回答一":
        st.session_state["choice"].append('j')
    if option_1 == "回答二":
        st.session_state["choice"].append('k')
        
    for i in range(st.session_state.counter):
        try:
            _, row = next(rows)
        except:
            return None
        
    st.session_state["q_messages"] = HumanMessage(content=row['question(string)'])
    st.session_state["a_messages_j"] = AIMessage(content=row['response_j'].lstrip().replace("\\n", ' '))
    st.session_state["a_messages_k"] = AIMessage(content=row['response_k'].lstrip().replace("\\n", ' '))

    st.session_state["qid"].append(row['qid'])
    st.session_state["question"].append(row['question(string)'])
    
    # st.session_state["generator"] = rows
    return None

def final():
    # print(len(st.session_state['question']),len(st.session_state["a_messages_j"],
    #                                             len(st.session_state["a_messages_k"])))
    # print(st.session_state)
    try:
        rating_data = pd.DataFrame({'qid':st.session_state["qid"],
                                'question':st.session_state["question"],
                                'choice':st.session_state['choice']
                                })
    except:
        print('exception')
    return rating_data
    # st.write(rating_data)

if st.button('确认 -> 下一个评估：', on_click=next_save, args=[option_1]):
    # next_save(option_1, option_2)
    # st.balloons()
    st.session_state.counter += 1
    if st.session_state.counter <= st.session_state.len + 1:
        pass
    else:
        data = final()
        st.write(data)
        st.snow()

# st.session_state
