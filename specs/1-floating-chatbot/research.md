# Research Document: Floating Chatbot UI Implementation

**Feature**: Floating Chatbot UI Component
**Date**: 2025-12-17

## Decision: Color Palette
- **Primary Blue**: Using #2563eb as specified in requirements
- **Alternative**: If needed, similar modern blues like #3b82f6 or #1d4ed8
- **Rationale**: Matches specification requirement and is a standard modern blue

## Decision: Animation Approach
- **Primary**: CSS transitions and transforms for performance
- **Alternative**: Framer Motion for more complex animations if needed
- **Rationale**: CSS-based animations have better performance characteristics

## Decision: Icon Library
- **Primary**: Lucide React or Heroicons for consistency with modern UI
- **Rationale**: Clean, line-style icons that match the requirement for "white stroke/line style"

## Decision: State Management
- **Primary**: React hooks for component state
- **Rationale**: Lightweight solution appropriate for UI component state

## Decision: RAG Integration Backend
- **Primary**: The floating chatbot will need to connect to an existing RAG backend service
- **Rationale**: The specification mentions "Powered by RAG" which implies an existing backend service
- **Implementation**: Component will use fetch or axios to communicate with backend API

## Decision: Message Persistence
- **Primary**: Session-based storage (in-memory React state)
- **Alternative**: Local storage for persistent conversations
- **Rationale**: For a floating chat widget, session-based storage is appropriate unless specified otherwise

## Decision: Animation Duration
- **Primary**: 300ms for open/close transitions (matches success criteria SC-004)
- **Easing**: Ease-in-out for smooth animations
- **Rationale**: Standard duration that provides good UX without being too slow