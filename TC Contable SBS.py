
from selenium import webdriver
import requests
import pandas as pd
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta

#Cambiar usuario y directorio a preferencia
usuario = 'rmezaf'
directorio = 'C:/Users/' + usuario + '/TC/'  


# URL de la página
url = "https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioContable.aspx"
driver = webdriver.Chrome()  # Otra opción es usar Firefox o Edge, dependiendo del navegador
driver.get(url)

# Identificadores de los elementos
date_picker_id = "ctl00_cphContent_rdpDate_dateInput"
button_id = "ctl00_cphContent_btnConsultar"
tc_sunat_class_name = "APLI_fila2"

# Rango de fechas
fecha_inicio_string = "2024-07-01"
fecha_fin_string = "2024-07-31"
fecha_inicio = datetime.strptime(fecha_inicio_string, "%Y-%m-%d")
fecha_fin = datetime.strptime(fecha_fin_string, "%Y-%m-%d")
delta = timedelta(days=1)

# Calcular el fin de mes de fecha_fin
fin_de_mes = fecha_fin.replace(day=1) + timedelta(days=32)
fin_de_mes = fin_de_mes.replace(day=1) - timedelta(days=1)
fin_de_mes_str = fin_de_mes.strftime("%d/%m/%Y")
fin_de_mes_str_2 = fin_de_mes.strftime("%Y-%m-%d")

# Lista para almacenar los datos
data = []

# Bucle para iterar sobre el rango de fechas
current_date = fecha_inicio
while current_date <= fecha_fin:
    fecha_consulta = current_date.strftime("%d/%m/%Y")
    
    # Ingresar la fecha en el RadDatePicker
    date_picker_input = driver.find_element(By.ID, date_picker_id)
    date_picker_input.clear()
    date_picker_input.send_keys(fecha_consulta)
    
    # Hacer clic en el botón de consulta
    consulta_button = driver.find_element(By.ID, button_id)
    consulta_button.click()
    
    # Esperar a que la página cargue los nuevos datos
    time.sleep(7)  # Ajusta el tiempo de espera según sea necesario
    
    # Extraer los valores de los elementos con la clase especificada
    consulta_tcsunat = driver.find_elements(By.CLASS_NAME, tc_sunat_class_name)
    textos_elementos = [elemento.text for elemento in consulta_tcsunat]
    
    # Conservar las filas dependiendo si el día es par o impar
    
    filas_conservadas = []
    if len(textos_elementos) >= 2:
            filas_conservadas.append(textos_elementos[2])  # Índice 1 corresponde a la segunda fila
 
    # Agregar los datos y la fecha al DataFrame
    if len(filas_conservadas) == 1:
        data.append(filas_conservadas + [fecha_consulta])
    
    # Avanzar a la siguiente fecha
    current_date += delta

# Crear el DataFrame
df = pd.DataFrame(data, columns=["TC Contable", "Fecha"])
# Verificar si existe una fila con la fecha de fin de mes
if df[df['Fecha'] == fin_de_mes_str].empty:
    # Duplicar la última fila disponible y modificar la fecha al fin de mes
    ultima_fila = df.iloc[-1].copy()
    ultima_fila['Fecha'] = fin_de_mes_str
    df = pd.concat([df, pd.DataFrame([ultima_fila])], ignore_index=True)


df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d/%m/%Y")
df["TC Contable"] = pd.to_numeric(df["TC Contable"]) 


df.to_excel(directorio + 'TC Contable ' + fin_de_mes_str_2 + '.xlsx', index=False)
# Cerrar el navegador
driver.quit()

