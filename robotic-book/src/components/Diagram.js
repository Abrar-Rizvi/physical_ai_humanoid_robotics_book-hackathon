import React from 'react';

const Diagram = ({ src, caption }) => {
  return (
    <figure style={{ textAlign: 'center', margin: '2em 0' }}>
      <img src={src} alt={caption} style={{ maxWidth: '100%', border: '1px solid #ccc' }} />
      <figcaption style={{ fontStyle: 'italic', marginTop: '0.5em', color: 'gray' }}>
        {caption}
      </figcaption>
    </figure>
  );
};

export default Diagram;
