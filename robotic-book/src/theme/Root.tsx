// import React from 'react';
// import RAGChatWidget from '@site/src/components/RAGChatWidget';

// // This is the top-level React component that wraps the entire Docusaurus site
// // It's used to inject components that should appear on every page
// const Root: React.FC<{ children: React.ReactNode }> = ({ children }) => {
//   return (
//     <>
//       {children}
//       <RAGChatWidget />
//     </>
//   );
// };

// export default Root;

import React from 'react';
import RAGChatWidget from '@site/src/components/RAGChatWidget';

export default function Root({ children }: { children: React.ReactNode }) {
  return (
    <>
    
      {children}
      <RAGChatWidget />
    </>
  );
}
