# Multimodal Persona Agents 

## 🚀 Overview

**Configurable multimodal AI agent framework** combining real-time communication, modern multimodal LLMs, and agentic tool integrations into a single unified system.

This agent can *listen, speak, see, interpret, and act* — supporting personal assistants, automation workflows, enterprise tasks, and real-time interactive UIs.

---

## ✨ Key Features

### **Modular Model Configuration**
- Supports Gemini, OpenAI, Anthropic, Llama, and more  
- Fully pluggable STT/TTS engines (all can be self-hosted locally)  
- Swap models with simple config changes

### **Real-Time Voice Interaction**
- **AssemblyAI STT** for fast speech recognition  
- **Cartesia AI TTS** for natural, expressive voice output  
- Real-time streaming powered by **LiveKit**

### **Image, Camera & Screen Understanding**
- Understands photos, screenshots, webcam feeds  
- Suitable for UI automation, screen reasoning, and vision-based tasks

### **Agentic Tools**
- Custom tools for **web search** using a self-hosted **SearxNG** Docker container  
- Tools to **browse the web**, like searching and playing YouTube videos  
- Simple architecture to add new workflows or enterprise automations

### **Frontend**
- Main Frontend is built using **Next.js** and hosted simplified frontend is built using **Vite React**.
- Live demo: **https://ayush-trikaya.pages.dev/**

### **Backend / Infra**
- Python-based agent runtime  
- Real-time communication via WebSockets  
- Dockerized environment for easy deployment  
- Integration-friendly code structure

---

## 🛠️ Technologies Used

- **Python**  
- **Next.js**  
- **Docker**  
- **LiveKit**  
- **WebSockets**  
- **SearxNG (self-hosted meta search engine)**  
- **Web scraping tools**  
- **AssemblyAI (STT)**  
- **Cartesia AI (TTS)**  
- **Multimodal LLMs** (Gemini, OpenAI, etc.)  
- **Custom agentic toolchains**

---

## 📌 To-Do / Next Steps

- [x] Multi LLM support (no vendor lock-in)
- [x] Multi tool support (STTs and TTSs models)
- [x] SearXNG meta search engine support 
- [x] Basic automation (PyAutoGUI)
- [ ] Integrate **n8n** for agentic workflows  
- [ ] Host backend on a **VPS**  
- [ ] Add **rate limiting**  
- [ ] Implement **global state management**

---

Crafted with ❤️ by Ayush Singh.