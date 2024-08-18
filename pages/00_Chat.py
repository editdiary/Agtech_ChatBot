## streamlit은 웹사이트를 만들어주는 도구이다.
import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import load_prompt
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os

st.title("Agtech Chatbot")

# 로그인 상태에서만 기능 실행
if st.session_state.get("is_login") is not True:
    st.error("로그인이 필요합니다.")
    st.stop()

# 메시지를 저장할 list를 생성합니다.
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 메시지에 새로운 메시지를 추가하는 함수
def add_message(role, message):
    # 메시지 list에 새로운 대화(메시지)를 추가합니다.
    st.session_state.messages.append(ChatMessage(role=role, content=message))

# 이전의 대화기록을 모두 출력하는 함수
def print_messages():
    for message in st.session_state.messages:
        # 대화를 출력
        st.chat_message(message.role).write(message.content)

# 체인 생성
def create_chain():
    prompt = load_prompt("prompts/AgtechBot.yaml", encoding="utf-8")
    # LLM 정의
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)   ## gpt-4o-mini, gpt-4o, gpt-3.5-turbo
    # 체인 생성
    chain = prompt | llm | StrOutputParser()
    return chain


# 이전 대화 기록을 모두 출력
print_messages()

# 채팅 입력창
user_input = st.chat_input("궁금한 내용을 입력해 주세요.")

# 만약에 유저가 채팅을 입력하면
if user_input:
    st.chat_message("user").write(user_input)

    # 체인 생성
    chain = create_chain()

    # chain을 실행해서 ai_answer를 받습니다.
    answer = chain.stream(user_input)

    with st.chat_message("ai"):
        # 빈 공간을 만듦
        chat_container = st.empty()

        # ai의 답변을 출력
        ai_answer = ""

        # 스트리밍 출력
        for token in answer:
            ai_answer += token
            chat_container.markdown(ai_answer)

    # 대화를 추가
    add_message("user", user_input)
    add_message("ai", ai_answer)