import React from 'react';

const CodeExample = ({ title, children }) => {
  return (
    <div style={{ border: '1px solid #ccc', borderRadius: '4px', margin: '1em 0' }}>
      <div style={{ background: '#f5f5f5', padding: '0.5em', borderBottom: '1px solid #ccc' }}>
        <strong>{title}</strong>
      </div>
      <div style={{ padding: '0.5em' }}>
        {children}
      </div>
    </div>
  );
};

export default CodeExample;
