import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


planilha = pd.read_excel('Registros.xlsx')

#separando os dataframes
registros_donos = planilha.iloc[:, 4:8]
registros_donos = registros_donos.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
registros_donos = registros_donos.drop_duplicates()

registros_planos = planilha.iloc[:,8:11]
registros_planos = registros_planos.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
registros_planos = registros_planos.drop_duplicates()

registros_animais = planilha[["Nome do Animal","Espécie",'Raça','Data de Nascimento','Nome do Dono','Plano do Animal']]

driver = webdriver.Chrome()
base_url = 'https://localhost:7280/'

for i in range(len(registros_donos)):
    driver.get(f'{base_url}Clientes/Create')  # Vai para a página de cadastro
    
    # Espera os elementos carregarem
    nome = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="Nome"]'))
    )
    email = driver.find_element(By.XPATH,'//*[@id="Email"]')
    telefone = driver.find_element(By.XPATH,'//*[@id="Telefone"]')
    endereco = driver.find_element(By.XPATH,'//*[@id="Endereco"]')
    cadastrar = driver.find_element(By.XPATH,'/html/body/main/div/form/div[5]/input')

    nome.clear()
    email.clear()
    telefone.clear()
    endereco.clear()

    nome.send_keys(registros_donos['Nome do Dono'].values[i])
    email.send_keys(registros_donos['Email do Dono'].values[i])
    telefone.send_keys(registros_donos['Telefone do Dono'].values[i])
    endereco.send_keys(registros_donos['Endereço do Dono'].values[i])
    cadastrar.click()

    if i != len(registros_donos) - 1:
        
        WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div[1]/div/a[1]'))
    )
        voltar_pagina = driver.find_element(By.XPATH,'/html/body/main/div/div[1]/div/a[1]')
        voltar_pagina.click()


# Planos
driver.find_element(By.XPATH,'//*[@id="mainNav"]/ul/li[4]/a').click()
driver.find_element(By.XPATH,'/html/body/main/div/div[1]/div/a[1]').click()
for i in range(len(registros_planos)):
  # Vai para a página de cadastro
    cadastrar = driver.find_element(By.XPATH,'/html/body/main/div/form/div[4]/input')
    # Espera os elementos carregarem
    nome = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="Nome"]'))
    ) 
    preco = driver.find_element(By.XPATH,'//*[@id="Preco"]')
    descricao = driver.find_element(By.XPATH,'//*[@id="Descricao"]')
   
    nome.clear()
    preco.clear()
    descricao.clear()

    nome.send_keys(registros_planos['Plano do Animal'].values[i])
    preco.send_keys(str(registros_planos['Preço do Plano'].values[i]))
    descricao.send_keys(registros_planos['Descrição do Plano'].values[i])
    cadastrar.click()

    if i != len(registros_planos) - 1:
        
        WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div[1]/div/a[1]'))
    )
        voltar_pagina = driver.find_element(By.XPATH,'/html/body/main/div/div[1]/div/a[1]')
        voltar_pagina.click()


# Animais
driver.find_element(By.XPATH,'//*[@id="mainNav"]/ul/li[2]/a').click()
driver.find_element(By.XPATH,'/html/body/main/div/div[1]/div/a[1]').click()
for i in range(len(registros_animais)):
    # Espera o botão de cadastrar estar presente
    cadastrar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/main/div/form/div[7]/input'))
    )

    # Localiza os campos
    nome = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Nome"]')))
    especie = Select(driver.find_element(By.XPATH,'//*[@id="Especie"]'))
    raca = driver.find_element(By.XPATH,'//*[@id="Raca"]')
    data_nascimento = driver.find_element(By.XPATH,'//*[@id="DataNascimento"]')
    dono_select = Select(driver.find_element(By.XPATH,'//*[@id="ClienteId"]'))
    plano_select = Select(driver.find_element(By.XPATH,'//*[@id="PlanoId"]'))

    # Preenche os campos
    nome.clear()
    nome.send_keys(registros_animais['Nome do Animal'].values[i])

    especie.select_by_visible_text(registros_animais['Espécie'].values[i])

    raca.clear()
    raca.send_keys(registros_animais['Raça'].values[i])

    # Converte data para string YYYY-MM-DD
    data_str = pd.to_datetime(registros_animais['Data de Nascimento'].values[i]).strftime('%d-%m-%Y')
    data_nascimento.clear()
    data_nascimento.send_keys(data_str)

    # Seleciona dono e plano
    dono_select.select_by_visible_text(registros_animais['Nome do Dono'].values[i])
    plano_select.select_by_visible_text(registros_animais['Plano do Animal'].values[i])

    # Garante que o botão esteja visível antes de clicar
    driver.execute_script("arguments[0].scrollIntoView(true);", cadastrar)
    driver.execute_script("arguments[0].click();", cadastrar)

    if i != len(registros_animais) - 1:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div[1]/div/a[1]'))
        )
        voltar_pagina = driver.find_element(By.XPATH,'/html/body/main/div/div[1]/div/a[1]')
        voltar_pagina.click()



input('')
