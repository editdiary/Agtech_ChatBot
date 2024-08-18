import streamlit as st
import os

# db 정보 가져오기
db_user = st.secrets["username"]
db_password = st.secrets["password"]

# session_state login 정보 초기화
st.session_state["is_login"] = False


# 로그인 화면
st.title("환영합니다!")

input_user = st.text_input("이름을 입력해주세요.")
input_password = st.text_input("비밀번호를 입력해주세요.", type="password")

login_btn = st.button("로그인", key="login_btn")

# 로그인 버튼 클릭 시
if login_btn:
    if (input_user in db_user) and (input_password == db_password):
        st.success("로그인 성공")

        # 로그인 성공 시 session_state에 로그인 정보 저장
        st.session_state["is_login"] = True

        # 로그인 성공시 환경변수 설정
        os.environ["OPENAI_API_KEY"] = st.secrets["openai_keys"]["OPENAI_API_KEY"]

        os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["langchain_keys"]["LANGCHAIN_TRACING_V2"]
        os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["langchain_keys"]["LANGCHAIN_ENDPOINT"]
        os.environ["LANGCHAIN_API_KEY"] = st.secrets["langchain_keys"]["LANGCHAIN_API_KEY"]
        os.environ["LANGCHAIN_PROJECT"] = st.secrets["langchain_keys"]["LANGCHAIN_PROJECT"]

        os.environ["TAVILY_API_KEY"] = st.secrets["tavily_keys"]["TAVILY_API_KEY"]

    else:
        st.error("로그인 실패")