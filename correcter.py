#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: macOS Text Correction/Rephrasing via OpenAI (Adjusted for Karabiner)
Description:
- This script interacts with the clipboard to correct or rephrase text using OpenAI's API.
- Designed to be triggered by Karabiner with optional parameters for mode (correction or rephrasing).
- Displays a badge in the top-right corner to indicate processing status.

Usage:
- Command + c: Correction (default mode)
- Ctrl + r: Rephrasing (triggered with --rephrase)
"""

import os
import sys
import logging
import pyperclip
import openai
import pyautogui
import time

# Configure Logging
logging.basicConfig(
    filename='/tmp/script.log',
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    logging.error("OPENAI_API_KEY not set.")
    print("Error: OPENAI_API_KEY not set.")
    sys.exit(1)

def show_notification(title, message):
    """
    Display a macOS notification in the top-right corner.

    Args:
        title (str): The title of the notification.
        message (str): The message content of the notification.
    """
    try:
        os.system(f'osascript -e \'display notification "{message}" with title "{title}"\'')
    except Exception as e:
        logging.error(f"Error showing notification: {e}")

def process_text(mode='correct'):
    """
    Process clipboard text for correction or rephrasing.

    Args:
        mode (str): The mode of processing ('correct' or 'rephrase'). Defaults to 'correct'.
    """
    try:
        # Simulate Command+C to copy selected text
        logging.info("Simulating Command+C to copy selected text.")
        pyautogui.hotkey('command', 'c')
        time.sleep(0.2)  # Allow some time for clipboard to update

        # Get text from clipboard
        text = pyperclip.paste()
        if not text.strip():
            logging.warning("No text found in clipboard.")
            return

        # Define system message based on mode
        system_message = (
            "You are a helpful assistant who corrects grammar and spelling. "
            "Keep the original meaning intact." if mode == 'correct'
            else "You are a helpful assistant who rephrases text for clarity and conciseness."
        )

        # Send text to OpenAI
        logging.info(f"Sending text to OpenAI for {mode}.")
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": text}
            ],
            max_tokens=500,
            temperature=0.2,
            timeout=10
        )

        # Extract the result
        result = response.choices[0].message.content.strip()
        result = result.rstrip(".")  # Remove trailing dots

        # Update clipboard with the result
        pyperclip.copy(result)
        logging.info("Text processed successfully. Updating clipboard.")

        # Show a notification that processing has completed
        show_notification("Text Processing", "Text has been processed and copied to clipboard.")

        # Simulate Command+V to paste the result
        logging.info("Simulating Command+V to paste the result.")
        pyautogui.hotkey('command', 'v')
        time.sleep(0.2)

    except Exception as e:
        logging.error(f"Error processing text: {e}")

if __name__ == "__main__":
    # Parse command-line arguments
    mode = 'correct'  # Default mode
    if len(sys.argv) > 1 and sys.argv[1] == '--rephrase':
        mode = 'rephrase'

    # Process the text
    process_text(mode=mode)