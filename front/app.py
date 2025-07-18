import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from back.retriever import responder_pergunta

st.title("Pergunte sobre a carteira do cliente:")

if "historico" not in st.session_state:
    st.session_state.historico = []

pergunta = st.text_input("Digite sua pergunta:", key="input")

if st.button("Enviar Pergunta") and pergunta:
    with st.spinner("Consultando o grafo e gerando resposta..."):
        resposta = responder_pergunta(pergunta)
        st.session_state.historico.append((pergunta, resposta))
        st.success("Resposta gerada com sucesso!")

if st.session_state.historico:
    st.markdown("### Histórico de Perguntas e Respostas")
    for i, (q, r) in enumerate(reversed(st.session_state.historico), 1):
        with st.expander(f"{i}. {q}"):
            st.write(r)
