---
id: 1
title: floating-chatbot-ui-specification
stage: spec
date: '2025-12-17'
surface: agent
model: Claude Sonnet 4.5
feature: floating-chatbot
branch: 1-floating-chatbot
user: Claude Code User
command: /sp.specify
labels:
  - ui-component
  - chatbot
  - floating
  - specification
links:
  spec: specs/1-floating-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-floating-chatbot/spec.md
  - specs/1-floating-chatbot/checklists/requirements.md
tests: []
---

# Prompt

```
Create a floating chatbot UI component that visually matches with the following exact behavior and styling requirements.

Closed State (Chatbot Button):
- Shape: Rounded square / circular floating button
- Background color: Blue (#2563eb or similar modern blue)
- Icon: Chat/message icon in white stroke/line style
- Border: White outline around the button
- Position: Bottom-right corner (floating)
- Hover: Slight scale or shadow for interactivity

Open State (Chatbot Window):
- Layout must match with the following requirments:

Header Section:
- Title text: "AI Companion"
- Subtitle text: "Online • Powered by RAG"
- Online indicator:
  - Small green dot before the word "Online"
- Text color: White
- Header background: Blue (same blue as button)
- Close button (X) on the top-right

Chat Body:
- Assistant messages:
  - White background
  - Rounded corners
  - Clean spacing
- User messages:
  - Blue background
  - White text
  - Rounded message bubble
  - Right aligned
- Smooth open/close animation

Input Area:
```

# Response

Created a comprehensive specification for the floating chatbot UI component with:

- Detailed user scenarios and acceptance criteria
- Functional requirements covering all visual and behavioral aspects
- Success criteria with measurable outcomes
- Quality validation checklist

The specification covers:
- Floating chatbot button with proper styling and hover effects
- Open chat window with header, message display, and input area
- Visual styling for user and assistant messages
- Responsive design considerations
- Edge cases and error handling

The spec is ready for the planning phase.