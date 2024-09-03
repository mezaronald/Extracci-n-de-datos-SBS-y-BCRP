
from selenium import webdriver
import requests
import pandas as pd
from selenium.webdriver.common.by import By
import time
import datetime
#from datetime import datetime, timedelta
import os
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

usuario = "rmezaf" #Cambiar a preferencia
fecha_consulta = datetime.datetime(2024, 9, 2)
fecha_consultaA = fecha_consulta.strftime("%d/%m/%Y")
fecha_consultaB = fecha_consulta.strftime("%y%m%d")

# Define la ubicación y el nombre del archivo que deseas descargar

download_directory = "C:\\Users\\"+ usuario +"\\Vector Precios\\" 

download_filename = "Vector SBS " + fecha_consultaB + ".xls"


chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False
}
chrome_options.add_experimental_option("prefs", prefs)

url = "https://www.sbs.gob.pe/app/pu/ccid/paginas/vp_rentafija.aspx"
driver = webdriver.Chrome(options = chrome_options) 
#driver = webdriver.Chrome()  # Otra opción es usar Firefox o Edge, dependiendo del navegador
driver.get(url)
date_picker_id = "cboFecProceso"
date_picker_input = driver.find_element(By.ID, date_picker_id)
date_picker_input.click()

date_value = date_picker_input.get_attribute("value")



date_picker_input.send_keys(fecha_consultaA)

 # Localizar el botón de consulta y hacer clic en él
button_id = "btnConsultar"  # Reemplaza con el ID del botón de consulta si es diferente
#time.sleep(2)
consulta_button = driver.find_element(By.ID, button_id)
consulta_button.click()

url_descarga = "https://www.sbs.gob.pe/app/pu/ccid/Exportar/exportar_reporte.aspx?tipo=4"
driver.get(url_descarga)


time.sleep(6)
downloaded_file_path = os.path.join(download_directory, "Renta Fija.xls")  # Ajusta el nombre si es necesario
new_file_path = os.path.join(download_directory, download_filename)
os.rename(downloaded_file_path, new_file_path)

driver.quit()
