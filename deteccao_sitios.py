import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
import rasterio
from rasterio.plot import show
from skimage import exposure, feature, filters, morphology, segmentation
from scipy import ndimage

# Configuração do diretório de trabalho
base_dir = '/home/ubuntu/amazonia-explorador'
dados_dir = os.path.join(base_dir, 'dados')
resultados_dir = os.path.join(base_dir, 'resultados')

# Criar diretório de resultados se não existir
if not os.path.exists(resultados_dir):
    os.makedirs(resultados_dir)

# Função para simular dados LIDAR para demonstração
def gerar_dados_simulados(tipo='geoglifo', ruido=0.1):
    """
    Gera dados simulados para demonstrar a metodologia de detecção
    
    Parâmetros:
    tipo: 'geoglifo', 'aldeia_circular', 'vala_circular'
    ruido: nível de ruído para simular vegetação e irregularidades
    """
    tamanho = 500
    dados = np.random.normal(0, ruido, (tamanho, tamanho))
    
    # Adicionar estrutura arqueológica simulada
    x, y = np.ogrid[:tamanho, :tamanho]
    centro = tamanho // 2
    
    if tipo == 'geoglifo':
        # Criar um quadrado
        mascara_quadrado = (abs(x - centro) < 100) & (abs(y - centro) < 100)
        dados[mascara_quadrado] -= 0.5
        
        # Criar um círculo dentro do quadrado
        mascara_circulo = (x - centro)**2 + (y - centro)**2 < 50**2
        dados[mascara_circulo] -= 0.3
        
    elif tipo == 'aldeia_circular':
        # Criar um anel circular (aldeia)
        raio_externo = 100
        raio_interno = 80
        mascara_anel = ((x - centro)**2 + (y - centro)**2 < raio_externo**2) & \
                       ((x - centro)**2 + (y - centro)**2 > raio_interno**2)
        dados[mascara_anel] -= 0.5
        
        # Adicionar montículos ao redor do anel
        for angulo in range(0, 360, 30):
            rad = np.radians(angulo)
            pos_x = int(centro + raio_externo * 0.9 * np.cos(rad))
            pos_y = int(centro + raio_externo * 0.9 * np.sin(rad))
            
            mascara_monticulo = (x - pos_x)**2 + (y - pos_y)**2 < 10**2
            dados[mascara_monticulo] -= 0.8
            
        # Adicionar estradas radiais
        for angulo in range(0, 360, 45):
            rad = np.radians(angulo)
            for r in range(raio_externo, raio_externo + 100):
                pos_x = int(centro + r * np.cos(rad))
                pos_y = int(centro + r * np.sin(rad))
                
                if 0 <= pos_x < tamanho and 0 <= pos_y < tamanho:
                    for dx in range(-2, 3):
                        for dy in range(-2, 3):
                            nx, ny = pos_x + dx, pos_y + dy
                            if 0 <= nx < tamanho and 0 <= ny < tamanho:
                                dados[nx, ny] -= 0.3
    
    elif tipo == 'vala_circular':
        # Criar uma vala circular
        raio = 100
        largura = 10
        mascara_vala = ((x - centro)**2 + (y - centro)**2 < (raio + largura/2)**2) & \
                       ((x - centro)**2 + (y - centro)**2 > (raio - largura/2)**2)
        dados[mascara_vala] -= 0.7
        
        # Adicionar entrada/abertura na vala
        angulo_entrada = np.radians(45)
        for r in range(int(raio - largura/2), int(raio + largura/2) + 1):
            for a in range(-10, 11):
                rad = angulo_entrada + np.radians(a)
                pos_x = int(centro + r * np.cos(rad))
                pos_y = int(centro + r * np.sin(rad))
                
                if 0 <= pos_x < tamanho and 0 <= pos_y < tamanho:
                    dados[pos_x, pos_y] += 0.7  # Remover a vala neste ponto
    
    # Adicionar mais ruído para simular vegetação
    vegetacao = np.random.normal(0, ruido * 2, (tamanho, tamanho))
    vegetacao = ndimage.gaussian_filter(vegetacao, sigma=3)
    
    # Combinar dados e vegetação
    dados_finais = dados + vegetacao
    
    return dados_finais

