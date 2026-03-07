import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Carpeta y archivo para fotos y datos
if not os.path.exists("fotos"):
    os.makedirs("fotos")

archivo = "ganaderia_datos.xlsx"

# Crear archivo Excel si no existe
if not os.path.exists(archivo):
    ganado = pd.DataFrame(columns=["Foto","Nombre","Fecha de Nacimiento","Madre","Padre"])
    produccion = pd.DataFrame(columns=["Fecha","Nombre","Litros"])
    servicio = pd.DataFrame(columns=["Nombre","Fecha de Servicio","Toro","Finaliza Producción","Fecha aprox. del parto","Fecha de Parto","Numero de Cria","Sexo Cria"])

    with pd.ExcelWriter(archivo, engine="openpyxl") as writer:
        ganado.to_excel(writer, sheet_name="Ganado", index=False)
        produccion.to_excel(writer, sheet_name="Produccion", index=False)
        servicio.to_excel(writer, sheet_name="Servicio", index=False)

st.title("🐄 Sistema de Gestión Ganadera")

menu = st.sidebar.selectbox(
    "Menú",
    ["Registro Ganado","Registrar Servicio","Registrar Producción","Buscar Res"]
)

# ===================== REGISTRO GANADO =====================
if menu == "Registro Ganado":
    st.subheader("Registro de Ganado")

    # Subir foto
    foto_file = st.file_uploader("Subir foto del ganado", type=["jpg","jpeg","png"])
    nombre = st.text_input("Nombre")
    fecha_nacimiento = st.date_input("Fecha de Nacimiento")
    madre = st.text_input("Nombre Madre")
    padre = st.text_input("Nombre Padre")

    if st.button("Guardar Ganado"):
        if nombre == "":
            st.warning("Debe ingresar el nombre")
        else:
            df = pd.read_excel(archivo, sheet_name="Ganado", engine="openpyxl")
            prod = pd.read_excel(archivo, sheet_name="Produccion", engine="openpyxl")
            serv = pd.read_excel(archivo, sheet_name="Servicio", engine="openpyxl")

            # Guardar foto
            foto_nombre = ""
            if foto_file is not None:
                foto_nombre = f"fotos/{nombre}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
                with open(foto_nombre, "wb") as f:
                    f.write(foto_file.getbuffer())

            nuevo = pd.DataFrame({
                "Foto":[foto_nombre],
                "Nombre":[nombre],
                "Fecha de Nacimiento":[fecha_nacimiento],
                "Madre":[madre],
                "Padre":[padre]
            })

            df = pd.concat([df,nuevo], ignore_index=True)

            with pd.ExcelWriter(archivo, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Ganado", index=False)
                prod.to_excel(writer, sheet_name="Produccion", index=False)
                serv.to_excel(writer, sheet_name="Servicio", index=False)

            st.success("Ganado registrado correctamente")
            if foto_file is not None:
                st.image(foto_nombre, caption="Foto del ganado", use_column_width=True)

# ===================== BUSCAR RES =====================
elif menu == "Buscar Res":
    st.subheader("Buscar ganado")
    nombre = st.text_input("Nombre de la res")

    if st.button("Buscar"):
        ganado = pd.read_excel(archivo, sheet_name="Ganado", engine="openpyxl")
        servicio = pd.read_excel(archivo, sheet_name="Servicio", engine="openpyxl")
        produccion = pd.read_excel(archivo, sheet_name="Produccion", engine="openpyxl")

        res = ganado[ganado["Nombre"] == nombre]
        if not res.empty:
            st.write("Datos del animal")
            st.write(res)

            foto = res.iloc[0]["Foto"]
            if foto and os.path.exists(foto):
                st.image(foto, caption="Foto del ganado", use_column_width=True)

            st.write("Historial de servicios")
            st.write(servicio[servicio["Nombre"] == nombre])

            st.write("Historial de producción")
            st.write(produccion[produccion["Nombre"] == nombre])
        else:
            st.warning("No se encontró la res")

# ===================== REGISTRAR SERVICIO =====================
elif menu == "Registrar Servicio":
    st.subheader("Registrar Servicio")
    nombre = st.text_input("Nombre de la res")
    fecha_servicio = st.date_input("Fecha de servicio")
    toro = st.text_input("Toro")
    finaliza_produccion = st.date_input("Finaliza producción")
    fecha_aprox = st.date_input("Fecha aprox. de parto")
    fecha_parto = st.date_input("Fecha de parto")
    numero_cria = st.number_input("Numero de Cria",0)
    sexo = st.selectbox("Sexo de la cria",["Macho","Hembra"])

    if st.button("Guardar Servicio"):
        ganado = pd.read_excel(archivo, sheet_name="Ganado", engine="openpyxl")
        prod = pd.read_excel(archivo, sheet_name="Produccion", engine="openpyxl")
        serv = pd.read_excel(archivo, sheet_name="Servicio", engine="openpyxl")

        nuevo = pd.DataFrame({
            "Nombre":[nombre],
            "Fecha de Servicio":[fecha_servicio],
            "Toro":[toro],
            "Finaliza Producción":[finaliza_produccion],
            "Fecha aprox. del parto":[fecha_aprox],
            "Fecha de Parto":[fecha_parto],
            "Numero de Cria":[numero_cria],
            "Sexo Cria":[sexo]
        })

        serv = pd.concat([serv,nuevo], ignore_index=True)

        with pd.ExcelWriter(archivo, engine="openpyxl") as writer:
            ganado.to_excel(writer, sheet_name="Ganado", index=False)
            prod.to_excel(writer, sheet_name="Produccion", index=False)
            serv.to_excel(writer, sheet_name="Servicio", index=False)

        st.success("Servicio registrado")

# ===================== REGISTRAR PRODUCCIÓN =====================
elif menu == "Registrar Producción":
    st.subheader("Producción diaria")
    nombre = st.text_input("Nombre de la res")
    litros = st.number_input("Litros producidos",0)

    if st.button("Guardar Producción"):
        ganado = pd.read_excel(archivo, sheet_name="Ganado", engine="openpyxl")
        prod = pd.read_excel(archivo, sheet_name="Produccion", engine="openpyxl")
        serv = pd.read_excel(archivo, sheet_name="Servicio", engine="openpyxl")

        nueva = pd.DataFrame({
            "Fecha":[datetime.now().date()],
            "Nombre":[nombre],
            "Litros":[litros]
        })

        prod = pd.concat([prod,nueva], ignore_index=True)

        with pd.ExcelWriter(archivo, engine="openpyxl") as writer:
            ganado.to_excel(writer, sheet_name="Ganado", index=False)
            prod.to_excel(writer, sheet_name="Produccion", index=False)
            serv.to_excel(writer, sheet_name="Servicio", index=False)

        st.success("Producción guardada")