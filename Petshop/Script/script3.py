import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Carrega a planilha
planilha = pd.read_excel('Registros.xlsx')

# Separando os DataFrames
registros_donos = planilha.iloc[:, 4:8].apply(lambda x: x.str.strip() if x.dtype == "object" else x).drop_duplicates()
registros_planos = planilha.iloc[:, 8:11].apply(lambda x: x.str.strip() if x.dtype == "object" else x).drop_duplicates()
registros_animais = planilha[["Nome do Animal","Espécie",'Raça','Data de Nascimento','Nome do Dono','Plano do Animal']]

# Inicializa driver
driver = webdriver.Chrome()
base_url = 'https://localhost:7280/'

# --- CADASTRO DE CLIENTES ---
for i in range(len(registros_donos)):
    driver.get(f'{base_url}Clientes/Create')
    
    nome = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "Nome")))
    email = driver.find_element(By.ID, "Email")
    telefone = driver.find_element(By.ID, "Telefone")
    endereco = driver.find_element(By.ID, "Endereco")
    cadastrar = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Cadastrar']")

    # Preenche campos
    nome.clear(); nome.send_keys(registros_donos['Nome do Dono'].values[i])
    email.clear(); email.send_keys(registros_donos['Email do Dono'].values[i])
    telefone.clear(); telefone.send_keys(registros_donos['Telefone do Dono'].values[i])
    endereco.clear(); endereco.send_keys(registros_donos['Endereço do Dono'].values[i])

    # Clica no botão de cadastrar de forma segura
    driver.execute_script("arguments[0].scrollIntoView(true);", cadastrar)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Cadastrar']")))
    driver.execute_script("arguments[0].click();", cadastrar)

# --- CADASTRO DE PLANOS ---
for i in range(len(registros_planos)):
    driver.get(f'{base_url}Planos/Create')
    
    nome = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "Nome")))
    preco = driver.find_element(By.ID, "Preco")
    descricao = driver.find_element(By.ID, "Descricao")
    cadastrar = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Cadastrar']")

    nome.clear(); nome.send_keys(registros_planos['Plano do Animal'].values[i])
    preco.clear(); preco.send_keys(str(registros_planos['Preço do Plano'].values[i]))
    descricao.clear(); descricao.send_keys(registros_planos['Descrição do Plano'].values[i])

    driver.execute_script("arguments[0].scrollIntoView(true);", cadastrar)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Cadastrar']")))
    driver.execute_script("arguments[0].click();", cadastrar)

# --- CADASTRO DE ANIMAIS ---
for i in range(len(registros_animais)):
    driver.get(f'{base_url}Animais/Create')
    
    nome = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "Nome")))
    especie = Select(driver.find_element(By.ID, "Especie"))
    raca = driver.find_element(By.ID, "Raca")
    data_nascimento = driver.find_element(By.ID, "DataNascimento")
    dono_select = Select(driver.find_element(By.ID, "ClienteId"))
    plano_select = Select(driver.find_element(By.ID, "PlanoId"))
    cadastrar = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Cadastrar']")

    # Preenche campos
    nome.clear(); nome.send_keys(registros_animais['Nome do Animal'].values[i])
    especie.select_by_visible_text(registros_animais['Espécie'].values[i])
    raca.clear(); raca.send_keys(registros_animais['Raça'].values[i])

    # Converte data para YYYY-MM-DD (formato aceito pelo input date do HTML)
    data_str = pd.to_datetime(registros_animais['Data de Nascimento'].values[i]).strftime('%d-%m-%Y')
    data_nascimento.clear(); data_nascimento.send_keys(data_str)

    # Seleciona dono e plano
    dono_select.select_by_visible_text(registros_animais['Nome do Dono'].values[i])
    plano_select.select_by_visible_text(registros_animais['Plano do Animal'].values[i])

    driver.execute_script("arguments[0].scrollIntoView(true);", cadastrar)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Cadastrar']")))
    driver.execute_script("arguments[0].click();", cadastrar)

# Mantém o navegador aberto ao final
input("Todos os cadastros concluídos. Pressione Enter para fechar o navegador.")
driver.quit()
