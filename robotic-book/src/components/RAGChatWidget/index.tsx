// import React, { useState, useEffect, useRef } from 'react';
// import styles from './RAGChatWidget.module.css';

// interface Message {
//   id: string;
//   role: 'user' | 'bot';
//   content: string;
//   timestamp: Date;
//   sources?: string[];
// }

// const RAGChatWidget: React.FC = () => {
//   const [isOpen, setIsOpen] = useState(false);
//   const [messages, setMessages] = useState<Message[]>([]);
//   const [inputValue, setInputValue] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [selectedText, setSelectedText] = useState<string | null>(null);
//   const messagesEndRef = useRef<null | HTMLDivElement>(null);

//   // Load messages from localStorage on component mount
//   useEffect(() => {
//     const savedMessages = localStorage.getItem('ragChatMessages');
//     if (savedMessages) {
//       try {
//         const parsedMessages = JSON.parse(savedMessages);
//         setMessages(parsedMessages.map((msg: any) => ({
//           ...msg,
//           timestamp: new Date(msg.timestamp)
//         })));
//       } catch (e) {
//         console.error('Failed to parse saved messages', e);
//       }
//     }

//     // Set up text selection listener
//     const handleSelection = () => {
//       const selection = window.getSelection();
//       if (selection && selection.toString().trim() !== '') {
//         setSelectedText(selection.toString().trim());
//       } else {
//         setSelectedText(null);
//       }
//     };

//     document.addEventListener('mouseup', handleSelection);
//     return () => {
//       document.removeEventListener('mouseup', handleSelection);
//     };
//   }, []);

//   // Save messages to localStorage whenever they change
//   useEffect(() => {
//     localStorage.setItem('ragChatMessages', JSON.stringify(messages));
//   }, [messages]);

//   // Scroll to bottom of messages when they change
//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
//   }, [messages]);

//   const sendMessage = async () => {
//     if (!inputValue.trim() || isLoading) return;

//     // Add user message to history
//     const userMessage: Message = {
//       id: Date.now().toString(),
//       role: 'user',
//       content: inputValue,
//       timestamp: new Date(),
//     };

//     setMessages(prev => [...prev, userMessage]);
//     setInputValue('');
//     setIsLoading(true);

//     try {
//       // Call the backend API
//       const response = await fetch('http://localhost:8000/query', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           query: inputValue,
//           context: selectedText || undefined, // Send selected text as context if available
//         }),
//       });

//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }

//       const data = await response.json();

//       // Bot response with actual backend data
//       const botMessage: Message = {
//         id: (Date.now() + 1).toString(),
//         role: 'bot',
//         content: data.response,
//         timestamp: new Date(),
//         sources: data.sources || [], // Use actual sources from backend
//       };

//       setMessages(prev => [...prev, botMessage]);
//     } catch (error) {
//       const errorMessage: Message = {
//         id: (Date.now() + 1).toString(),
//         role: 'bot',
//         content: 'Error: Backend offline. Please make sure the FastAPI server is running at http://localhost:8000.',
//         timestamp: new Date(),
//       };
//       setMessages(prev => [...prev, errorMessage]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const sendSelectedTextQuery = async () => {
//     if (!selectedText) return;

//     // Add user message to history
//     const userMessage: Message = {
//       id: Date.now().toString(),
//       role: 'user',
//       content: `About this text: "${selectedText}"`,
//       timestamp: new Date(),
//     };

//     setMessages(prev => [...prev, userMessage]);
//     setIsOpen(true);
//     setIsLoading(true);

//     try {
//       // Call the backend API with selected text as context
//       const response = await fetch('http://localhost:8003/query', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           query: `About this text: "${selectedText}"`,
//           context: selectedText,
//         }),
//       });

//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }

//       const data = await response.json();

//       // Bot response with actual backend data
//       const botMessage: Message = {
//         id: (Date.now() + 1).toString(),
//         role: 'bot',
//         content: data.response,
//         timestamp: new Date(),
//         sources: data.sources || [], // Use actual sources from backend
//       };

//       setMessages(prev => [...prev, botMessage]);
//     } catch (error) {
//       const errorMessage: Message = {
//         id: (Date.now() + 1).toString(),
//         role: 'bot',
//         content: 'Error: Backend offline. Please make sure the FastAPI server is running at http://localhost:8003.',
//         timestamp: new Date(),
//       };
//       setMessages(prev => [...prev, errorMessage]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleKeyPress = (e: React.KeyboardEvent) => {
//     if (e.key === 'Enter' && !e.shiftKey) {
//       e.preventDefault();
//       sendMessage();
//     }
//   };

