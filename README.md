# End-to-End Agentic AI Chatbot

A production-ready Agentic AI application built with **LangGraph**, **LangChain**, and **Streamlit**. This application provides a modular and stateful architecture for building advanced AI agents.

## Features

-   **Stateful Conversations**: Maintains context across user interactions using LangGraph.
-   **Modular Architecture**: Clean separation of concerns (UI, Graph Logic, Nodes, LLM Configuration).
-   **Streamlit UI**: Interactive and dynamic user interface with chat history management.
-   **Logging**: Centralized logging for debugging and monitoring (`logs/` directory).
-   **Extensible**: Easy to add new use cases and nodes.

## Project Structure

```
d:\jake\
├── app.py                      # Application Entry Point
├── requirements.txt            # Project Dependencies
├── tests/                      # Unit Tests
├── logs/                       # Application Logs
└── src/
    ├── langgraphagenticai/     # Core Logic
    │   ├── graph/              # Graph Construction
    │   ├── nodes/              # Graph Nodes (Agents/Tools)
    │   ├── state/              # State Definition
    │   ├── LLMS/               # LLM Configuration (Groq, etc.)
    │   └── main.py             # Logic Entry Point
    ├── ui/                     # User Interface
    │   ├── streamlitui/        # Streamlit Components
    │   ├── main.py             # UI Orchestration
    │   └── uiconfigfile.*      # UI Configuration
    └── utils/
        └── logger.py           # Logging Utility
```

## Setup & Installation

1.  **Clone the repository** (if applicable).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

## Configuration

-   **API Keys**: Enter your **Groq API Key** in the sidebar.
-   **UI Settings**: Modify `src/ui/uiconfigfile.ini` to change page titles, model options, or available use cases.

## Testing

Run unit tests to verify functionality:
```bash
python -m unittest discover tests
```

## Logs

Logs are automatically generated in the `logs/` directory. Check them for debugging info and runtime errors.
