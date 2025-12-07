import React from 'react';

const Citation = ({ source }) => {
  return (
    <span style={{ fontStyle: 'italic', color: 'gray' }}>
      ({source})
    </span>
  );
};

export default Citation;
