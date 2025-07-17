import streamlit as st 
from funciones import pagInicio, pagRegistro, pagLogin, sesionIniciada

if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'inicio'

if 'id' not in st.session_state:
    st.session_state['id'] = ""

if 'limiteMensual' not in st.session_state:
    st.session_state['limiteMensual'] = 0.0


st.set_page_config(page_title="Seguimiento Gastos", page_icon="💰")

if st.session_state['pagina'] == 'inicio':
    pagInicio()
    if st.session_state['pagina'] != 'inicio':
        st.rerun()

elif st.session_state['pagina'] == 'registro':
      pagRegistro()
      if st.session_state['pagina'] != 'registro':
          st.rerun()

elif st.session_state['pagina'] == 'login':
    pagLogin()
    if st.session_state['pagina'] != 'login':
        st.rerun()
      

elif st.session_state['pagina'] == "Sesion iniciada":
    sesionIniciada()
    if st.session_state['pagina'] != 'Sesion iniciada':
        st.rerun()

