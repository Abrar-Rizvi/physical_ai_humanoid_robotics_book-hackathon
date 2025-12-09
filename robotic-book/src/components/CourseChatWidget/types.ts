// robotic-book/src/components/CourseChatWidget/types.ts

export type MessageSender = 'user' | 'bot';
export type MessageStatus = 'pending' | 'sent' | 'error';
export type ErrorType = 'network' | 'api' | 'rate_limit' | 'unknown';

export interface Message {
  id: string;
  text: string;
  sender: MessageSender;
  timestamp: number;
  status?: MessageStatus;
}

export interface ChatSession {
  sessionId: string;
  messages: Message[];
  startedAt: number;
  lastActivityAt: number;
}

export interface PageContext {
  title: string;
  pathname: string;
  section?: string;
}

export interface ChatRequest {
  user_query: string;
  page_context: PageContext;
  session_id?: string;
}

export interface Source {
  title: string;
  url: string;
}

export interface ResponseMetadata {
  processing_time_ms?: number;
  model_used?: string;
  tokens_used?: number;
}

export interface ChatResponse {
  response_text: string;
  sources?: Source[];
  metadata?: ResponseMetadata;
}

export interface ErrorState {
  hasError: boolean;
  errorType?: ErrorType;
  errorMessage?: string;
  retryable?: boolean;
}

export interface WidgetState {
  isOpen: boolean;
  messages: Message[];
  inputValue: string;
  isLoading: boolean;
  errorMessage: string | null;
}
