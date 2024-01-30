import os
import re
from PyPDF2 import PdfReader
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import Select

# Alterar para o caminho do chromedriver no seu PC
chrome_driver_path = "C:/chromedriver-win64/chromedriver.exe"
chrome_options = ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(executable_path=chrome_driver_path), options=chrome_options)

try:
    driver.get("http://diariooficial.imprensaoficial.com.br/nav_v6/index.asp?c=34031&e=20231030&p=1")

    # Aguarde até que o iframe esteja presente
    iframe = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'topFrame'))
    )

    # Mudando para o iframe onde será realizado o primeiro passo
    driver.switch_to.frame(iframe)

    # Aguarde até que o select esteja presente
    select_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'pg'))
    )

    # Crie um objeto Select para o elemento select
    select = Select(select_element)

    for option in select.options:
        if "137" in option.get_attribute("value") and "____Educação" in option.text:
            select.select_by_value(option.get_attribute("value"))
            break

    driver.switch_to.default_content()

    # Aguarde até que o iframe do PDF esteja presente
    pdf_iframe = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'frame'))
    )

    # Mude para o iframe do PDF
    driver.switch_to.frame(pdf_iframe)

    # Obtenha o URL do PDF
    pdf_url = driver.current_url

    # Utilize urllib para baixar o PDF
    pdf_path = os.path.join(os.getcwd(), 'pg_0137.pdf')

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)

        all_occurrences = []
        contagem = 0
        string_tdp = r'TOMADA\s*DE\s*PREÇOS'
        for page_number, page in enumerate(pdf_reader.pages, 1):
            page_text = page.extract_text()
            occurrences = re.finditer(string_tdp, page_text)

            for match in occurrences:
                # Agora, para cada ocorrência de "TOMADA DE PREÇOS", vamos procurar pelo número associado
                number_match = re.search(r'Nº:\s*(\d+\s*/[\d\s/]+)', page_text[match.end():])
                if number_match:
                    contagem += 1
                    print(f"Ocorrência {contagem} na página {page_number}: {match.group(0)} {number_match.group(1)}")

finally:
    # Certifique-se de sair do iframe antes de fechar o navegador
    driver.switch_to.default_content()
    # Certifique-se de fechar o navegador ao finalizar
    driver.quit()
