import React from 'react';

interface ImageGalleryProps {
  images: {
    src: string;
    alt: string;
    caption?: string;
  }[];
  title: string;
}

const ImageGallery: React.FC<ImageGalleryProps> = ({ images, title }) => {
  return (
    <div className="py-8">
      <h2 className="text-2xl font-bold mb-6 text-center">{title}</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {images.map((image, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
            <img 
              src={image.src} 
              alt={image.alt} 
              className="w-full h-64 object-cover hover:scale-105 transition-transform duration-300"
            />
            {image.caption && (
              <div className="p-4 bg-gray-50">
                <p className="text-gray-700 text-sm">{image.caption}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ImageGallery;
