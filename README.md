# 🤖 Multi-Agent Correction and Verification System: Project Shani

This Python script implements a sophisticated **four-stage multi-agent pipeline** designed to enhance the quality, accuracy, and reliability of Large Language Model (LLM) generated content. It simulates an **Agent ADK architecture**, integrating the **Gemini API** and **Google Search grounding tool** to automate content creation, audit, refinement, and factual verification.

## 🚀 Architecture Overview

The system operates as a **sequential pipeline**, where the output of one agent becomes the input for the next, creating a **closed-loop quality control process**.

The agents are:

  * **Generation Agent (Drafting):** Creates the initial response.
  * **Inspector Agent (Auditing):** Critiques the draft for flaws.
  * **Correction Agent (Refining):** Rewrites the draft based on the critique.
  * **Verification Agent (Grounding):** Fact-checks the final output using real-time web search.

-----

## 🪐 Project Name and Vision: Shani

The project is named **Shani**, derived from the Hindu deity associated with the planet **Saturn (Shani Dev)**, who is known for dispensing justice and providing correction.

This name reflects the system's core mission: to act as a **real-time arbiter** that corrects the "mistakes" (hallucinations, factual errors, and logical inconsistencies) of raw LLM outputs, ensuring the final content output is **accurate and reliable**.

## Practical Applications

The Shani multi-agent system is designed for high-stakes content generation where **accuracy is non-negotiable**. Its primary uses include:

  * **High-Confidence Content Generation:** Producing articles, reports, and summaries that are automatically vetted for factual accuracy, suitable for professional and academic environments.
  * **Automated Fact-Checking Layer:** Serving as a crucial intermediate step in content pipelines to automatically audit and correct information before publication.
  * **Educational Content Creation:** Generating study guides, quizzes, and explanations where the verification stage guarantees the pedagogical material is sound and free from LLM errors.
  * **Research Assistance:** Providing researchers with reliable summaries of complex topics, complete with verifiable **citations (grounding)** from the web.

-----

## ⚙️ Tools and Technologies

The following tools and technologies are utilized by the system:

  * **Python (3.8+):** The primary development language and environment for agent orchestration.
  * **Gemini API** (`gemini-2.5-flash-preview-09-2025`): The core Large Language Model that powers the logic and generation of all four agents.
  * **Google Search Grounding Tool:** A built-in feature of the Gemini API used by the **Verification Agent** to provide **real-time, verifiable context and citations**, mitigating LLM hallucination.

-----

## 🧑‍💻 Agent Roles and Responsibilities

| Stage | Agent Name | Role | Gemini API Tooling |
| :---: | :--- | :--- | :--- |
| **1** | **Generation Agent** | Produces a detailed, initial draft in response to the user's query. | Standard Text Generation |
| **2** | **Inspector Agent** | Acts as a critical auditor. Identifies factual errors, logical flaws, oversimplifications, and biases in the initial response. | Standard Text Generation (Critical Persona) |
| **3** | **Correction Agent** | Reconstructs and improves the text, synthesizing the original content and the Inspector's critique to create a final, high-quality version. | Standard Text Generation (Correction Persona) |
| **4** | **Verification Agent** | Verifies the factual accuracy of the final corrected text using real-time information and provides citation sources. | **Google Search Grounding Tool** |

-----

## 🛠️ Requirements and Setup

### Prerequisites

  * **Python (3.8+)**
  * Access to the **Gemini API** (a real implementation requires an API key).

### Running the Simulation

> **Note:** This script is designed to demonstrate the workflow using simulated API responses (`_simulate_api_call`) for clarity and immediate execution.

1.  **Save the file:** Save the provided code as `multi_agent_system.py`.
2.  **Execute:** Run the file from your terminal:
    ```bash
    python multi_agent_system.py
    ```

### Expected Output

The script will print the process step-by-step, showing:

  * The initial, potentially flawed response.
  * The critique detailing the flaws.
  * The corrected, high-quality final text.
  * The verification status and simulated sources (citations) provided by the Google Search tool.

-----

## ✨ Key Concepts Demonstrated

The solution architecture successfully integrates the following required course features:

### 1\. Multi-Agent System (Sequential)

  * **Application:** The project uses four distinct agent classes (Generation, Inspector, Correction, Verification), each powered by the Gemini LLM but tasked with a specific, unique responsibility.
  * **Benefit:** This **modularity** ensures a separation of concerns, preventing a single monolithic LLM call from being responsible for all steps and improving output reliability.

### 2\. Sequential Agents

  * **Application:** The agents are orchestrated in a strict, **linear pipeline** where the output of **Agent N** is the input for **Agent N+1**.
  * **Benefit:** This workflow creates a crucial **quality control loop**: content is drafted, then audited, then corrected, and finally verified, guaranteeing a high level of rigor in the final output.

### 3\. Built-in Tools (Google Search Grounding)

  * **Application:** The Verification Agent leverages the built-in **Google Search grounding tool** provided by the Gemini API.
  * **Benefit:** This is the most critical feature for addressing **hallucination**. It forces the final output to be fact-checked against real-time web information, providing verifiable citation sources and ensuring **factual integrity**.

-----

## 🔑 Technical Features

  * **Modular Design:** Uses Python classes (`BaseAgent`) to define clear responsibilities for each stage.
  * **Quality Control Loop:** Ensures no single agent's error propagates to the final output.
  * **Factual Grounding:** Utilizes the Google Search tool in the final stage to mitigate hallucination and provide verifiable sources.
  * **System Instructions:** Leverages specific system prompts to define the distinct persona and behavior of each LLM call.

