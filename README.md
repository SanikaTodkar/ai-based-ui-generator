# AI-Based UI Generator (Prototype)

This project is a basic AI-powered UI generation prototype that converts natural language instructions into structured UI components.

It demonstrates how an LLM can be used as a planning engine to dynamically generate and modify UI elements in real-time.

⚠️ Note: This is a prototype system created for demonstration purposes and is not a fully production-ready framework.

---

## 🚀 Features

- Natural language → UI generation
- Structured JSON UI tree
- Recursive validation & sanitization
- Live preview rendering
- Iterative modification via chat
- Explanation output from AI
- Rollback / version history support
- Dynamic button color handling

---

## 🏗 Architecture

User Input  
↓  
Planner (LLM)  
↓  
Recursive Sanitizer  
↓  
Validator (Pydantic + Allowed Components)  
↓  
JSX Renderer  
↓  
Live Preview  

The system ensures:
- Only allowed UI components are rendered
- Invalid or hallucinated components are filtered
- UI updates are version-controlled

---

## 🛠 Tech Stack

### Backend
- FastAPI
- OpenAI-compatible API (Llama 3 Instruct)
- Pydantic
- Python

### Frontend
- React
- CSS
- Dynamic component rendering

---
