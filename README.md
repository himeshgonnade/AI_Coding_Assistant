# 🧠 LogicPilot — AI Code Intelligence Platform

> **LogicPilot** is an interactive, Socratic AI coding mentor and code intelligence platform designed to help developers write, debug, optimize, and visualize code without handing out copy-paste shortcuts.

---

## ✨ Features

- 🧠 **AI Code Mentor**: A strictly scope-enforced AI assistant that answers programming questions, explains algorithms, and provides step-by-step logic hints without dumping full copy-paste code.
- 🐞 **Socratic Debugger**: An interactive debugging partner that asks targeted questions to guide you toward identifying and fixing bugs on your own.
- ⚡ **Complexity Optimizer**: Analyzes time ($O(N)$) and space complexity of code snippets, compares execution performance at scale, and provides optimization insights.
- 🗺️ **Step-by-Step Logic Pathfinder**: Breaks down complex programming goals into sequential, scaffolded thinking steps.
- 💻 **Real-Time Code Execution**: Executes code snippets instantly via the backend API.
- 🎨 **Modern Next.js UI**: Clean interface built with Monaco Editor, Framer Motion animations, and responsive dark mode design.

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 16 (React 19, TypeScript)
- **Styling**: Tailwind CSS, PostCSS
- **Editor**: `@monaco-editor/react`
- **Animations & Icons**: Framer Motion, Lucide React

### Backend
- **Framework**: FastAPI (Python 3.13)
- **AI Integration**: Groq SDK (`groq/compound` LLM model)
- **Server**: Uvicorn
- **Environment & Tools**: `python-dotenv`, `pydantic`, `httpx`

---

## 🚀 Getting Started

### Prerequisites
- **Node.js**: v18.0.0 or higher
- **Python**: v3.10 or higher
- **Groq API Key**: Obtain a free API key from [Groq Console](https://console.groq.com)

---

### 1️⃣ Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the `backend/` directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=groq/compound
   ```

5. Start the FastAPI backend server:
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

---

### 2️⃣ Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the Next.js development server:
   ```bash
   npm run dev
   ```

4. Open **[http://localhost:3000](http://localhost:3000)** in your browser.

---

## 📁 Project Structure

```
LogicPilot/
├── backend/
│   ├── main.py              # FastAPI server routes & endpoints
│   ├── requirements.txt     # Python backend dependencies
│   ├── modules/
│   │   ├── logic_engine.py  # AI Mentor Socratic system prompt
│   │   ├── debugger.py      # Socratic Debugger system prompts
│   │   ├── optimizer.py     # Complexity Analyzer & Tutor prompts
│   │   ├── pathfinder.py    # Logic Pathfinder engine
│   │   └── visualizer.py   # Code execution visualizer prompt
│   └── utils/
│       ├── groq_client.py   # Groq API client & model handler
│       └── code_runner.py   # Code execution runner
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js App Router pages
│   │   └── components/      # Compiler, Debugger, Optimizer & Visualizer UI
│   ├── package.json         # Node dependencies & scripts
│   └── tsconfig.json        # TypeScript configuration
└── README.md
```

---

## 🔒 Security & Guidelines

- **Scope Boundary**: LogicPilot's chatbot is strictly restricted to programming and computer science topics. Off-topic queries are automatically filtered with a polite redirect message.
- **No Full Code Dumps**: Prompts enforce conceptual guidance and pseudocode over raw code generation to maximize learning retention.

---

## 📄 License

This project is licensed under the MIT License.
