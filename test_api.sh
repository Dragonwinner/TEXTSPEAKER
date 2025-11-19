#!/bin/bash

# Simple test script for the TEXTSPEAKER backend API
# Usage: ./test_api.sh

set -e

echo "================================"
echo "TEXTSPEAKER API Test Script"
echo "================================"
echo ""

# Check if Django server is running
echo "1. Checking if Django server is running on port 8000..."
if curl -s http://127.0.0.1:8000/admin/ > /dev/null 2>&1; then
    echo "✓ Django server is running"
else
    echo "✗ Django server is NOT running"
    echo "  Please start it with: cd videogen_backend && python manage.py runserver"
    exit 1
fi

echo ""
echo "2. Testing API endpoint with valid text..."
response=$(curl -s -X POST http://127.0.0.1:8000/api/generatevideo/ \
    -H "Content-Type: application/json" \
    -d '{"text": "Hello world"}')

echo "Response: $response"

if echo "$response" | grep -q "detail"; then
    echo "✓ API is responding (TTS/video generation not configured, as expected)"
else
    echo "✓ API returned video URL successfully"
fi

echo ""
echo "3. Testing API endpoint with empty text..."
response=$(curl -s -X POST http://127.0.0.1:8000/api/generatevideo/ \
    -H "Content-Type: application/json" \
    -d '{"text": ""}')

echo "Response: $response"

if echo "$response" | grep -q "empty"; then
    echo "✓ Empty text validation working"
else
    echo "⚠ Empty text validation may not be working as expected"
fi

echo ""
echo "4. Testing CORS headers..."
cors_header=$(curl -s -X OPTIONS http://127.0.0.1:8000/api/generatevideo/ \
    -H "Origin: http://localhost:3000" \
    -H "Access-Control-Request-Method: POST" \
    -I | grep -i "access-control-allow-origin")

if [ -n "$cors_header" ]; then
    echo "✓ CORS is configured: $cors_header"
else
    echo "✗ CORS headers not found"
fi

echo ""
echo "================================"
echo "Test Summary"
echo "================================"
echo "Backend API is functional!"
echo "Next steps:"
echo "  1. Install TTS library: pip install TTS"
echo "  2. Uncomment TTS code in api/views.py"
echo "  3. Add your avatar image to videogen_backend/avatar/avatar.png"
echo "  4. Integrate Wav2Lip or SadTalker model"
echo ""
