// Session management utility for maintaining conversation context
// Implements session management functionality per task T009

// Generate a unique session ID
const generateSessionId = () => {
  return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
};

// Session management class
class SessionManager {
  constructor() {
    this.currentSession = null;
    this.storageKey = 'rag_chat_sessions';
  }

  // Create a new session
  createSession(initialData = {}) {
    const sessionId = generateSessionId();
    const session = {
      id: sessionId,
      created_at: new Date().toISOString(),
      last_activity: new Date().toISOString(),
      messages: [],
      metadata: {
        ...initialData,
        page_context: window.location.href,
        user_agent: navigator.userAgent
      }
    };

    this.currentSession = session;
    this.saveSession(session);
    return session;
  }

  // Get the current session
  getCurrentSession() {
    if (!this.currentSession) {
      // Try to load from storage
      this.currentSession = this.loadCurrentSession();
    }
    return this.currentSession;
  }

  // Load session from storage
  loadCurrentSession() {
    const sessions = this.getAllSessions();
    // Get the most recent active session or create a new one
    if (sessions && sessions.length > 0) {
      // Find the most recent session (or implement your own logic for session selection)
      return sessions[0]; // For now, return the first session
    }
    return null;
  }

  // Save session to storage
  saveSession(session) {
    if (!session) return;

    const sessions = this.getAllSessions();
    const existingIndex = sessions.findIndex(s => s.id === session.id);

    if (existingIndex >= 0) {
      // Update existing session
      sessions[existingIndex] = { ...session, last_activity: new Date().toISOString() };
    } else {
      // Add new session
      sessions.unshift({ ...session, last_activity: new Date().toISOString() });
    }

    // Limit stored sessions to prevent storage bloat
    const maxSessions = 10;
    if (sessions.length > maxSessions) {
      sessions.splice(maxSessions);
    }

    try {
      localStorage.setItem(this.storageKey, JSON.stringify(sessions));
    } catch (error) {
      console.warn('Failed to save session to localStorage:', error);
    }
  }

  // Get all sessions from storage
  getAllSessions() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.warn('Failed to load sessions from localStorage:', error);
      return [];
    }
  }

  // Add a message to the current session
  addMessageToSession(message) {
    const session = this.getCurrentSession() || this.createSession();
    session.messages.push({
      ...message,
      timestamp: new Date().toISOString()
    });
    session.last_activity = new Date().toISOString();
    this.currentSession = session;
    this.saveSession(session);
    return session;
  }

  // Clear the current session
  clearCurrentSession() {
    this.currentSession = null;
    try {
      localStorage.removeItem(this.storageKey);
    } catch (error) {
      console.warn('Failed to clear sessions from localStorage:', error);
    }
  }

  // Update session metadata
  updateSessionMetadata(metadata) {
    const session = this.getCurrentSession();
    if (session) {
      session.metadata = { ...session.metadata, ...metadata };
      session.last_activity = new Date().toISOString();
      this.currentSession = session;
      this.saveSession(session);
    }
  }
}

// Create a singleton instance
const sessionManager = new SessionManager();

// Export functions for direct use
export const createNewSession = (initialData = {}) => sessionManager.createSession(initialData);
export const getCurrentSession = () => sessionManager.getCurrentSession();
export const addMessageToCurrentSession = (message) => sessionManager.addMessageToSession(message);
export const clearCurrentSession = () => sessionManager.clearCurrentSession();
export const updateSessionMetadata = (metadata) => sessionManager.updateSessionMetadata(metadata);
export const getAllSessions = () => sessionManager.getAllSessions();

// Export the manager instance if needed
export default sessionManager;