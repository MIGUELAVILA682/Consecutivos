import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Tu enlace compartido de SharePoint
url = "https://argconsultoresyserviciossas-my.sharepoint.com/:x:/g/personal/mavila_arg_net_co/EQbwXc_HWmBLorw52Kts_8sBSkyxeU5Dt-_BH5jZxj1yIQ?e=x6u1OW"

st.title("Lectura de archivo Excel desde OneDrive/SharePoint")

try:
    # Descargar el archivo
    response = requests.get(url)
    response.raise_for_status()

    # Leerlo con pandas
    df = pd.read_excel(BytesIO(response.content))
    st.success("Archivo cargado correctamente.")
    st.dataframe(df)

except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
