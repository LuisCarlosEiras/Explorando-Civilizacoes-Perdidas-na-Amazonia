import React from 'react';
import { ArrowDown } from 'lucide-react';

const Hero: React.FC = () => {
  return (
    <section 
      id="inicio" 
      className="relative h-screen flex items-center justify-center bg-cover bg-center text-white"
      style={{ 
        backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7)), url('/hero-background.jpg')` 
      }}
    >
      <div className="container mx-auto px-4 text-center">
        <h1 className="text-4xl md:text-6xl font-bold mb-6">
          Explorando a Amazônia Digital
        </h1>
        <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
          Descobrindo civilizações ocultas sob o dossel da floresta através de tecnologias avançadas e métodos inovadores
        </p>
        <a 
          href="#descobertas" 
          className="inline-block bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 px-8 rounded-lg transition-colors"
        >
          Explorar Descobertas
        </a>
      </div>
      
      <div className="absolute bottom-10 left-0 right-0 flex justify-center animate-bounce">
        <a href="#descobertas" className="text-white">
          <ArrowDown size={32} />
        </a>
      </div>
    </section>
  );
};

export default Hero;
