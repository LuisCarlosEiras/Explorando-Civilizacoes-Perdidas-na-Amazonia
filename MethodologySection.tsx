import React from 'react';

interface MethodologySectionProps {
  title: string;
  steps: {
    number: number;
    title: string;
    description: string;
    icon?: string;
  }[];
}

const MethodologySection: React.FC<MethodologySectionProps> = ({ title, steps }) => {
  return (
    <section id="metodologia" className="py-16 bg-emerald-50">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold mb-8 text-center text-emerald-800">{title}</h2>
        
        <div className="max-w-4xl mx-auto">
          {steps.map((step, index) => (
            <div key={index} className="flex mb-8">
              <div className="mr-6">
                <div className="flex items-center justify-center w-12 h-12 rounded-full bg-emerald-600 text-white font-bold text-xl">
                  {step.number}
                </div>
                {index < steps.length - 1 && (
                  <div className="h-full w-0.5 bg-emerald-300 mx-auto mt-2"></div>
                )}
              </div>
              <div className="bg-white rounded-lg shadow-md p-6 flex-1">
                <h3 className="text-xl font-bold mb-2 text-emerald-700">{step.title}</h3>
                <p className="text-gray-700">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default MethodologySection;
