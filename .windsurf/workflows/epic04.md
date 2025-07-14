---
description: Epic 4 Modular RAG Agent Architecture
---

This document outlines the development workflow for creating a system of interconnected AI agents to perform complex RAG tasks.

## Agents

- **Retriever Agent**: Fetches relevant context from the vector store based on a query.
- **Augmentor Agent**: Enriches or updates existing content by finding and filling gaps.
- **Writer Agent**: Generates new, long-form content from prompts and retrieved context.
- **Editor Agent**: Refines existing text for tone, style, formatting, and grammar.

## User Stories Covered

- **US4.1:** As a user, I want agents to help answer questions from my Markdown docs.
- **US4.2:** As a user, I want agents to help me co-author new documentation.
- **US4.3:** As a user, I want agents to suggest updates for outdated docs.

## Planned Implementation Steps

1.  **Module Creation:**

    - A new `agents` module will be created within the `rag_system` package. This will be the central hub for all agent-related logic.
    - It will contain sub-modules for each agent type (e.g., `agents/retriever.py`, `agents/writer.py`) and a central `router.py` for agent-driven endpoints.

2.  **Base Agent Class:**

    - An abstract `BaseAgent` class will be defined to establish a common interface for all agents (e.g., an `execute` method).
    - This promotes consistency and allows agents to be used interchangeably in workflows.

3.  **LLM Integration:**

    - A new `llm` module will be created to abstract communication with Large Language Models.
    - It will contain an `ollama_provider.py` to handle prompting and receiving responses from generative models (distinct from the embedding models).

4.  **Agent Implementation:**

    - **Retriever Agent:** This agent will be a lightweight wrapper around the `SearchService` developed in Epic 3. Its primary role is to fetch context for other agents.
    - **Writer Agent:** This agent will take a user prompt and retrieved context (from the Retriever Agent) to generate a new piece of documentation. It will use the `llm` provider to generate the text.
    - **Editor Agent:** This agent will take a piece of text and a set of instructions (e.g., "make this more formal") and use the `llm` provider to refine it.
    - **Augmentor Agent:** This agent will orchestrate a more complex workflow: retrieve context related to a topic, analyze it for gaps or outdated information (using the LLM), and then use the Writer/Editor agents to generate suggested updates.

5.  **Agentic Workflow Endpoints (US4.1, US4.2, US4.3):**

    - New API endpoints will be created in `agents/router.py` to expose the capabilities of the agents.
    - **/agents/qna (US4.1):** An endpoint that takes a question. It will use the `Retriever Agent` to find context and the `Writer Agent` to synthesize an answer.
    - **/agents/co-author (US4.2):** An endpoint that takes a topic or prompt. It will use the `Retriever Agent` and `Writer Agent` to generate a first draft.
    - **/agents/suggest-updates (US4.3):** An endpoint that takes a document or topic. It will use the `Augmentor Agent` to analyze and suggest changes.

6.  **Integration:**
    - The new `agents_router` will be included in the main `FastAPI` application in `main.py`.
