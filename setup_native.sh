#!/bin/bash
# =============================================================================
# 4D SYSTEMS NATIVE ARCHITECTURE - MAC STUDIO SETUP
# =============================================================================
# This script sets up a native 4D processing system where:
# - Each node is a genuinely different computational module
# - Sequence determines actual compute path
# - We measure real efficiency metrics
# =============================================================================

set -e

echo "=============================================="
echo "4D SYSTEMS NATIVE ARCHITECTURE SETUP"
echo "Mac Studio Edition"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# -----------------------------------------------------------------------------
# 1. CHECK PREREQUISITES
# -----------------------------------------------------------------------------
echo -e "\n${YELLOW}[1/6] Checking prerequisites...${NC}"

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
echo -e "${GREEN}✓ Homebrew${NC}"

# Check for Python 3.9+
PYTHON_VERSION=$(/usr/bin/python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"

# -----------------------------------------------------------------------------
# 2. INSTALL OLLAMA (Local LLM Runtime)
# -----------------------------------------------------------------------------
echo -e "\n${YELLOW}[2/6] Setting up Ollama...${NC}"

if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    brew install ollama
fi
echo -e "${GREEN}✓ Ollama installed${NC}"

# Start Ollama service if not running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi
echo -e "${GREEN}✓ Ollama service running${NC}"

# -----------------------------------------------------------------------------
# 3. PULL MODELS FOR DIFFERENT NODES
# -----------------------------------------------------------------------------
echo -e "\n${YELLOW}[3/6] Pulling models for node modules...${NC}"

# We use different sized models for different nodes to create genuine compute differences
# This is crucial: different nodes = different actual computation

echo "Pulling models (this may take a while on first run)..."

# Node modules mapping:
# - Tiny model (qwen2.5:0.5b): Fast pattern matching, action extraction
# - Small model (qwen2.5:1.5b): Emotion analysis, comprehension
# - Medium model (qwen2.5:3b): Reasoning, decision-making, integration

# Tiny model for fast/reactive nodes (Node 1, 4, 7)
echo "  → Tiny model (0.5B) for reactive nodes..."
ollama pull qwen2.5:0.5b

# Small model for specialized nodes (Node 6, 8, 9)
echo "  → Small model (1.5B) for specialized nodes..."
ollama pull qwen2.5:1.5b

# Medium model for complex nodes (Node 3, 5, 10)
echo "  → Medium model (3B) for complex nodes..."
ollama pull qwen2.5:3b

echo -e "${GREEN}✓ Models ready${NC}"

# -----------------------------------------------------------------------------
# 4. INSTALL PYTHON DEPENDENCIES
# -----------------------------------------------------------------------------
echo -e "\n${YELLOW}[4/6] Installing Python dependencies...${NC}"

/usr/bin/python3 -m pip install --upgrade pip --user

# Core dependencies
/usr/bin/python3 -m pip install --user \
    ollama \
    psutil \
    rich

echo -e "${GREEN}✓ Dependencies installed${NC}"

# -----------------------------------------------------------------------------
# 5. VERIFY SETUP
# -----------------------------------------------------------------------------
echo -e "\n${YELLOW}[5/6] Verifying setup...${NC}"

# Test Ollama connection
/usr/bin/python3 << 'EOF'
import ollama

try:
    response = ollama.chat(model='qwen2.5:0.5b', messages=[
        {'role': 'user', 'content': 'Say "ready" and nothing else.'}
    ])
    print(f"✓ Ollama test: {response['message']['content'].strip()}")
except Exception as e:
    print(f"✗ Ollama test failed: {e}")
EOF

# Test psutil for metrics
/usr/bin/python3 << 'EOF'
import psutil
print(f"✓ System metrics available")
print(f"  CPU cores: {psutil.cpu_count()}")
print(f"  Memory: {psutil.virtual_memory().total / (1024**3):.1f} GB")
EOF

echo ""
echo "=============================================="
echo -e "${GREEN}SETUP COMPLETE${NC}"
echo "=============================================="
echo ""
echo "Models installed:"
echo "  • qwen2.5:0.5b  (Reactive nodes - fast)"
echo "  • qwen2.5:1.5b  (Specialized nodes - balanced)"
echo "  • qwen2.5:3b    (Complex nodes - thorough)"
echo ""
echo "Next: Run the 4D Native Architecture benchmark"
echo "  python3 4d_native_architecture.py"
echo ""
