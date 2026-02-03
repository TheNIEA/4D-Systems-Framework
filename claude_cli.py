#!/usr/bin/env python3
"""
Simple Claude CLI - Interactive chat with Claude
Usage: python3 claude_cli.py
"""
import os
import sys
from anthropic import Anthropic

def main():
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    client = Anthropic(api_key=api_key)
    
    print("Claude CLI - Type 'exit' or 'quit' to end\n")
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8096,
                messages=conversation_history
            )
            
            assistant_message = response.content[0].text
            conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            print(f"\nClaude: {assistant_message}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
