# Metodologia para Identificação de Sítios Arqueológicos Ocultos na Amazônia

## 1. Introdução

Este documento descreve a metodologia que será utilizada para identificar potenciais sítios arqueológicos ocultos sob a cobertura florestal da Amazônia. A abordagem combina técnicas de sensoriamento remoto, análise de dados LIDAR, processamento de imagens de satélite e integração com conhecimentos arqueológicos existentes.

## 2. Características de Sítios Arqueológicos na Amazônia

Com base na literatura científica analisada, os principais tipos de estruturas arqueológicas a serem identificados incluem:

### 2.1. Geoglifos
- Estruturas geométricas (círculos, quadrados, hexágonos)
- Valas e montículos formando padrões regulares
- Dimensões típicas: 100-300m de diâmetro
- Localizados principalmente em áreas de terra firme

### 2.2. Aldeias Circulares com Montículos
- Padrão circular ou semicircular
- Montículos dispostos em formato de anel
- Estradas radiais partindo do centro
- Dimensões típicas: 100-200m de diâmetro

### 2.3. Valas Circulares (Ring Ditches)
- Estruturas defensivas em formato circular
- Frequentemente associadas a ilhas florestais em áreas de savana
- Podem estar conectadas a sistemas de canais e estruturas de manejo de água

### 2.4. Assentamentos Fortificados
- Grandes áreas habitacionais cercadas por valas
- Sistemas de estradas conectando diferentes assentamentos
- Evidências de planejamento espacial complexo

## 3. Indicadores de Presença Arqueológica

### 3.1. Indicadores Diretos
- Anomalias geométricas na topografia
- Padrões regulares não naturais
- Estruturas lineares ou circulares
- Montículos e elevações artificiais

### 3.2. Indicadores Indiretos
- Diferenças na composição da vegetação (Terra Preta de Índio)
- Variações na resposta espectral do solo
- Padrões de drenagem modificados
- Concentração de espécies vegetais indicadoras (palmeiras, árvores frutíferas)

## 4. Fontes de Dados

### 4.1. Dados LIDAR
- Penetração do dossel florestal
- Detecção de micro-relevo e estruturas sutis
- Geração de Modelos Digitais de Terreno (MDT)

### 4.2. Imagens de Satélite
- Sentinel-2: resolução de 10m, 13 bandas (bom para cicatrizes de vegetação)
- Landsat: cobertura histórica desde 1972
- Imagens de alta resolução quando disponíveis

### 4.3. Dados Arqueológicos Existentes
- Sítios já documentados como referência
- Padrões conhecidos de assentamento
- Contexto histórico e cultural

## 5. Processamento de Dados

### 5.1. Pré-processamento
- Correção atmosférica de imagens de satélite
- Filtragem de dados LIDAR para remoção de vegetação
- Geração de MDT e Modelos de Superfície

### 5.2. Técnicas de Realce
- Análise de componentes principais
- Índices de vegetação (NDVI, EVI)
- Filtros de detecção de bordas
- Realce de contraste local

### 5.3. Detecção de Anomalias
- Algoritmos de detecção de formas geométricas
- Análise de textura e padrões
- Detecção de anomalias topográficas
- Identificação de padrões regulares

## 6. Abordagem Metodológica

### 6.1. Fase 1: Análise Regional
- Identificação de áreas prioritárias com base em modelos preditivos
- Foco em regiões com características ambientais favoráveis à ocupação humana
- Análise de grandes áreas usando dados de média resolução

### 6.2. Fase 2: Análise Local
- Exame detalhado de áreas prioritárias
- Aplicação de técnicas de realce e detecção
- Identificação de potenciais estruturas arqueológicas

### 6.3. Fase 3: Validação
- Comparação com sítios conhecidos
- Análise cruzada usando diferentes fontes de dados
- Avaliação de especialistas

## 7. Implementação

### 7.1. Ferramentas Computacionais
- Processamento de imagens: Python com bibliotecas GDAL, Rasterio, OpenCV
- Análise espacial: QGIS, ArcGIS
- Aprendizado de máquina: Scikit-learn, TensorFlow

### 7.2. Fluxo de Trabalho
1. Aquisição e organização de dados
2. Pré-processamento e preparação
3. Aplicação de algoritmos de detecção
4. Análise visual e interpretação
5. Documentação e validação

## 8. Documentação e Registro

Para cada potencial sítio identificado, serão registrados:
- Coordenadas geográficas
- Tipo de estrutura
- Dimensões e características
- Método de detecção
- Nível de confiança
- Contexto ambiental e geográfico

## 9. Limitações e Desafios

- Cobertura florestal densa limitando a visibilidade
- Disponibilidade limitada de dados LIDAR de alta resolução
- Erosão e degradação de estruturas antigas
- Similaridade entre padrões naturais e antrópicos

## 10. Referências Metodológicas

1. Wagner, F.H. et al. (2022) "Fast computation of digital terrain model anomalies based on LiDAR data for geoglyph detection in the Amazon."
2. Iriarte, J. et al. (2020) "Geometry by Design: Contribution of Lidar to the Understanding of Settlement Patterns of the Mound Villages in SW Amazonia."
3. Walker, R.S. et al. (2023) "Predicting the geographic distribution of ancient Amazonian archaeological sites with machine learning."
