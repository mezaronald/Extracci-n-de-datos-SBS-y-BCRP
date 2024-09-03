# -*- coding: utf-8 -*-

from selenium import webdriver
import requests
import pandas as pd
from selenium.webdriver.common.by import By
import time
import datetime
import os
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


TipoCurva='CBCRS' #CDs
#TipoCurva= 'CCPSS' #Soberana
#TipoCurva= 'CCPEDS' #Treasuries

FechaInicio0 = datetime.datetime(2024, 9, 2)
FechaFin0 = datetime.datetime(2024, 9, 2)

FechaInicio = FechaInicio0.strftime("%d/%m/%Y")
FechaInicioB = FechaInicio0.strftime("%y%m%d")
FechaInicioC = FechaInicio0.strftime("%B%y")

FechaFin = FechaFin0.strftime("%d/%m/%Y")
FechaFinB = FechaFin0.strftime("%y%m%d")


# Define la ubicación y el nombre del archivo que deseas descargar
download_directory = "C:\\Users\\"+ usuario +"\\Curva CD\\" # Definir ruta a preferencia
download_filename = "Curva CD " + FechaInicioB + " " + FechaFinB + ".xlsx"
#download_filename = "Curva_Soberano_" + FechaInicioC + ".xlsx"
#download_filename = "Curva_Soberano_" + FechaInicioC + ".xlsx"

#obtiene todos los datos de la curva de cupon cero de un determinado fecha de proceso
#df_cup_hist = cc.get_curva_cupon_cero_historico(FechaInicio=inicio,FechaFin=fin,TipoCurva=tipoCurva)
#df_cup_hist.head()

chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False
}
chrome_options.add_experimental_option("prefs", prefs)


URL = "https://www.sbs.gob.pe/app/pp/n_CurvaSoberana/CurvaSoberana/ConsultaHistorica" 

driver = webdriver.Chrome(options = chrome_options)  # Otra opción es usar Firefox o Edge, dependiendo del navegador
#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
#driver = webdriver.Chrome() 

driver.get(URL)
date_picker_id = "txtFiltroFechaInicio"
date_picker_input = driver.find_element(By.ID, date_picker_id)
driver.execute_script(f"arguments[0].value = '{FechaInicio}';", date_picker_input)
date_value = date_picker_input.get_attribute("value")
date_value 


date_picker_id2 = "txtFiltroFechaFin"
date_picker_input2 = driver.find_element(By.ID, date_picker_id2)
driver.execute_script(f"arguments[0].value = '{FechaFin}';", date_picker_input2)
date_value2 = date_picker_input2.get_attribute("value")
date_value2

curve_picker_id = "cboFiltroTipoCurva"
curve_picker_input = driver.find_element(By.ID, curve_picker_id)
driver.execute_script(f"arguments[0].value = '{TipoCurva}';", curve_picker_input)
curve_value = curve_picker_input.get_attribute("value")
curve_value

button_id = "btnBuscarInformacionHistorica" 
consulta_button = driver.find_element(By.ID, button_id)
time.sleep(5)
consulta_button.click()

time.sleep(8)

downloaded_file_path = os.path.join(download_directory, "curva_historica.xlsx")  # Ajusta el nombre si es necesario

time.sleep(2)
new_file_path = os.path.join(download_directory, download_filename)
os.rename(downloaded_file_path, new_file_path)
driver.quit()

download_directory
