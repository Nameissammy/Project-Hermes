"""
Simple Gemini API Test Script
This script tests the Gemini API key directly without using CrewAI
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("No Gemini API key found in environment variables.")
    exit(1)

print(f"Found Gemini API key: {api_key[:5]}...{api_key[-5:]}")

# Configure the Gemini API
genai.configure(api_key=api_key)

# List available models
print("\nListing available models:")
for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(f"- {model.name}")

# Use the Gemini API
print("\nTesting Gemini API with a simple prompt:")
model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content("Write a short poem about AI.")

print("\nResponse from Gemini:")
print(response.text)

print("\nGemini API test completed successfully!")
