# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 09:52:37 2024

@author: rmezaf
"""


from selenium import webdriver
import requests
import pandas as pd
from selenium.webdriver.common.by import By
import time
import datetime
#from datetime import datetime, timedelta


fecha_consulta = datetime.datetime(2024, 8, 8)

url = "https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioContable.aspx"
driver = webdriver.Chrome()  # Otra opción es usar Firefox o Edge, dependiendo del navegador
driver.get(url)
date_picker_id = "ctl00_cphContent_rdpDate_dateInput"
date_picker_input = driver.find_element(By.ID, date_picker_id)
date_picker_input.click()

date_value = date_picker_input.get_attribute("value")
#date_value 


fecha_consulta = fecha_consulta.strftime("%d/%m/%Y")
date_picker_input.send_keys(fecha_consulta)

 # Localizar el botón de consulta y hacer clic en él
button_id = "ctl00_cphContent_btnConsultar"  # Reemplaza con el ID del botón de consulta si es diferente
time.sleep(2)
consulta_button = driver.find_element(By.ID, button_id)
consulta_button.click()
# Esperar a que la página cargue los nuevos datos
time.sleep(2) 
#TC Contable
tc_contable_id = "APLI_fila2"
consulta_tccontable = driver.find_elements(By.CLASS_NAME, tc_contable_id)
textos_elementos = [elemento.text for elemento in consulta_tccontable]
print("Textos de los elementos:")
print(textos_elementos)

len(textos_elementos)
 # Conservar solo las filas 2 y 21
filas_conservadas = []
if len(textos_elementos) >= 2:
        filas_conservadas.append(textos_elementos[2])  # Índice 1 corresponde a la segunda fila

# Agregar los datos y la fecha al DataFrame
if len(filas_conservadas) == 1:
    filas_conservadas.append(fecha_consulta)
    
df = pd.DataFrame([filas_conservadas], columns=["TC Contable SBS", "Fecha"])
#df["Fecha"] = fecha_consulta
print(df)

driver.quit()
