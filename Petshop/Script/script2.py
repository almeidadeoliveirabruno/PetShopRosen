import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Carrega a planilha
planilha = pd.read_excel('Registros.xlsx')

# --- Separando os DataFrames ---
registros_donos = planilha.iloc[:, 4:8].apply(lambda x: x.str.strip() if x.dtype == "object" else x).drop_duplicates()
registros_planos = planilha.iloc[:, 8:11].apply(lambda x: x.str.strip() if x.dtype == "object" else x).drop_duplicates()
registros_animais = planilha[["Nome do Animal","Espécie","Raça","Data de Nascimento","Nome do Dono","Plano do Animal"]]

# --- Inicializa o WebDriver ---
driver = webdriver.Chrome()
base_url = 'https://localhost:7280/'

# -----------------------
# 1) Cadastro de Clientes
# -----------------------
for i in range(len(registros_donos)):
    driver.get(f'{base_url}Clientes/Create')
    
    # Espera os campos carregarem
    nome = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Nome"]')))
    email = driver.find_element(By.XPATH,'//*[@id="Email"]')
    telefone = driver.find_element(By.XPATH,'//*[@id="Telefone"]')
    endereco = driver.find_element(By.XPATH,'//*[@id="Endereco"]')
    cadastrar = driver.find_element(By.XPATH,'/html/body/main/div/form/div[5]/input')

    # Limpa e preenche
    nome.clear()
    nome.send_keys(registros_donos['Nome do Dono'].values[i])
    email.clear()
    email.send_keys(registros_donos['Email do Dono'].values[i])
    telefone.clear()
    telefone.send_keys(registros_donos['Telefone do Dono'].values[i])
    endereco.clear()
    endereco.send_keys(registros_donos['Endereço do Dono'].values[i])

    # Garante que o botão esteja visível e clicável
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div/form/div[5]/input')))
    driver.execute_script("arguments[0].scrollIntoView(true);", cadastrar)
    driver.execute_script("arguments[0].click();", cadastrar)

# -----------------------
# 2) Cadastro de Planos
# -----------------------
# Espera menu de Planos estar clicável
planos_menu = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainNav"]/ul/li[4]/a'))
)
planos_menu.click()

# Espera botão "Novo Plano"
novo_plano_btn = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div[1]/div/a[1]'))
)
novo_plano_btn.click()

for i in range(len(registros_planos)):
    cadastrar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,'/html/body/main/div/form/div[4]/input'))
    )
    
    nome = driver.find_element(By.XPATH,'//*[@id="Nome"]')
    preco = driver.find_element(By.XPATH,'//*[@id="Preco"]')
    descricao = driver.find_element(By.XPATH,'//*[@id="Descricao"]')

    nome.clear()
    preco.clear()
    descricao.clear()

    nome.send_keys(registros_planos['Plano do Animal'].values[i])
    preco.send_keys(str(registros_planos['Preço do Plano'].values[i]))
    descricao.send_keys(registros_planos['Descrição do Plano'].values[i])

    driver.execute_script("arguments[0].scrollIntoView(true);", cadastrar)
    driver.execute_script("arguments[0].click();", cadastrar)

# -----------------------
# 3) Cadastro de Animais
# -----------------------
animais_menu = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="mainNav"]/ul/li[2]/a'))
)
animais_menu.click()

novo_animal_btn = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/div[1]/div/a[1]'))
)
novo_animal_btn.click()

for i in range(len(registros_animais)):
    cadastrar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/main/div/form/div[7]/input'))
    )

    nome = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Nome"]')))
    especie = Select(driver.find_element(By.XPATH,'//*[@id="Especie"]'))
    raca = driver.find_element(By.XPATH,'//*[@id="Raca"]')
    data_nascimento = driver.find_element(By.XPATH,'//*[@id="DataNascimento"]')
    dono_select = Select(driver.find_element(By.XPATH,'//*[@id="ClienteId"]'))
    plano_select = Select(driver.find_element(By.XPATH,'//*[@id="PlanoId"]'))

    nome.clear()
    nome.send_keys(registros_animais['Nome do Animal'].values[i])

    especie.select_by_visible_text(registros_animais['Espécie'].values[i])
    raca.clear()
    raca.send_keys(registros_animais['Raça'].values[i])

    # Converte data para YYYY-MM-DD (C#)
    data_str = pd.to_datetime(registros_animais['Data de Nascimento'].values[i]).strftime('%Y-%m-%d')
    data_nascimento.clear()
    data_nascimento.send_keys(data_str)

    dono_select.select_by_visible_text(registros_animais['Nome do Dono'].values[i])
    plano_select.select_by_visible_text(registros_animais['Plano do Animal'].values[i])

    driver.execute_script("arguments[0].scrollIntoView(true);", cadastrar)
    driver.execute_script("arguments[0].click();", cadastrar)

# Mantém o navegador aberto
input('Cadastro concluído! Pressione Enter para fechar o navegador...')
driver.quit()
