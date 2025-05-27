import { useEffect, useState } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import Hero from './components/Hero';
import ArticleSection from './components/ArticleSection';
import ImageGallery from './components/ImageGallery';
import MapSection from './components/MapSection';
import MethodologySection from './components/MethodologySection';

function App() {
  const [articleContent, setArticleContent] = useState('');

  useEffect(() => {
    // Carregar conteúdo do artigo
    fetch('/data/artigo_final.md')
      .then(response => response.text())
      .then(text => {
        setArticleContent(text);
      })
      .catch(error => console.error('Erro ao carregar artigo:', error));
  }, []);

  // Dados para a galeria de imagens
  const discoveryImages = [
    {
      src: '/original_geoglifo.png',
      alt: 'Geoglifo Original',
      caption: 'Imagem original de geoglifo identificado na região amazônica'
    },
    {
      src: '/geoglifo_bordas.png',
      alt: 'Geoglifo com Detecção de Bordas',
      caption: 'Aplicação de algoritmo de detecção de bordas para realçar estruturas'
    },
    {
      src: '/original_aldeia_circular.png',
      alt: 'Aldeia Circular Original',
      caption: 'Imagem original de aldeia circular identificada na região do Xingu'
    },
    {
      src: '/aldeia_circular_bordas.png',
      alt: 'Aldeia Circular com Detecção de Bordas',
      caption: 'Aplicação de algoritmo de detecção de bordas para realçar estruturas'
    },
    {
      src: '/original_vala_circular.png',
      alt: 'Vala Circular Original',
      caption: 'Imagem original de vala circular defensiva identificada'
    },
    {
      src: '/vala_circular_bordas.png',
      alt: 'Vala Circular com Detecção de Bordas',
      caption: 'Aplicação de algoritmo de detecção de bordas para realçar estruturas'
    }
  ];

  // Dados para a seção de mapas
  const mapData = [
    {
      src: '/coordenadas/mapa_previsoes_amazonia.png',
      alt: 'Mapa de Previsões - Amazônia',
      title: 'Mapa de Previsões para a Região Amazônica',
      description: 'Este mapa mostra os resultados da aplicação de dois métodos independentes para previsão de coordenadas geográficas de potenciais sítios arqueológicos na região amazônica. Os pontos verdes representam sítios reais, os azuis são previsões corretas de ambos os métodos, e os vermelhos são previsões incorretas.'
    },
    {
      src: '/coordenadas/mapa_previsoes_xingu.png',
      alt: 'Mapa de Previsões - Xingu',
      title: 'Mapa de Previsões para a Região do Xingu',
      description: 'Análise detalhada da região do Xingu, onde foram identificados padrões de aldeias circulares interconectadas, possivelmente relacionadas à lendária "Cidade Perdida de Z" e ao complexo de Kuhikugu.'
    },
    {
      src: '/coordenadas/importancia_features_amazonia.png',
      alt: 'Importância das Características - Amazônia',
      title: 'Importância das Características Ambientais',
      description: 'Este gráfico mostra a importância relativa de diferentes características ambientais e topográficas para a previsão de sítios arqueológicos. A proximidade a rios e a elevação moderada são os fatores mais determinantes.'
    }
  ];

  // Dados para a seção de metodologia
  const methodologySteps = [
    {
      number: 1,
      title: 'Aquisição e Integração de Dados Multimodais',
      description: 'Coleta e integração de dados de múltiplas fontes, incluindo imagens de satélite, LIDAR, modelos digitais de elevação, dados históricos e conhecimento indígena.'
    },
    {
      number: 2,
      title: 'Pré-processamento e Realce Adaptativo',
      description: 'Aplicação de técnicas de pré-processamento e realce para maximizar a detecção de estruturas arqueológicas, incluindo correção atmosférica, filtragem adaptativa e realce de contraste.'
    },
    {
      number: 3,
      title: 'Detecção Multicamada com Validação Cruzada',
      description: 'Implementação de uma abordagem de detecção em três camadas complementares, com validação cruzada para aumentar a confiabilidade das previsões.'
    },
    {
      number: 4,
      title: 'Contextualização Histórico-Cultural',
      description: 'Integração de conhecimento arqueológico e indígena para contextualizar as descobertas, incluindo análise de redes culturais e padrões de assentamento.'
    },
    {
      number: 5,
      title: 'Priorização e Verificação Colaborativa',
      description: 'Sistema de priorização para identificação de sítios para verificação em campo, com plataforma colaborativa para contribuições distribuídas e ciclo de feedback.'
    }
  ];

  // Extrair o resumo do artigo (primeiros parágrafos)
  const getArticleSummary = () => {
    if (!articleContent) return '';
    const paragraphs = articleContent.split('\n\n');
    // Pegar os parágrafos após o título principal, até o próximo título
    let summary = '';
    let foundFirstTitle = false;
    
    for (let i = 0; i < paragraphs.length; i++) {
      if (paragraphs[i].startsWith('# ')) {
        foundFirstTitle = true;
        continue;
      }
      
      if (foundFirstTitle && !paragraphs[i].startsWith('#')) {
        summary += paragraphs[i] + '\n\n';
      }
      
      if (foundFirstTitle && paragraphs[i].startsWith('## ')) {
        break;
      }
    }
    
    return summary;
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-grow">
        <Hero />
        
        <section id="descobertas" className="py-16">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-8 text-center text-emerald-800">Descobertas Principais</h2>
            
            <div className="mb-12">
              <ArticleSection 
                title="Explorando a Amazônia Digital" 
                content={getArticleSummary()} 
              />
              
              <div className="text-center mt-8">
                <a 
                  href="#artigo-completo" 
                  className="inline-block bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 px-6 rounded-lg transition-colors"
                >
                  Ler Artigo Completo
                </a>
              </div>
            </div>
            
            <ImageGallery 
              title="Visualizações de Estruturas Arqueológicas" 
              images={discoveryImages} 
            />
          </div>
        </section>
        
        <MapSection maps={mapData} />
        
        <MethodologySection 
          title="Metodologia Inovadora" 
          steps={methodologySteps} 
        />
        
        <section id="artigo-completo" className="py-16 bg-white">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-8 text-center text-emerald-800">Artigo Completo</h2>
            
            <div className="bg-white rounded-lg shadow-lg p-8">
              <ArticleSection 
                title="" 
                content={articleContent} 
              />
            </div>
          </div>
        </section>
        
        <section id="sobre" className="py-16 bg-gray-50">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-8 text-center text-emerald-800">Sobre o Projeto</h2>
            
            <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
              <p className="text-lg mb-6">
                Este projeto de exploração digital da Amazônia utiliza tecnologias avançadas como imagens de satélite, LIDAR e inteligência artificial para identificar e analisar potenciais sítios arqueológicos ocultos sob o dossel da floresta.
              </p>
              
              <p className="text-lg mb-6">
                Através da integração de múltiplas fontes de dados, desenvolvimento de metodologias inovadoras de detecção e validação cruzada, o estudo revela novos insights sobre as antigas civilizações amazônicas e propõe uma abordagem revolucionária para a descoberta arqueológica em grande escala.
              </p>
              
              <p className="text-lg">
                Os resultados sugerem uma Amazônia pré-colombiana muito mais densamente povoada e culturalmente complexa do que se acreditava anteriormente, com evidências que conectam lendas como a "Cidade Perdida de Z", Paititi e El Dorado a padrões reais de assentamentos antigos.
              </p>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
}

export default App;
