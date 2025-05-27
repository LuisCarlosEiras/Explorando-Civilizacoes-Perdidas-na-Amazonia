import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-white py-8">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-semibold mb-4">Amazônia Explorer</h3>
            <p className="text-gray-400">
              Explorando civilizações ocultas sob o dossel da floresta amazônica através de tecnologias avançadas e métodos inovadores.
            </p>
          </div>
          
          <div>
            <h3 className="text-xl font-semibold mb-4">Links Rápidos</h3>
            <ul className="space-y-2">
              <li><a href="#inicio" className="text-gray-400 hover:text-emerald-300 transition-colors">Início</a></li>
              <li><a href="#descobertas" className="text-gray-400 hover:text-emerald-300 transition-colors">Descobertas</a></li>
              <li><a href="#metodologia" className="text-gray-400 hover:text-emerald-300 transition-colors">Metodologia</a></li>
              <li><a href="#mapas" className="text-gray-400 hover:text-emerald-300 transition-colors">Mapas</a></li>
              <li><a href="#sobre" className="text-gray-400 hover:text-emerald-300 transition-colors">Sobre</a></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-xl font-semibold mb-4">Referências</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-400 hover:text-emerald-300 transition-colors">Artigos Científicos</a></li>
              <li><a href="#" className="text-gray-400 hover:text-emerald-300 transition-colors">Fontes de Dados</a></li>
              <li><a href="#" className="text-gray-400 hover:text-emerald-300 transition-colors">Metodologia Completa</a></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-800 mt-8 pt-6 text-center text-gray-500">
          <p>&copy; {new Date().getFullYear()} Amazônia Explorer. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
