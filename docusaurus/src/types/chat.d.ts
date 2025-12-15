// Type definitions for RAG Chatbot interface
// Based on data-model.md specifications

// Represents a user's query sent from the frontend to the backend
export interface ChatQuery {
  query: string;              // The main question or query text (max 2000 chars per constitution compliance)
  context?: string;           // Optional context from selected text (max 5000 chars per constitution compliance)
  session_id?: string;        // Optional session identifier for conversation context
  metadata?: QueryMetadata;   // Additional metadata about the query
}

// Additional information about the query context
export interface QueryMetadata {
  page_url?: string;          // URL of the page where query originated
  selected_text_position?: {  // Position of selected text in document
    start: number;
    end: number;
  };
  timestamp: string;          // ISO timestamp of query submission
  user_agent?: string;        // Information about the user's browser/device
}

// Represents the response received from the backend RAG agent
export interface ChatResponse {
  response: string;           // The AI-generated response text (grounded in book content per constitution)
  sources: SourceReference[]; // List of sources used to generate the response (for attribution per constitution)
  session_id: string;         // Session identifier for conversation context
  confidence?: number;        // Optional confidence score (0-1)
  metadata?: ResponseMetadata;// Additional response metadata
}

// Represents a source document or section used in the response
export interface SourceReference {
  id: string;                 // Unique identifier for the source
  title: string;              // Title or heading of the source
  content: string;            // Snippet of content from the source
  url?: string;               // URL to the source document
  page?: number;              // Page number if applicable
  score?: number;             // Relevance score (0-1)
  metadata?: Record<string, any>; // Additional metadata about the source
}

// Additional information about the response
export interface ResponseMetadata {
  processing_time: number;    // Time taken to process the query (in milliseconds)
  tokens_used: number;        // Number of tokens used in the response
  model: string;              // Name of the model used to generate the response
  timestamp: string;          // ISO timestamp of response generation
}

// Represents the state of a conversation session
export interface ChatSession {
  id: string;                 // Unique session identifier
  created_at: string;         // ISO timestamp of session creation
  last_activity: string;      // ISO timestamp of last activity
  messages: ChatMessage[];    // Array of messages in the conversation
  metadata?: SessionMetadata; // Additional session metadata
}

// Represents a single message in a conversation
export interface ChatMessage {
  id: string;                 // Unique message identifier
  role: 'user' | 'assistant'; // Role of the message sender
  content: string;            // The message content
  timestamp: string;          // ISO timestamp of message creation
  sources?: SourceReference[];// Sources referenced in the message (for assistant responses)
}

// Additional metadata about the session
export interface SessionMetadata {
  page_context?: string;      // Context of the page where session started
  user_preferences?: UserPreferences; // User preferences for this session
}

// User preferences for the chat experience
export interface UserPreferences {
  response_length?: 'short' | 'medium' | 'long'; // Preferred response length
  citation_style?: 'formal' | 'casual' | 'minimal'; // Preferred citation style
  enable_typing_indicator?: boolean; // Whether to show typing indicators
}

// Represents the current state of the chat interface
export interface ChatState {
  messages: ChatMessage[];    // Current messages in the conversation
  isLoading: boolean;         // Whether a response is being generated
  error: string | null;       // Any error message to display
  session: ChatSession | null;// Current session information
  preferences: UserPreferences; // Current user preferences
}

// Configuration options for the chat interface
export interface UIConfiguration {
  position: 'bottom-right';   // Fixed position per constitution requirement (20px offset)
  title: string;              // Title displayed in the chat interface
  initial_open: boolean;      // Whether the chat should be open by default (false per constitution)
  theme: 'light' | 'dark';    // Theme using CSS variables for automatic light/dark mode
  max_height: number;         // Maximum height of the chat interface
  max_width: number;          // Maximum width: 400px desktop, full-width-20px mobile per constitution
}