# Função para aplicar técnicas de realce e detecção
def processar_dados(dados, metodo='realce'):
    """
    Processa os dados para realçar estruturas arqueológicas
    
    Parâmetros:
    dados: array 2D com os dados de elevação
    metodo: 'realce', 'bordas', 'segmentacao'
    """
    if metodo == 'realce':
        # Equalização de histograma para melhorar contraste
        dados_processados = exposure.equalize_hist(dados)
        
    elif metodo == 'bordas':
        # Detecção de bordas usando filtro Sobel
        dados_processados = filters.sobel(dados)
        
    elif metodo == 'segmentacao':
        # Segmentação usando watershed
        gradiente = filters.sobel(dados)
        marcadores = np.zeros_like(dados, dtype=int)
        marcadores[dados < dados.mean() - 0.2] = 1
        marcadores[dados > dados.mean() + 0.2] = 2
        dados_processados = segmentation.watershed(gradiente, marcadores)
        
    return dados_processados

# Função para visualizar os resultados
def visualizar_dados(dados, titulo, filename, colormap='terrain', sombreamento=True):
    """
    Visualiza e salva os dados processados
    
    Parâmetros:
    dados: array 2D com os dados
    titulo: título do gráfico
    filename: nome do arquivo para salvar
    colormap: mapa de cores para visualização
    sombreamento: aplicar sombreamento para realçar relevo
    """
    plt.figure(figsize=(12, 10))
    
    if sombreamento:
        # Aplicar sombreamento para realçar relevo
        ls = LightSource(azdeg=315, altdeg=45)
        dados_sombreados = ls.shade(dados, cmap=plt.cm.get_cmap(colormap), 
                                   vert_exag=10, blend_mode='soft')
        plt.imshow(dados_sombreados)
    else:
        plt.imshow(dados, cmap=colormap)
    
    plt.title(titulo, fontsize=16)
    plt.colorbar(label='Elevação relativa')
    plt.axis('off')
    
    # Salvar figura
    caminho_completo = os.path.join(resultados_dir, filename)
    plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho_completo

# Função principal para demonstrar o fluxo de trabalho
def demonstrar_fluxo_trabalho():
    """
    Demonstra o fluxo de trabalho completo para detecção de sítios arqueológicos
    """
    resultados = []
    
    # Processar diferentes tipos de estruturas
    for tipo in ['geoglifo', 'aldeia_circular', 'vala_circular']:
        print(f"Processando simulação de {tipo}...")
        
        # Gerar dados simulados
        dados_originais = gerar_dados_simulados(tipo=tipo, ruido=0.1)
        
        # Salvar dados originais
        caminho_original = visualizar_dados(
            dados_originais, 
            f"Dados LIDAR Simulados - {tipo.replace('_', ' ').title()}", 
            f"original_{tipo}.png"
        )
        resultados.append(caminho_original)
        
        # Aplicar diferentes métodos de processamento
        for metodo in ['realce', 'bordas', 'segmentacao']:
            dados_processados = processar_dados(dados_originais, metodo=metodo)
            
            # Visualizar e salvar resultados
            caminho_processado = visualizar_dados(
                dados_processados, 
                f"{tipo.replace('_', ' ').title()} - Método: {metodo.title()}", 
                f"{tipo}_{metodo}.png",
                colormap='viridis' if metodo == 'segmentacao' else 'terrain',
                sombreamento=metodo != 'segmentacao'
            )
            resultados.append(caminho_processado)
    
    return resultados

# Executar demonstração
if __name__ == "__main__":
    print("Iniciando demonstração de detecção de sítios arqueológicos...")
    caminhos_resultados = demonstrar_fluxo_trabalho()
    print(f"Demonstração concluída. {len(caminhos_resultados)} imagens geradas em {resultados_dir}")
