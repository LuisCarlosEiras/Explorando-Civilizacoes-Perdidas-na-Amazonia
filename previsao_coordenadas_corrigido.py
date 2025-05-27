import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.impute import SimpleImputer

# Configuração do diretório de trabalho
base_dir = '/home/ubuntu/amazonia-explorador'
dados_dir = os.path.join(base_dir, 'dados')
resultados_dir = os.path.join(base_dir, 'resultados')
coordenadas_dir = os.path.join(resultados_dir, 'coordenadas')

# Criar diretório de coordenadas se não existir
if not os.path.exists(coordenadas_dir):
    os.makedirs(coordenadas_dir)

# Função para gerar dados simulados de treinamento
def gerar_dados_treinamento(n_amostras=1000, ruido=0.2):
    """
    Gera dados simulados para treinamento dos modelos preditivos
    
    Parâmetros:
    n_amostras: número de amostras a serem geradas
    ruido: nível de ruído nos dados
    
    Retorna:
    X: features (características ambientais e topográficas)
    y: labels (1 para sítio arqueológico, 0 para não-sítio)
    """
    # Características simuladas
    # Elevação (m)
    elevacao = np.random.uniform(50, 300, n_amostras)
    
    # Distância de rios (km)
    dist_rios = np.random.exponential(5, n_amostras)
    
    # Declividade (graus)
    declividade = np.random.gamma(2, 2, n_amostras)
    
    # Índice de vegetação (NDVI)
    ndvi = np.random.beta(2, 2, n_amostras)
    
    # Tipo de solo (categórico: 0, 1, 2, 3)
    tipo_solo = np.random.randint(0, 4, n_amostras)
    
    # Precipitação anual (mm)
    precipitacao = np.random.normal(2000, 500, n_amostras)
    
    # Temperatura média (°C)
    temperatura = np.random.normal(25, 3, n_amostras)
    
    # Combinar características
    X = np.column_stack((elevacao, dist_rios, declividade, ndvi, tipo_solo, precipitacao, temperatura))
    
    # Gerar labels com base em regras que simulam preferências de assentamento
    # Sítios tendem a estar:
    # - Em elevações moderadas (100-200m)
    # - Próximos a rios (<3km)
    # - Em áreas com declividade baixa (<5°)
    # - Em áreas com vegetação moderada a alta (NDVI > 0.4)
    # - Em certos tipos de solo (1 e 2)
    # - Em áreas com precipitação moderada (1500-2500mm)
    
    probabilidade = (
        (1 - np.abs(elevacao - 150) / 150) * 0.3 +  # Preferência por elevações moderadas
        (1 - np.minimum(dist_rios / 10, 1)) * 0.25 +  # Preferência por proximidade a rios
        (1 - np.minimum(declividade / 10, 1)) * 0.15 +  # Preferência por áreas planas
        (ndvi * 0.1) +  # Preferência por vegetação mais densa
        ((tipo_solo == 1) | (tipo_solo == 2)) * 0.1 +  # Preferência por certos tipos de solo
        (1 - np.abs(precipitacao - 2000) / 1000) * 0.1  # Preferência por precipitação moderada
    )
    
    # Adicionar ruído
    probabilidade += np.random.normal(0, ruido, n_amostras)
    
    # Converter para classificação binária
    y = (probabilidade > 0.6).astype(int)
    
    # Criar DataFrame para melhor visualização
    colunas = ['Elevacao', 'Dist_Rios', 'Declividade', 'NDVI', 'Tipo_Solo', 'Precipitacao', 'Temperatura']
    X_df = pd.DataFrame(X, columns=colunas)
    
    return X_df, y

# Método 1: Modelo baseado em características ambientais e topográficas
def metodo_1_ambiental(X_train, y_train, X_test):
    """
    Método 1: Previsão baseada em características ambientais e topográficas
    usando Random Forest
    
    Parâmetros:
    X_train: features de treinamento
    y_train: labels de treinamento
    X_test: features de teste
    
    Retorna:
    y_pred: previsões para os dados de teste
    importancia: importância das features
    """
    print("Método 1: Aplicando modelo baseado em características ambientais e topográficas...")
    
    # Treinar modelo Random Forest
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    
    # Fazer previsões
    y_pred = modelo.predict(X_test)
    
    # Calcular importância das features
    importancia = pd.DataFrame({
        'Feature': X_train.columns,
        'Importância': modelo.feature_importances_
    }).sort_values('Importância', ascending=False)
    
    return y_pred, importancia

