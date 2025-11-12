# pip install python | python -m install streamlit
import streamlit as st
from groq import Groq

st.set_page_config(page_title="Tu asistente virtúal :)", page_icon="👻")
st.title("My first app on Streamlit")

nombre = st.text_input("Como te llamás?")
if st.button("Saludar!"):
    st.write(f"Bienvenido {nombre}, haz todas las preguntas que quieras.")

MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b']

def configurar_pagina():
    st.title("Mi asistente virtúal V11.25")
    st.sidebar.title("Configuracion de la IA")

    elegirModelo = st.sidebar.selectbox(
        "Elegi un modelo",
        options = MODELOS,
        index = 0
    )

    return elegirModelo

# ------------FUNCIONES-----------------------------------
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key= clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content": mensajeDeEntrada}],
        stream = True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border= True)
    with contenedorDelChat: mostrar_historial()


# Clase 9 - funciones
def generar_respuestas(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        print(frase.choices[0].delta.content)
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

# Main - > Todas las funciones para correr el Chatbot
def main ():
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    modelo = configurar_pagina()
    area_chat() #Nuevo 
    mensaje = st.chat_input("Tipear mensaje:")

    if mensaje:
        actualizar_historial("user", mensaje, "👽")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
                with st.chat_message("assistant"):
                    respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                    actualizar_historial("assistant", respuesta_completa, "👾")
                    st.rerun()
            
        
if __name__ == "__main__":
    main()
