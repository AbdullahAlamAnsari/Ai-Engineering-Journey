# 🔗 n8n AI Agent Workflows

<p align="center">
  <img src="https://img.shields.io/badge/n8n-EA4B71?style=flat-square&logo=n8n&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" />
  <img src="https://img.shields.io/badge/Cohere-39594D?style=flat-square" />
  <img src="https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=white" />
  <img src="https://img.shields.io/badge/Pinecone-000000?style=flat-square" />
  <img src="https://img.shields.io/badge/Airtable-18BFFF?style=flat-square&logo=airtable&logoColor=white" />
  <img src="https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blue?style=flat-square" />
</p>

A collection of AI agent workflows built in **n8n**, exploring agentic automation, RAG pipelines, MCP servers/clients, and no-code AI-powered business processes. Each workflow is exported as a ready-to-import `.json` file.

---

## 📁 Workflows

### 📧 Email Filter — Feedback Classifier
`Email_filter.json`
Classifies incoming form submissions (customer feedback) into **Complaint**, **Compliment**, or **Feature Request**, then routes each to the right destination.
- Form submission trigger → AI Agent (OpenAI) classifies the feedback
- Switch node branches based on classification
- Logs each category into its own Airtable table
- Sends real-time notifications via Slack (complaints/compliments) and Gmail (feature requests)

### 💼 Job Filter — Applicant Router
`Job_filter.json`
Routes job applications submitted via a form to the correct role-specific Airtable table using AI classification.
- Form trigger captures applicant details
- AI Agent (Google Gemini) determines the applied-for role
- Switch node routes to **AI Engineer**, **Video Editor**, or **Graphic Designer** tables
- Creates and updates Airtable records to track applicant status

### 🗂️ Big Data Filter — Customer Data Cleaner
`Big_data_filter.json`
Pulls customer records, reshapes the fields, and branches the data based on whether a `Country` value exists.
- Fetches all records from the n8n training customer datastore
- Standardizes fields into Full Name, Email, Country, ID
- `If` node checks for missing `Country`
- Routes valid vs. incomplete records down separate paths for different handling

### 📬 Email Responder — Auto-Draft Agent
`Email_responder.json`
Scans unread Gmail messages on a schedule and drafts AI-generated replies, logging everything for review before sending.
- Hourly Schedule Trigger → fetches unread emails from Gmail
- AI Agent (Cohere) drafts a reply body for each email
- Saves sender info, original email, and the drafted reply to Airtable
- Marks the original email thread as read once processed

### 🍳 Recipe Generator — Structured Output Agent
`Json_workflow.json`
Chat-triggered agent that generates a full recipe (ingredients, instructions, tips) in strict JSON format and saves it to Airtable.
- Chat trigger accepts a dish name from the user
- AI Agent (Cohere) generates the recipe using a structured system prompt
- Structured + Auto-fixing Output Parsers enforce a consistent JSON schema
- Saves the parsed recipe fields directly into an Airtable table

### 🔌 MCP Client + AI Agent
`MCP_CLIENT___AI_AGENT.json`
A conversational AI agent that connects to an external MCP server as a tool source, with memory for multi-turn context.
- Chat trigger → AI Agent (Cohere) with buffer window memory
- Connects to a remote MCP server endpoint as a callable tool
- Demonstrates client-side MCP tool consumption inside an n8n agent

### 🖧 MCP Server Trigger — Tool Exposer
`MCP_SERVER_TRIGGER.json`
Exposes Gmail and YouTube actions as MCP tools that any MCP-compatible client (including Claude) can call remotely.
- MCP Server Trigger node opens an MCP-accessible endpoint
- Exposes **Get many Gmail messages**, **Get many YouTube channels**, and **Send a Gmail message** as callable tools
- Lets external AI clients interact with Gmail/YouTube through a single MCP connection

### 🧠 RAG Data Processing — Knowledge Base Ingestion
`RAG_DATA_PROCESSING.json`
Watches a Google Drive folder for new documents and automatically embeds them into a Pinecone vector store.
- Google Drive Trigger polls a "Knowledge Base" folder every minute for new files
- Downloads new files and loads them via a `.docx` document loader
- Generates embeddings with Cohere (`embed-english-v3.0`)
- Inserts vectors into a Pinecone index (`n8nagent`) for later retrieval

### 🔍 RAG Data Retrieval — Personal Knowledge Agent
`RAG_DATA_RETRIVAL.json`
A chat agent that answers questions strictly from a personal knowledge base — no hallucination allowed.
- Chat trigger → AI Agent (Cohere) with buffer memory
- Retrieves context via a Pinecone Vector Store tool (same `n8nagent` index as the ingestion workflow)
- System prompt enforces tool-only answers — refuses to answer from general knowledge if the tool returns nothing
- Built as a personal assistant that only speaks from verified, ingested facts

### 🎙️ Voice Agent — RAG-Powered Webhook Assistant
`voice_agent.json`
End-to-end voice/webhook-triggered version of the personal knowledge agent, combining ingestion and retrieval in one workflow.
- Webhook receives a question (e.g. from a voice interface) and responds via `Respond to Webhook`
- AI Agent (Cohere) answers strictly using a Pinecone-backed retrieval tool
- Includes its own embedded Google Drive → Pinecone ingestion pipeline to keep the knowledge base updated
- Designed to power a voice assistant that only speaks accurate, sourced information

---

## 🛠️ Core Stack

- **n8n** — visual workflow orchestration
- **LangChain (n8n nodes)** — AI Agent, memory, output parsers, vector store integration
- **LLMs:** Cohere, OpenAI, Google Gemini
- **Pinecone** — vector database for RAG
- **Cohere Embeddings** (`embed-english-v3.0`) — text embeddings for retrieval
- **Airtable** — structured data storage/logging across workflows
- **Gmail, Google Drive, Slack, YouTube** — integrated triggers and actions
- **MCP (Model Context Protocol)** — both client and server implementations for cross-tool AI agent connectivity

---

## 🗂️ Repo Structure

```
.
├── Email_filter.json
├── Job_filter.json
├── Big_data_filter.json
├── Email_responder.json
├── Json_workflow.json
├── MCP_CLIENT___AI_AGENT.json
├── MCP_SERVER_TRIGGER.json
├── RAG_DATA_PROCESSING.json
├── RAG_DATA_RETRIVAL.json
├── voice_agent.json
└── README.md
```

## ▶️ How to Use

1. Open your n8n instance
2. Go to **Workflows → Import from File**
3. Select any `.json` file from this repo
4. Reconnect the required credentials (Gmail, Cohere, OpenAI, Google Gemini, Pinecone, Airtable, Slack, Google Drive) — credential IDs are stripped/instance-specific and won't carry over
5. Activate the workflow

---

## 💡 What I Learned

Building these workflows across classification, RAG, and MCP taught me how to design agents that stay grounded — using tool-forced retrieval and strict system prompts to prevent hallucination — and how to wire together triggers, branching logic, and multiple LLM providers into reliable, production-style automations without writing a full backend from scratch.

---

## 👤 About Me

**Abdullah Alam Ansari**
BS Computer Science, GIK Institute of Engineering Sciences and Technology (GIKI)

<p align="center">Automating one workflow at a time ⚙️</p>