# Método 2: Modelo baseado em padrões espaciais e proximidade
def metodo_2_espacial(X_train, y_train, X_test, coords_train, coords_test):
    """
    Método 2: Previsão baseada em padrões espaciais e proximidade
    usando Gradient Boosting e informações de vizinhança
    
    Parâmetros:
    X_train: features de treinamento
    y_train: labels de treinamento
    X_test: features de teste
    coords_train: coordenadas dos pontos de treinamento
    coords_test: coordenadas dos pontos de teste
    
    Retorna:
    y_pred: previsões para os dados de teste
    """
    print("Método 2: Aplicando modelo baseado em padrões espaciais e proximidade...")
    
    # Adicionar características de vizinhança
    X_train_espacial = X_train.copy()
    X_test_espacial = X_test.copy()
    
    # Para cada ponto, calcular distância para o sítio conhecido mais próximo
    for i, (lat, lon) in enumerate(coords_test):
        # Calcular distâncias para todos os sítios conhecidos (onde y_train == 1)
        sitios_conhecidos = coords_train[y_train == 1]
        if len(sitios_conhecidos) > 0:
            distancias = np.sqrt(((sitios_conhecidos[:, 0] - lat) ** 2) + 
                                ((sitios_conhecidos[:, 1] - lon) ** 2))
            dist_min = np.min(distancias)
        else:
            dist_min = 999  # Valor alto se não houver sítios conhecidos
        
        # Adicionar como nova feature
        X_test_espacial.loc[i, 'Dist_Sitio_Proximo'] = dist_min
    
    # Para os dados de treinamento, usar validação cruzada para evitar vazamento de dados
    for i, (lat, lon) in enumerate(coords_train):
        # Excluir o próprio ponto
        outros_sitios = np.delete(coords_train, i, axis=0)
        outros_y = np.delete(y_train, i)
        
        # Calcular distâncias para todos os outros sítios conhecidos
        sitios_conhecidos = outros_sitios[outros_y == 1]
        if len(sitios_conhecidos) > 0:
            distancias = np.sqrt(((sitios_conhecidos[:, 0] - lat) ** 2) + 
                                ((sitios_conhecidos[:, 1] - lon) ** 2))
            dist_min = np.min(distancias)
        else:
            dist_min = 999
        
        X_train_espacial.loc[i, 'Dist_Sitio_Proximo'] = dist_min
    
    # Pré-processamento: Imputação de valores NaN
    imputer = SimpleImputer(strategy='mean')
    X_train_espacial_imputed = imputer.fit_transform(X_train_espacial)
    X_test_espacial_imputed = imputer.transform(X_test_espacial)
    
    # Treinar modelo Gradient Boosting
    modelo = GradientBoostingClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train_espacial_imputed, y_train)
    
    # Fazer previsões
    y_pred = modelo.predict(X_test_espacial_imputed)
    
    return y_pred

# Função para gerar coordenadas simuladas
def gerar_coordenadas_simuladas(n_amostras, regiao='amazonia'):
    """
    Gera coordenadas simuladas para a região amazônica
    
    Parâmetros:
    n_amostras: número de coordenadas a serem geradas
    regiao: região geográfica ('amazonia', 'acre', 'xingu', 'tapajos')
    
    Retorna:
    coords: array com pares [latitude, longitude]
    """
    if regiao == 'amazonia':
        # Região geral da Amazônia brasileira
        lat_min, lat_max = -10.0, -2.0
        lon_min, lon_max = -70.0, -50.0
    elif regiao == 'acre':
        # Região dos geoglifos do Acre
        lat_min, lat_max = -11.0, -8.0
        lon_min, lon_max = -70.0, -67.0
    elif regiao == 'xingu':
        # Região do Alto Xingu
        lat_min, lat_max = -13.0, -11.0
        lon_min, lon_max = -54.0, -52.0
    elif regiao == 'tapajos':
        # Região do Alto Tapajós
        lat_min, lat_max = -9.0, -7.0
        lon_min, lon_max = -58.0, -56.0
    else:
        raise ValueError("Região não reconhecida")
    
    # Gerar coordenadas aleatórias dentro da região
    latitudes = np.random.uniform(lat_min, lat_max, n_amostras)
    longitudes = np.random.uniform(lon_min, lon_max, n_amostras)
    
    return np.column_stack((latitudes, longitudes))

