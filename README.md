# AI-Based UI Generator (Prototype)

A prototype system that converts natural language instructions into structured UI components using a multi-agent LLM pipeline.

This project focuses on architectural clarity, controlled generation, and safe rendering — not production completeness.

> ⚠️ This is an evaluation prototype and not a production-ready UI framework.

---

## Architecture Overview

The system follows a controlled multi-stage pipeline:

User Input
↓
Planner Agent (Intent + High-Level Plan)
↓
Generator Agent (Structured UI Tree Construction)
↓
Tree Normalization
↓
Validator (Allowed Components Enforcement)
↓
JSX Renderer
↓
Live Preview


Each stage has a clearly defined responsibility to reduce hallucination and maintain structure.

---

### Backend Execution Flow

1. User sends a message (e.g., "Create a green submit button")
2. Planner agent determines intent and produces a structured plan
3. Generator agent converts the plan into a consistent UI tree
4. Tree is normalized and sanitized
5. Validator enforces allowed component rules
6. Validated tree is rendered as JSX
7. Previous state is stored for rollback

The separation between planning and generation keeps responsibilities modular and easier to debug.

---

## Agent Design & Prompts

The system uses three LLM-driven agents:

- **Planner Agent**
- **Generator Agent**
- **Explainer Agent**

Each agent handles a focused responsibility instead of combining all behavior into one large prompt.

---

## 1. Planner Agent

**Purpose**

- Interprets natural language input  
- Detects user intent (`create` / `add` / `modify` / `remove`)  
- Outputs a structured high-level plan  

The planner does not construct the final UI tree.  
It focuses only on intent detection and component specification.

Example Planner Output

```json
{
  "intent": "create",
  "nodes": [
    {
      "type": "Button",
      "props": {
        "label": "Submit",
        "color": "green"
      }
    }
  ]
}
```

**Design Decisions**

- Enforced JSON-only output

- Intent-based structure

- Minimal logic inside the prompt

- Keeps mutation logic outside the LLM

---

## 2. Generator Agent

**Purpose**

- Converts planner output into a well-formed UI tree

- Ensures consistent structure (type, props, children)

- Handles nested component construction

- Each node is normalized into:

``` json
{
  "type": "...",
  "props": {},
  "children": []
}
```

**Responsibilities**

- Adds missing children arrays

- Normalizes node structure

- Prepares tree for validation

- This layer reduces structural inconsistencies and keeps prompts simpler.

---

## 3. Explainer Agent
**Purpose**

- Compares previous and current UI states

- Generates a human-readable explanation

- Improves transparency of AI-driven updates

The explainer:

- Does not modify application state

- Only analyzes differences

- Produces descriptive reasoning output


Example explanation:

A green “Submit” button was added to the root container.

---

## Component System Design

The UI is represented as a structured JSON tree:
 ``` json
{
  "type": "Card",
  "props": {},
  "children": []
}
```

Each node contains:

- type — Component name

- props — Component properties

- children — Nested components

---

**Allowed Component Registry**

The system enforces a predefined list of allowed components.

If the LLM outputs:

- Unknown components

- Malformed structures

- Invalid types

They are removed during validation.

Only validated trees are rendered.

---

**Validation & Sanitization**

The backend performs:

- Recursive normalization

- Type checking

- Structural enforcement

- Property cleanup

This ensures hallucinated or unsafe UI elements are filtered before rendering.

---

**Version Control & Rollback**

Each validated tree state is stored in memory.

Rollback:

- Removes the most recent state

- Restores the previous version

- Re-renders the UI

This enables iterative UI modification through chat.

---

## Tech Stack

**Backend**

- FastAPI

- Python

- Pipenv

- OpenRouter-compatible API (Llama 3 Instruct)

- Pydantic

**Frontend**

- React (Vite)

- Axios

- CSS

- Dynamic JSX rendering

**Deployment**

Backend → Render

Frontend → Vercel

---

**Known Limitations**

This prototype intentionally keeps scope limited:

- Limited component library

- Basic layout intelligence

- No persistent database (history stored in memory)

- No authentication or multi-user support

- No streaming responses

- Minimal production-level error handling

- LLM output depends on prompt consistency

- Render free tier introduces cold-start delays

The system prioritizes architectural clarity over production readiness.

---

**What I Would Improve With More Time**

If extended further, I would:

1. Add persistent storage (PostgreSQL) for version history

2. Implement schema-driven component validation

3. Improve layout reasoning (grid/flex inference)

4. Introduce streaming responses for better UX

5. Add multi-session support

6. Strengthen prompt guardrails

7. Implement rate limiting and structured logging

8. Expand the component library

9. Add design tokens and theming support

---

## Setup Instructions

**Backend**

```
cd backend
pipenv install
pipenv run uvicorn main:app --reload
```

**Required environment variables:**

OPENAI_API_KEY
OPENAI_BASE_URL


**Frontend**

```
cd frontend
npm install
npm run dev
```

For production deployment:

VITE_API_BASE_URL=https://your-backend-url

---

**Project Focus**

This prototype demonstrates:

- Controlled AI-driven UI planning

- Multi-agent separation of responsibilities

- Structured tree generation

- Validation layers for safety

- Iterative modification via chat

- Transparent explanation of changes

The primary goal is to demonstrate system design thinking around LLM-powered UI generation rather than build a full production UI builder.
