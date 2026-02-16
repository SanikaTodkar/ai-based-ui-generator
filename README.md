###AI-Based UI Generator (Prototype)
This project is a prototype system that converts natural language instructions into structured UI components.
It demonstrates how a multi-agent LLM pipeline can be used to plan, generate, validate, and explain UI updates in real time.

⚠️ This is an evaluation prototype and not a production-ready UI framework.

---

##1. Architecture Overview

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

Backend Flow

User sends a message (e.g., “Create a green submit button”).

The Planner agent determines intent and produces a structured plan.

The Generator agent converts the plan into a consistent UI tree format.

The tree is normalized to remove malformed nodes.

The Validator enforces allowed component rules.

The validated tree is converted into JSX.

The frontend renders the updated UI.

Previous versions are stored in memory for rollback support.

The system intentionally separates planning from generation to improve modularity and control.

---

##2. Agent Design & Prompts

The system uses three LLM-driven agents:

Planner Agent

Generator Agent

Explainer Agent

Each agent performs a focused task instead of combining all responsibilities into one large prompt.


#2.1 Planner Agent

Purpose:

Interprets natural language input

Detects user intent (create / add / modify / remove)

Outputs a structured high-level plan

The planner does not directly construct the final UI tree.
It focuses only on intent detection and component specification.

Example planner output:

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


Design decisions:

Enforced JSON-only output

Intent-based structure

Minimal logic inside prompt

Keeps mutation logic outside the LLM


#2.2 Generator Agent

Purpose:

Converts planner output into a well-formed UI tree

Ensures consistent structure (type, props, children)

Handles nested component construction

The generator ensures every node has:

{
  "type": "...",
  "props": {},
  "children": []
}


Responsibilities:

Adds missing children arrays

Normalizes component structure

Prepares tree for validation

This layer helps reduce structural inconsistencies and keeps prompts simpler.


#2.3 Explainer Agent

Purpose:

Compares previous and current UI states

Generates a human-readable explanation

Improves transparency of AI-driven updates

The explainer:

Does not modify state

Only analyzes differences

Produces descriptive reasoning output

Example explanation:

A green “Submit” button was added to the root container.




##3. Component System Design

The UI is represented as a structured JSON tree:

{
  "type": "Card",
  "props": {},
  "children": []
}


Each node contains:

type → Component name

props → Component properties

children → Nested components

Allowed Component Registry

The system enforces a predefined list of allowed components.


If the LLM outputs:

Unknown components

Malformed structures

Invalid types

They are removed during validation.

This prevents hallucinated or unsafe UI elements from being rendered.

Validation & Sanitization


The system includes:

Recursive normalization

Type checking

Structural enforcement

Property cleanup


Only validated trees are:

Stored in version history

Rendered in frontend

Version Control & Rollback

Each validated tree state is stored in memory.


Rollback:

Removes the most recent state

Restores the previous version

Re-renders the UI

This enables iterative modification through chat.


##4. Tech Stack

Backend:

FastAPI

Python

Pipenv

OpenAI-compatible API (Llama 3 Instruct)

Pydantic


Frontend:

React (Vite)

Axios

CSS

Dynamic JSX rendering



Deployment:

Backend → Render

Frontend → Vercel


##5. Known Limitations

This prototype has several limitations:

Limited component library

Basic layout intelligence

No persistent database (history stored in memory)

No authentication or multi-user support

No streaming responses

Minimal production-level error handling

LLM output quality depends on prompt stability

Render free tier cold-start delays

The system prioritizes architectural clarity over production readiness.


##6. What I Would Improve With More Time

If extended further, I would:

Add persistent storage (PostgreSQL) for version history

Implement schema-driven component validation

Improve layout reasoning (grid/flex inference)

Introduce streaming responses for better UX

Add multi-session support

Strengthen prompt guardrails

Add automated testing for tree mutations

Implement rate limiting and structured logging

Expand component library

Add design tokens / theming support


##7. Setup Instructions
Backend
cd backend
pipenv install
pipenv run uvicorn main:app --reload


Required environment variables:

OPENAI_API_KEY
OPENAI_BASE_URL

Frontend
cd frontend
npm install
npm run dev


For production deployment:

VITE_API_BASE_URL = https://your-backend-url
