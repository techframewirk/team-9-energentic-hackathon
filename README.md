# 📌 WIAN: Watts In A Name — Your AI-Driven Home Energy Manager

**Overview**
WIAN (Watts In A Name) is an intelligent energy management system that transforms household electricity consumption into transparent, data-driven actions. Leveraging a network of specialized micro-agents, WIAN optimizes device schedules, provides real-time usage metrics, and fosters community-based energy challenges.

---

## Key Features

* **Adaptive Scheduling**: Automatically adjusts appliance operation to align with off-peak rates and user comfort preferences.
* **Live Performance Metrics**: Displays daily savings in monetary terms, energy units (kWh), and CO₂ reduction, enabling users to track progress over time.
* **Community Leaderboards**: Compares individual household performance against local peers and aggregates results within user-defined “Green Squads.”
* **Proactive Action Queue**: Shows upcoming tasks such as device power-down, temperature adjustments, and equipment evaluations, all coordinated via Beckn Protocol signals.
* **User Override Controls**: Offers manual toggles for critical appliances, ensuring users retain final authority over automated decisions.
* **Transparent AI Reasoning**: Logs each agent decision with contextual explanations and timestamps, supporting auditability and user trust.

---

## System Architecture

* **Multi-Agent Framework**: Implements LAAM (Lightweight Agent-to-Agent Message) for inter-agent communication and a unified Context Schema for shared state management.
* **Protocol Integration**: Integrates Beckn Protocol sandbox endpoints to browse and purchase solar panels
* **Data Simulation**: Consumes synthetic grid and household telemetry from the World Engine Meter-Data Simulator to validate system responses.
* **LLM-Powered Interface**: Utilizes Google Gemini via the Generative Language API to generate conversational prompts, interpret user queries, and articulate decision rationales.

---

## Team Members

* Srikanth 
* Amogh
* Anindita
* Aswathi

---

## Technology Stack

* **Core**: Python 3.10+, Flask, flask-cors, python-dotenv, requests
* **Agent Communication**: Custom LAAM v1.0 messages over HTTP/JSON
* **State Management**: Shared Context Schema v1.0 persisted as JSON
* **AI Services**: Google Gemini (Generative Language API)
* **Protocol**: Beckn Protocol sandbox (BAP/BPP) for Demand Flexibility
* **Simulation**: World Engine Meter-Data Simulator
* **Frontend**: HTML, CSS, JavaScript (static mock interface)

---

## Installation & Execution

1. **Clone Repository**

   ```bash
   git clone <repository-url>
   cd <repository-root>/PROTOTYPE
   ```

2. **Initialize Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure Environment**

   * Create an `.env` and populate:

     * `BECKN_REGISTRY_URL`, `BECKN_GATEWAY_URL`
     * Beckn API credentials (key/secret)
     * `WORLD_ENGINE_URL`
     * `GEMINI_API_KEY`

5. **Start Backend**

   ```bash
   cd backend
   python api.py
   ```

7. **Access Frontend**

   ```bash
   cd backend
   python -m http.server 8000
   ```

---

## Demo & Visuals

* **WattsinaName Team 9 Energentic Hackathon (with voiceover)**: https://youtu.be/zvpKG7wQy7Q
* **WattsinaName Team 9 Energentic Hackathon (with backend view)**: https://youtu.be/8vXeuhzAu7A
* **Screenshots**: https://drive.google.com/drive/folders/1NjbCc4MyMSEGdyXcXpxnCZEsaZd_8t7l?usp=sharing
---

## Challenges & Insights

* **Schema Alignment**: Harmonizing multiple agents around the LAAM messaging protocol and a unified context store.
* **Conversational AI**: Integrating Gemini to produce coherent, context-aware dialogues and rationales for system actions.
* **Protocol Orchestration**: Implementing Beckn demand flexibility flows and ensuring seamless callback handling.
* **Data Fidelity**: Mapping simulated telemetry to agent workflows for realistic behavioral validation.
* **Usability Trade-offs**: Balancing automated optimizations with user override capabilities to maintain trust.

---

## References & Resources

* **Ener’gentic 2025 Hackathon Problem Statement**
  [https://energy.becknprotocol.io/wp-content/uploads/2025/05/Copy-of-DEG-Hackathon-Problem-Statement.pdf](https://energy.becknprotocol.io/wp-content/uploads/2025/05/Copy-of-DEG-Hackathon-Problem-Statement.pdf)
* **Beckn Demand Flexibility API Docs**
  [https://documenter.getpostman.com/view/23690031/2sB2qUmQAU](https://documenter.getpostman.com/view/23690031/2sB2qUmQAU)
