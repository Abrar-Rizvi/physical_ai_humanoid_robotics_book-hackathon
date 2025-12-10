// robotic-book/src/theme/Root.js
// T031: Docusaurus Root wrapper to include CourseChatWidget globally

import React from 'react';
import CourseChatWidget from '@site/src/components/CourseChatWidget';

export default function Root({children}) {
  return (
    <>
      {children}
      <CourseChatWidget />
    </>
  );
}