# Função para comparar e validar resultados dos dois métodos
def comparar_metodos(y_true, y_pred_1, y_pred_2):
    """
    Compara os resultados dos dois métodos de previsão
    
    Parâmetros:
    y_true: valores reais
    y_pred_1: previsões do método 1
    y_pred_2: previsões do método 2
    
    Retorna:
    metricas: dicionário com métricas de comparação
    """
    # Calcular acurácia de cada método
    acc_1 = accuracy_score(y_true, y_pred_1)
    acc_2 = accuracy_score(y_true, y_pred_2)
    
    # Calcular matrizes de confusão
    cm_1 = confusion_matrix(y_true, y_pred_1)
    cm_2 = confusion_matrix(y_true, y_pred_2)
    
    # Calcular concordância entre os métodos
    concordancia = np.mean(y_pred_1 == y_pred_2)
    
    # Identificar previsões onde os métodos concordam
    concordam = y_pred_1 == y_pred_2
    
    # Acurácia quando os métodos concordam
    if np.sum(concordam) > 0:
        acc_concordancia = accuracy_score(y_true[concordam], y_pred_1[concordam])
    else:
        acc_concordancia = 0
    
    metricas = {
        'Acurácia Método 1': acc_1,
        'Acurácia Método 2': acc_2,
        'Concordância entre métodos': concordancia,
        'Acurácia quando concordam': acc_concordancia,
        'Matriz Confusão Método 1': cm_1,
        'Matriz Confusão Método 2': cm_2
    }
    
    return metricas

# Função para visualizar resultados em mapa simplificado
def visualizar_mapa_simplificado(coords, y_true, y_pred_1, y_pred_2, regiao, filename):
    """
    Visualiza os resultados em um mapa simplificado (sem geopandas)
    
    Parâmetros:
    coords: coordenadas dos pontos [latitude, longitude]
    y_true: valores reais
    y_pred_1: previsões do método 1
    y_pred_2: previsões do método 2
    regiao: nome da região
    filename: nome do arquivo para salvar
    """
    # Configurar figura
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Plotar pontos
    # Sítios reais
    sitios_reais = np.where(y_true == 1)[0]
    ax.scatter(coords[sitios_reais, 1], coords[sitios_reais, 0], 
              c='green', marker='o', s=100, label='Sítio Real', alpha=0.7)
    
    # Previsões corretas de ambos os métodos
    corretos_ambos = np.where((y_true == y_pred_1) & (y_true == y_pred_2))[0]
    ax.scatter(coords[corretos_ambos, 1], coords[corretos_ambos, 0], 
              c='blue', marker='s', s=80, label='Previsão Correta (Ambos)', alpha=0.5)
    
    # Previsões corretas apenas do método 1
    corretos_m1 = np.where((y_true == y_pred_1) & (y_true != y_pred_2))[0]
    ax.scatter(coords[corretos_m1, 1], coords[corretos_m1, 0], 
              c='cyan', marker='^', s=80, label='Previsão Correta (Método 1)', alpha=0.5)
    
    # Previsões corretas apenas do método 2
    corretos_m2 = np.where((y_true != y_pred_1) & (y_true == y_pred_2))[0]
    ax.scatter(coords[corretos_m2, 1], coords[corretos_m2, 0], 
              c='purple', marker='v', s=80, label='Previsão Correta (Método 2)', alpha=0.5)
    
    # Previsões incorretas de ambos os métodos
    incorretos = np.where((y_true != y_pred_1) & (y_true != y_pred_2))[0]
    ax.scatter(coords[incorretos, 1], coords[incorretos, 0], 
              c='red', marker='x', s=80, label='Previsão Incorreta (Ambos)', alpha=0.5)
    
    # Configurar título e legendas
    ax.set_title(f'Previsão de Sítios Arqueológicos - Região: {regiao.title()}', fontsize=16)
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.legend(loc='upper right')
    
    # Adicionar grade
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Salvar figura
    caminho_completo = os.path.join(coordenadas_dir, filename)
    plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho_completo

