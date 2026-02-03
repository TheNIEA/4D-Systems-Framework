#!/bin/bash
# =============================================================================
# 4D Systems Framework - Mac Studio Setup Script
# Created by Khoury Howell
# =============================================================================
#
# Run this script with: chmod +x setup_4d_systems.sh && ./setup_4d_systems.sh
#
# =============================================================================

set -e  # Exit on any error

echo "======================================================================"
echo "4D Systems Framework - Mac Studio Setup"
echo "======================================================================"
echo ""
echo "\"Here lies the evolution between beginnings and ends -"
echo " The cycle of to be, is, and has become.\""
echo "                                        - Khoury H"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo -e "${BLUE}[1/6] Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Installing via Homebrew..."
    if ! command -v brew &> /dev/null; then
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install python@3.11
fi

if ! command -v git &> /dev/null; then
    echo "Git not found. Installing via Homebrew..."
    brew install git
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"

# Step 2: Create project directory
echo -e "${BLUE}[2/6] Creating project directory...${NC}"
mkdir -p ~/Projects/NIEA
cd ~/Projects/NIEA

# Step 3: Clone or update repository
echo -e "${BLUE}[3/6] Cloning 4D Systems Framework repository...${NC}"
if [ -d "4D-Systems-Framework" ]; then
    echo "Repository exists, pulling latest changes..."
    cd 4D-Systems-Framework
    git pull
else
    git clone https://github.com/TheNIEA/4D-Systems-Framework.git
    cd 4D-Systems-Framework
fi
echo -e "${GREEN}✓ Repository ready at ~/Projects/NIEA/4D-Systems-Framework${NC}"

# Step 4: Set up Python virtual environment
echo -e "${BLUE}[4/6] Setting up Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Step 5: Install dependencies
echo -e "${BLUE}[5/6] Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install numpy scipy matplotlib
pip install spacy requests textblob
pip install jupyter ipython  # For interactive exploration

# Download spaCy language model
python -m spacy download en_core_web_sm

echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 6: Create launch scripts
echo -e "${BLUE}[6/6] Creating launch scripts...${NC}"

# Create activation script
cat > activate_4d.sh << 'EOF'
#!/bin/bash
# Quick activation script for 4D Systems Framework
cd ~/Projects/NIEA/4D-Systems-Framework
source venv/bin/activate
echo "4D Systems Framework environment activated!"
echo "Run: python implementations/consciousness_4d_framework.py"
EOF
chmod +x activate_4d.sh

# Create run script
cat > run_4d.sh << 'EOF'
#!/bin/bash
# Run the 4D Systems Framework
cd ~/Projects/NIEA/4D-Systems-Framework
source venv/bin/activate
python implementations/consciousness_4d_framework.py
EOF
chmod +x run_4d.sh

# Create interactive Python startup
cat > interactive_4d.py << 'EOF'
"""
4D Systems Framework - Interactive Session
Launch with: python -i interactive_4d.py
"""
import numpy as np
import json
from pathlib import Path

# Load framework schema
with open('framework/4d_systems_framework_schema.json', 'r') as f:
    FRAMEWORK = json.load(f)

# Core functions
def D_node(t, alpha=0.7, beta=0.1, gamma=0.8, delta=0.05):
    """Node Development Function"""
    return alpha * np.exp(-beta * t) + gamma * (1 - np.exp(-delta * t))

def T_opt(t, v_init=0.3, v_max=1.0, r=0.05):
    """Temporal Optimization Function"""
    return v_init + (v_max - v_init) / (1 + np.exp(-r * t))

def M_4D(weights, development, efficiency, temporal):
    """4D Systems Metric"""
    return sum(w * n * (s / 1.0) * t 
               for w, n, s, t in zip(weights, development, efficiency, temporal))

print("4D Systems Framework loaded!")
print("Available: FRAMEWORK, D_node(), T_opt(), M_4D()")
print("Try: D_node(10)  or  FRAMEWORK['nodes']")
EOF

echo -e "${GREEN}✓ Launch scripts created${NC}"

# Print summary
echo ""
echo "======================================================================"
echo -e "${GREEN}✓ SETUP COMPLETE!${NC}"
echo "======================================================================"
echo ""
echo "Your 4D Systems Framework is ready at:"
echo "  ~/Projects/NIEA/4D-Systems-Framework"
echo ""
echo "Quick commands:"
echo "  cd ~/Projects/NIEA/4D-Systems-Framework"
echo "  source venv/bin/activate"
echo "  python implementations/consciousness_4d_framework.py"
echo ""
echo "Or use the helper scripts:"
echo "  ./activate_4d.sh  - Activate the environment"
echo "  ./run_4d.sh       - Run the framework"
echo ""
echo "For interactive exploration:"
echo "  python -i interactive_4d.py"
echo ""
echo "Repository structure:"
echo "  framework/       - Theoretical foundations (JSON schemas)"
echo "  implementations/ - Executable Python code"
echo "  docs/            - PDFs and LaTeX documentation"
echo "  assets/          - Visual diagrams"
echo ""
echo "======================================================================"
echo "\"This is now. This is time. This is the technology of becoming.\""
echo "======================================================================"
