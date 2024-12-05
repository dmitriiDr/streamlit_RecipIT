#!/bin/sh
echo "Starting Ollama server..."
ollama serve &
sleep(5)
ollama run qwen:0.5b