# Função principal para demonstrar o fluxo de trabalho
def demonstrar_previsao_coordenadas():
    """
    Demonstra o fluxo de trabalho completo para previsão e verificação de coordenadas
    """
    resultados = []
    
    # Gerar dados de treinamento simulados
    print("Gerando dados de treinamento simulados...")
    X_train_full, y_train_full = gerar_dados_treinamento(n_amostras=2000, ruido=0.3)
    
    # Dividir em conjuntos de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X_train_full, y_train_full, test_size=0.3, random_state=42
    )
    
    # Gerar coordenadas simuladas para os dados
    print("Gerando coordenadas simuladas...")
    regioes = ['amazonia', 'acre', 'xingu', 'tapajos']
    
    for regiao in regioes:
        print(f"\nProcessando região: {regiao}")
        
        # Gerar coordenadas para esta região
        coords_train = gerar_coordenadas_simuladas(len(X_train), regiao)
        coords_test = gerar_coordenadas_simuladas(len(X_test), regiao)
        
        # Aplicar Método 1: Baseado em características ambientais
        y_pred_1, importancia = metodo_1_ambiental(X_train, y_train, X_test)
        
        # Aplicar Método 2: Baseado em padrões espaciais
        y_pred_2 = metodo_2_espacial(X_train, y_train, X_test, coords_train, coords_test)
        
        # Comparar resultados
        metricas = comparar_metodos(y_test, y_pred_1, y_pred_2)
        
        print(f"Resultados para região {regiao}:")
        print(f"Acurácia Método 1: {metricas['Acurácia Método 1']:.4f}")
        print(f"Acurácia Método 2: {metricas['Acurácia Método 2']:.4f}")
        print(f"Concordância entre métodos: {metricas['Concordância entre métodos']:.4f}")
        print(f"Acurácia quando métodos concordam: {metricas['Acurácia quando concordam']:.4f}")
        
        # Visualizar importância das features (Método 1)
        plt.figure(figsize=(10, 6))
        importancia.plot(kind='barh', x='Feature', y='Importância')
        plt.title(f'Importância das Características - Região: {regiao.title()}')
        plt.tight_layout()
        caminho_importancia = os.path.join(coordenadas_dir, f'importancia_features_{regiao}.png')
        plt.savefig(caminho_importancia, dpi=300)
        plt.close()
        resultados.append(caminho_importancia)
        
        # Visualizar resultados em mapa simplificado
        caminho_mapa = visualizar_mapa_simplificado(
            coords_test, y_test, y_pred_1, y_pred_2, 
            regiao, f'mapa_previsoes_{regiao}.png'
        )
        resultados.append(caminho_mapa)
        
        # Salvar coordenadas de sítios previstos com alta confiança
        sitios_alta_confianca = np.where((y_pred_1 == 1) & (y_pred_2 == 1))[0]
        if len(sitios_alta_confianca) > 0:
            coords_alta_confianca = coords_test[sitios_alta_confianca]
            df_alta_confianca = pd.DataFrame({
                'Latitude': coords_alta_confianca[:, 0],
                'Longitude': coords_alta_confianca[:, 1],
                'Confiança': np.ones(len(sitios_alta_confianca))
            })
            
            caminho_csv = os.path.join(coordenadas_dir, f'sitios_previstos_{regiao}.csv')
            df_alta_confianca.to_csv(caminho_csv, index=False)
            resultados.append(caminho_csv)
    
    return resultados

# Executar demonstração
if __name__ == "__main__":
    print("Iniciando demonstração de previsão e verificação de coordenadas geográficas...")
    resultados = demonstrar_previsao_coordenadas()
    print(f"Demonstração concluída. Resultados salvos em {coordenadas_dir}")