//   return (
//     <div className={styles.chatContainer}>
//       {/* Selected text indicator */}
//       {selectedText && (
//         <div className={styles.selectedTextIndicator}>
//           <div className="text-sm mb-1">Selected text:</div>
//           <div className={styles.truncateText}>{selectedText}</div>
//           <button
//             onClick={sendSelectedTextQuery}
//             className={styles.askButton}
//           >
//             Ask about this
//           </button>
//         </div>
//       )}

//       {isOpen ? (
//         <div className={styles.chatPanel}>
//           {/* Header */}
//           <div className={styles.chatHeader}>
//             <div className="font-semibold">RAG Chat</div>
//             <button
//               onClick={() => setIsOpen(false)}
//               className={styles.closeButton}
//             >
//               <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
//                 <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
//               </svg>
//             </button>
//           </div>

//           {/* Messages container */}
//           <div className={styles.messagesContainer}>
//             {messages.length === 0 ? (
//               <div className={styles.noMessages}>
//                 No messages yet. Start a conversation!
//               </div>
//             ) : (
//               <div>
//                 {messages.map((message) => (
//                   <div
//                     key={message.id}
//                     className={`${styles.message} ${styles[message.role]}`}
//                   >
//                     <div
//                       className={`${styles.messageContent} ${styles[message.role]}`}
//                     >
//                       <div className="text-sm">{message.content}</div>
//                       {message.sources && message.sources.length > 0 && (
//                         <div className={styles.messageSources}>
//                           <details className={styles.sourcesDetails}>
//                             <summary className={styles.sourcesSummary}>
//                               Sources:
//                             </summary>
//                             <ul className={styles.sourcesList}>
//                               {message.sources.map((source: any, idx: number) => {
//                                 // Handle different possible source formats
//                                 let title = 'Source';
//                                 let url = null;
//                                 let content = null;

//                                 if (typeof source === 'string') {
//                                   // If source is just a string
//                                   title = source.length > 50 ? source.substring(0, 50) + '...' : source;
//                                   content = source;
//                                 } else if (typeof source === 'object' && source !== null) {
//                                   // If source is an object, try to extract meaningful fields
//                                   title = source.title || source.page_title || source.metadata?.title || source.metadata?.source || `Source ${idx + 1}`;
//                                   url = source.url || source.metadata?.url || source.metadata?.source_url || null;
//                                   content = source.content || source.content_snippet || source.text || null;
//                                 } else {
//                                   // Fallback for any other type
//                                   title = `Source ${idx + 1}`;
//                                 }

//                                 return (
//                                   <li key={idx} className={styles.sourceItem}>
//                                     {url ? (
//                                       <a
//                                         href={url}
//                                         target="_blank"
//                                         rel="noopener noreferrer"
//                                         className={styles.sourceLink}
//                                       >
//                                         {title}
//                                       </a>
//                                     ) : (
//                                       <span className={styles.sourceText}>
//                                         {title}
//                                         {content && (
//                                           <div className={styles.sourceContentPreview}>
//                                             {content.length > 100 ? content.substring(0, 100) + '...' : content}
//                                           </div>
//                                         )}
//                                       </span>
//                                     )}
//                                   </li>
//                                 );
//                               })}
//                             </ul>
//                           </details>
//                         </div>
//                       )}
//                     </div>
//                   </div>
//                 ))}
//                 {isLoading && (
//                   <div className={styles.loadingIndicator}>
//                     <div className={styles.loadingContent}>
//                       <div className={styles.loadingDots}>
//                         <div className={styles.loadingDot}></div>
//                         <div className={styles.loadingDot}></div>
//                         <div className={styles.loadingDot}></div>
//                       </div>
//                     </div>
//                   </div>
//                 )}
//                 <div ref={messagesEndRef} />
//               </div>
//             )}
//           </div>

//           {/* Input area */}
//           <div className={styles.inputContainer}>
//             <div className={styles.inputForm}>
//               <textarea
//                 value={inputValue}
//                 onChange={(e) => setInputValue(e.target.value)}
//                 onKeyPress={handleKeyPress}
//                 placeholder="Ask about the book..."
//                 className={styles.chatInput}
//                 disabled={isLoading}
//               />
//               <button
//                 onClick={sendMessage}
//                 disabled={isLoading || !inputValue.trim()}
//                 className={`${styles.sendButton} ${isLoading || !inputValue.trim() ? styles.disabled : styles.enabled}`}
//               >
//                 <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
//                   <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
//                 </svg>
//               </button>
//             </div>
//           </div>
//         </div>
//       ) : null}

//       {/* Chat toggle button */}
//       <button
//         onClick={() => setIsOpen(true)}
//         className={styles.chatToggleButton}
//         aria-label="Open chat"
//       >
//         <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//           <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
//         </svg>
//       </button>
//     </div>
//   );
// };

// export default RAGChatWidget;