import json
import time
from typing import Dict, Any, List

# --- Configuration and Utility Functions ---

GEMINI_MODEL = "gemini-2.5-flash-preview-09-2025"
API_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
# Simulate the API Key being available from the environment.
# Note: In a real application, this should be loaded securely from an environment variable.
API_KEY = ""

def _simulate_api_call(system_instruction: str, user_prompt: str, use_grounding: bool = False, payload_modifier: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Simulates the network call to the Gemini API with predefined responses.

    This function prints the API request structure and returns hardcoded results
    to demonstrate the multi-agent workflow without making actual network calls.
    In a real implementation, this would involve a robust HTTP client with retry logic.

    Args:
        system_instruction: The instruction defining the agent's role for the LLM.
        user_prompt: The specific query or task for the LLM to execute.
        use_grounding: If True, the Google Search tool is added to the payload.
        payload_modifier: Optional dictionary to update the base API payload.

    Returns:
        A dictionary containing the simulated 'text' response and 'sources' list.
    """
    print(f"\n--- SIMULATING API CALL ({'GROUNDED' if use_grounding else 'STANDARD'}) ---")
    print(f"MODEL: {GEMINI_MODEL}")
    print(f"SYSTEM INSTRUCTION: '{system_instruction[:80]}...'")

    payload = {
        "contents": [{"parts": [{"text": user_prompt}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]}
    }

    if use_grounding:
        # Mandatory tool definition for Google Search grounding
        payload["tools"] = [{"google_search": {}}]

    if payload_modifier:
        payload.update(payload_modifier)

    print(f"PAYLOAD PREVIEW (JSON): {json.dumps(payload, indent=2)[:500]}...")

    # --- SIMULATED RESPONSE LOGIC based on the Agent's system instruction ---
    time.sleep(0.5) # Simulate network delay

    # 1. Generation Agent Simulation
    if system_instruction.startswith("You are a world-class content creator"):
        return {
            "text": "The primary cause of the Industrial Revolution was the invention of the steam engine in 1769 by James Watt, which allowed factories to be built anywhere, leading to rapid urbanization and economic growth.",
            "sources": []
        }
    # 2. Inspector Agent Simulation
    elif system_instruction.startswith("You are a critical auditing agent"):
        return {
            "text": "Critique: The statement oversimplifies the cause. James Watt improved the steam engine (Newcomen's engine was earlier), and his work was in 1776, not 1769. The cause was multifactorial, including capital, political stability, and agricultural advances. Reasoning is weak.",
            "sources": []
        }
    # 3. Correction Agent Simulation
    elif system_instruction.startswith("You are an expert correction agent"):
        return {
            "text": "The Industrial Revolution was a period of major mechanization driven by several interlocking factors, including significant agricultural advancements, the accumulation of capital, favorable political stability in Great Britain, and key technological innovations. Crucially, the practical refinement of the steam engine by figures like James Watt (following earlier designs by Newcomen) provided a reliable, scalable power source that facilitated the rapid growth of the textile and manufacturing industries.",
            "sources": []
        }
    # 4. Verification Agent Simulation (Requires Grounding)
    elif use_grounding:
        return {
            "text": "Verification complete. All claims appear grounded and accurate.",
            "sources": [
                {"title": "Causes of the Industrial Revolution - History.com", "uri": "https://www.history.com/topics/industrial-revolution/industrial-revolution"},
                {"title": "James Watt and the Steam Engine - Science Museum", "uri": "https://www.sciencemuseum.org.uk/objects/watt_engine"}
            ]
        }
    return {"text": "Simulated default response.", "sources": []}


# --- Agent Definitions ---

class BaseAgent:
    """
    Base class for all agents in the multi-agent system.

    Provides common initialization logic for the agent name and its fixed
    system instruction (persona).
    """
    def __init__(self, name: str, system_prompt: str):
        """
        Initializes the base agent.

        Args:
            name: The human-readable name of the agent (e.g., 'Inspector Agent').
            system_prompt: The instruction defining the agent's role for the LLM.
        """
        self.name = name
        self.system_prompt = system_prompt

    def run(self, input_data: str) -> Dict[str, Any]:
        """
        Runs the agent's core task. Must be implemented by subclasses.

        Args:
            input_data: The input string (e.g., a query, or the output of a previous agent).

        Returns:
            A dictionary containing the agent's output and metadata.
        """
        raise NotImplementedError("Subclasses must implement the run method.")

class GenerationAgent(BaseAgent):
    """
    1. Generates the initial content based on the user's query.

    Acts as the first stage in the pipeline, producing a draft response.
    """
    def __init__(self):
        system_prompt = (
            "You are a world-class content creator and initial response generator. "
            "Your task is to produce a detailed, informative, and engaging response "
            "to the user's query. Be confident but do not hallucinate."
        )
        super().__init__("Generation Agent", system_prompt)

    def run(self, topic: str) -> str:
        """
        Generates the initial draft content.

        Args:
            topic: The user's original query.

        Returns:
            The raw text string generated by the LLM.
        """
        print(f"\n[{self.name}] received topic: '{topic}'")
        response = _simulate_api_call(self.system_prompt, topic)
        return response["text"]

class InspectorAgent(BaseAgent):
    """
    2. Audits the initial response for factual errors, logical flaws, and bias.

    The Inspector agent is designed to be highly critical and output a focused critique.
    """
    def __init__(self):
        system_prompt = (
            "You are a critical auditing agent (the Inspector). Your job is to meticulously "
            "review the provided text. Identify any factual inaccuracies, oversimplifications, "
            "logical inconsistencies, or potential biases. Return a concise 'Critique' only."
        )
        super().__init__("Inspector Agent", system_prompt)

    def run(self, initial_response: str) -> str:
        """
        Audits the provided text and generates a critique.

        Args:
            initial_response: The output text from the Generation Agent.

        Returns:
            The critique text string generated by the LLM.
        """
        prompt = f"Critique the following text for accuracy and logic:\n\n---\n{initial_response}\n---"
        print(f"\n[{self.name}] performing audit on the generated response.")
        response = _simulate_api_call(self.system_prompt, prompt)
        return response["text"]

class CorrectionAgent(BaseAgent):
    """
    3. Reconstructs and improves the content based on the inspector's critique.

    This agent synthesizes the original text and the feedback to create a final,
    high-quality version.
    """
    def __init__(self):
        system_prompt = (
            "You are an expert correction agent. You must take the original text and the "
            "inspector's critique, and produce a fully corrected, high-quality, and comprehensive "
            "rewrite that addresses all identified issues. Output only the corrected text."
        )
        super().__init__("Correction Agent", system_prompt)

    def run(self, initial_response: str, critique: str) -> str:
        """
        Rewrites the initial response based on the critique.

        Args:
            initial_response: The original text.
            critique: The feedback from the Inspector Agent.

        Returns:
            The corrected text string generated by the LLM.
        """
        prompt = (
            f"Original Text:\n---\n{initial_response}\n---\n\n"
            f"Inspector's Critique:\n---\n{critique}\n---\n\n"
            "Produce the corrected and improved version of the text."
        )
        print(f"\n[{self.name}] performing correction based on critique.")
        response = _simulate_api_call(self.system_prompt, prompt)
        return response["text"]

class VerificationAgent(BaseAgent):
    """
    4. Confirms the factual accuracy of the final content using Google Search grounding.

    This agent uses the search tool to ground the claims and provide citations.
    """
    def __init__(self):
        system_prompt = (
            "You are the Verification Agent, tasked with confirming the factual accuracy of the "
            "provided content by using the Google Search grounding tool. "
            "Do not rewrite the text, simply confirm its factual basis and provide citations."
        )
        super().__init__("Verification Agent", system_prompt)

    def run(self, final_response: str) -> Dict[str, Any]:
        """
        Fact-checks the final response using the Google Search tool.

        Args:
            final_response: The output text from the Correction Agent.

        Returns:
            A dictionary containing the verification status text and the sources list.
        """
        prompt = f"Fact-check and cite all claims in the following corrected text:\n\n---\n{final_response}\n---"
        print(f"\n[{self.name}] performing factual verification using Google Search grounding.")

        # This call must include the 'tools' property for Google Search
        verification_data = _simulate_api_call(
            self.system_prompt,
            prompt,
            use_grounding=True
        )
        return verification_data

# --- Multi-Agent Orchestrator ---

class MultiAgentSystem:
    """
    Orchestrates the workflow between the four distinct agents.

    The pipeline ensures content is generated, audited, corrected, and finally
    verified for factual accuracy using the Gemini API and Google Search grounding.
    """
    def __init__(self):
        """Initializes all four agents."""
        self.generation_agent = GenerationAgent()
        self.inspector_agent = InspectorAgent()
        self.correction_agent = CorrectionAgent()
        self.verification_agent = VerificationAgent()
        self.agents = [
            self.generation_agent,
            self.inspector_agent,
            self.correction_agent,
            self.verification_agent
        ]
        print("Multi-Agent System Initialized.")

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Executes the 4-stage agent pipeline for a given query.

        Args:
            query: The initial user prompt.

        Returns:
            A dictionary summarizing the output of all stages of the pipeline.
        """
        print("="*60)
        print(f"STARTING PIPELINE for Query: '{query}'")
        print("="*60)

        # 1. Generation
        initial_response = self.generation_agent.run(query)
        print("\n\n--- 1. GENERATION AGENT OUTPUT (Initial Response) ---")
        print(initial_response)

        # 2. Inspection
        critique = self.inspector_agent.run(initial_response)
        print("\n\n--- 2. INSPECTOR AGENT OUTPUT (Critique) ---")
        print(critique)

        # 3. Correction
        corrected_response = self.correction_agent.run(initial_response, critique)
        print("\n\n--- 3. CORRECTION AGENT OUTPUT (Final Corrected Text) ---")
        print(corrected_response)

        # 4. Verification
        verification_data = self.verification_agent.run(corrected_response)
        verification_text = verification_data.get("text", "N/A")
        sources = verification_data.get("sources", [])
        print("\n\n--- 4. VERIFICATION AGENT OUTPUT (Grounded Verification) ---")
        print(verification_text)

        # Final Report
        print("\n" + "="*60)
        print("PIPELINE COMPLETE - FINAL REPORT")
        print("="*60)
        print("FINAL CORRECTED TEXT:")
        print(corrected_response)
        print("\nFACTUAL SOURCES (via Google Search Tool):")
        if sources:
            for i, source in enumerate(sources, 1):
                # Prints the source title and URI for verification
                print(f"  {i}. {source.get('title', 'No Title')} - {source.get('uri', 'No URI')}")
        else:
            print("  No verifiable sources found in the simulation.")

        return {
            "query": query,
            "initial_response": initial_response,
            "critique": critique,
            "corrected_response": corrected_response,
            "verification_text": verification_text,
            "sources": sources
        }

# --- Execution ---
if __name__ == "__main__":
    system = MultiAgentSystem()
    query = "What were the main causes of the Industrial Revolution?"
    system.process_query(query)
