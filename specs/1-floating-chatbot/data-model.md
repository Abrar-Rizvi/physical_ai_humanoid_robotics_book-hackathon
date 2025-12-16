# Data Model: Floating Chatbot UI Component

**Feature**: Floating Chatbot UI Component
**Date**: 2025-12-17

## Entity: ChatMessage

### Description
Represents a single message in the chat conversation between user and assistant.

### Fields
- `id` (string, required): Unique identifier for the message
- `content` (string, required): The text content of the message
- `sender` (enum, required): The sender of the message - "user" or "assistant"
- `timestamp` (Date, required): When the message was sent
- `status` (enum, optional): Message delivery status - "sent", "delivered", "read" (default: "sent")
- `type` (enum, optional): Message type - "text", "command", "system" (default: "text")

### Validation Rules
- `id` must be a unique string
- `content` must be 1-2000 characters
- `sender` must be one of the allowed values
- `timestamp` must be a valid date
- `status` must be one of the allowed values if provided

## Entity: ChatSession

### Description
Represents an active chat session with state and message history.

### Fields
- `id` (string, required): Unique identifier for the session
- `isOpen` (boolean, required): Whether the chat window is currently open
- `messages` (array of ChatMessage, required): Collection of messages in the session
- `lastActive` (Date, required): Time of last interaction
- `isOnline` (boolean, required): Status of the AI service
- `createdAt` (Date, required): When the session was created

### Validation Rules
- `id` must be a unique string
- `messages` array must contain 0-500 messages
- `lastActive` must be a valid date
- `createdAt` must be a valid date
- `createdAt` must be before or equal to `lastActive`

## Entity: ChatConfig

### Description
Configuration settings for the chatbot UI component.

### Fields
- `title` (string, required): The header title text (default: "AI Partner")
- `subtitle` (string, required): The subtitle text (default: "Online • Powered by RAG")
- `primaryColor` (string, required): Primary color in hex format (default: "#2563eb")
- `iconType` (string, optional): Type of chat icon to use (default: "message")
- `animationDuration` (number, optional): Animation duration in ms (default: 300)
- `maxMessageLength` (number, optional): Maximum allowed message length (default: 2000)

### Validation Rules
- `title` must be 1-100 characters
- `subtitle` must be 1-200 characters
- `primaryColor` must be a valid hex color format
- `animationDuration` must be between 100-1000 ms
- `maxMessageLength` must be between 100-10000 characters

## State Transitions

### Chat Window State
- `closed` → `opening`: When user clicks floating button
- `opening` → `open`: After animation completes
- `open` → `closing`: When user clicks close button or outside area
- `closing` → `closed`: After animation completes

### Message Status Transitions
- `sent` → `delivered`: When message reaches server
- `delivered` → `read`: When assistant processes the message (if applicable)

## Relationships
- One ChatSession contains many ChatMessage objects
- ChatSession may have one ChatConfig (optional, for customization)