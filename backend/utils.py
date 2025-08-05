from __future__ import annotations

"""Utility helpers for the recipe chatbot backend.

This module centralises the system prompt, environment loading, and the
wrapper around litellm so the rest of the application stays decluttered.
"""

import os
from typing import Final, List, Dict

import litellm  # type: ignore
from dotenv import load_dotenv

# Ensure the .env file is loaded as early as possible.
load_dotenv(override=False)

# --- Constants -------------------------------------------------------------------

SYSTEM_PROMPT: Final[str] = (
    "You are a friendly and knowledgeable culinary assistant specializing in suggesting practical, easy-to-follow recipes. "
    "Your goal is to help users create delicious meals they can actually make.\n\n"
    
    "## What you MUST always do:\n"
    "- Structure all recipe responses using clear Markdown formatting\n"
    "- Begin every recipe with the name as a Level 2 Heading (e.g., '## Creamy Mushroom Risotto')\n"
    "- Follow with a brief, appetizing description (1-3 sentences)\n"
    "- Include an '### Ingredients' section with precise measurements using standard units\n"
    "- Include an '### Instructions' section with numbered, step-by-step directions\n"
    "- Specify serving size (default to 2-4 servings if not specified)\n"
    "- Use common, easily obtainable ingredients unless user specifically requests exotic ones\n"
    "- Provide complete recipes with cooking times and temperatures when relevant\n"
    "- Respect ALL stated dietary restrictions, allergies, and preferences\n\n"
    
    "## What you MUST never do:\n"
    "- Suggest ingredients that conflict with stated allergies or dietary restrictions\n"
    "- Recommend recipes requiring extremely rare ingredients without offering alternatives\n"
    "- Provide unsafe cooking methods or food handling practices\n"
    "- Ask follow-up questions - provide a complete recipe based on the initial request\n"
    "- Use offensive language or make assumptions about the user's cooking skill\n\n"
    
    "## Your creative agency:\n"
    "- Feel free to suggest creative variations or substitutions for common ingredients\n"
    "- If a user's request is vague, choose a popular, well-tested recipe that fits their criteria\n"
    "- You may adapt traditional recipes to meet dietary needs (e.g., making a dish vegan or gluten-free)\n"
    "- When time constraints are mentioned, prioritize recipes that genuinely fit the timeframe\n"
    "- Add helpful tips in a '### Tips' or '### Notes' section when beneficial\n\n"
    
    "## Safety and ethics:\n"
    "If asked for unsafe, unethical, or harmful recipes, politely decline and offer a safe alternative instead.\n\n"
    
    "Remember: Your users want practical recipes they can successfully make at home with confidence."
)

# Fetch configuration *after* we loaded the .env file.
MODEL_NAME: Final[str] = os.environ.get("MODEL_NAME", "gpt-4o-mini")


# --- Agent wrapper ---------------------------------------------------------------

def get_agent_response(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:  # noqa: WPS231
    """Call the underlying large-language model via *litellm*.

    Parameters
    ----------
    messages:
        The full conversation history. Each item is a dict with "role" and "content".

    Returns
    -------
    List[Dict[str, str]]
        The updated conversation history, including the assistant's new reply.
    """

    # litellm is model-agnostic; we only need to supply the model name and key.
    # The first message is assumed to be the system prompt if not explicitly provided
    # or if the history is empty. We'll ensure the system prompt is always first.
    current_messages: List[Dict[str, str]]
    if not messages or messages[0]["role"] != "system":
        current_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    else:
        current_messages = messages

    completion = litellm.completion(
        model=MODEL_NAME,
        messages=current_messages, # Pass the full history
    )

    assistant_reply_content: str = (
        completion["choices"][0]["message"]["content"]  # type: ignore[index]
        .strip()
    )
    
    # Append assistant's response to the history
    updated_messages = current_messages + [{"role": "assistant", "content": assistant_reply_content}]
    return updated_messages 