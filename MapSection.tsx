import React from 'react';

interface MapSectionProps {
  maps: {
    src: string;
    alt: string;
    title: string;
    description: string;
  }[];
}

const MapSection: React.FC<MapSectionProps> = ({ maps }) => {
  return (
    <section id="mapas" className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold mb-8 text-center text-emerald-800">Mapas e Visualizações</h2>
        <p className="text-lg text-gray-700 max-w-4xl mx-auto mb-12 text-center">
          Explore os mapas e visualizações geradas a partir de nossa análise de dados, mostrando potenciais sítios arqueológicos e padrões de assentamento na Amazônia.
        </p>
        
        <div className="space-y-16">
          {maps.map((map, index) => (
            <div 
              key={index} 
              className={`flex flex-col ${index % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'} gap-8 items-center`}
            >
              <div className="w-full md:w-1/2">
                <img 
                  src={map.src} 
                  alt={map.alt} 
                  className="w-full h-auto rounded-lg shadow-lg"
                />
              </div>
              <div className="w-full md:w-1/2">
                <h3 className="text-2xl font-bold mb-4 text-emerald-700">{map.title}</h3>
                <p className="text-gray-700">{map.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default MapSection;
