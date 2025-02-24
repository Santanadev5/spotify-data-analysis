import os
import json
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

# Configuração do caminho do arquivo kaggle.json
kaggle_json_path = os.path.expanduser("~/.kaggle/kaggle.json")

# Verifica se o arquivo existe
try:
    with open(kaggle_json_path, 'r') as file:
        dados = json.load(file)
except FileNotFoundError:
    print("❌ Arquivo 'kaggle.json' não encontrado! Baixe-o no Kaggle e coloque na pasta ~/.kaggle/")
    exit()
except json.JSONDecodeError:
    print("❌ Erro ao ler o JSON do 'kaggle.json'!")
    exit()

# Configurar variáveis de ambiente
os.environ['KAGGLE_USERNAME'] = dados['username']
os.environ['KAGGLE_KEY'] = dados['key']

# Autenticação no Kaggle e download do dataset
try:
    api = KaggleApi()
    api.authenticate()
    print("✅ Autenticação bem-sucedida!")

    dataset_name = "dhruvildave/spotify-charts"  # Novo dataset
    download_path = "./data"
    api.dataset_download_files(dataset_name, path=download_path, unzip=True)
    print(f"✅ Dataset '{dataset_name}' baixado com sucesso!")

except Exception as e:
    print(f"❌ Erro: {e}")
    exit()

# Verificar qual arquivo foi baixado
arquivos_baixados = os.listdir(download_path)
print("\n📂 Arquivos baixados:", arquivos_baixados)

# Definir o nome correto do arquivo CSV
csv_path = f"{download_path}/charts.csv"  # Nome correto do novo dataset!

# Carregar o dataset
try:
    df = pd.read_csv(csv_path)
    print("✅ Dataset carregado!")
    print(df.head())  # Mostrar as primeiras linhas do dataset
except FileNotFoundError:
    print(f"❌ Arquivo {csv_path} não encontrado. Verifique o nome do arquivo baixado!")
    exit()
except Exception as e:
    print(f"❌ Erro ao carregar o dataset: {e}")
    exit()

# Verificar valores nulos
missing_values = df.isnull().sum()
missing_percent = (missing_values / len(df)) * 100

# Verificar valores iguais a 0 (somente para colunas numéricas)
zero_values = (df == 0).sum()
zero_percent = (zero_values / len(df)) * 100

# Exibir resultados
print("\n🔍 Valores nulos por coluna:")
print(pd.DataFrame({'Valores Nulos': missing_values, 'Percentual (%)': missing_percent}))

print("\n🔍 Valores iguais a 0 por coluna:")
print(pd.DataFrame({'Valores 0': zero_values, 'Percentual (%)': zero_percent}))
