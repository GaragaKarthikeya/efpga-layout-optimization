#!/bin/bash
# Test script to verify VTR setup is working correctly
# This runs a simple benchmark to ensure VTR is properly installed and configured

set -e  # Exit on any error

echo "========================================="
echo "VTR Setup Verification Test"
echo "========================================="
echo ""

# Check if VTR directory exists
if [ ! -d "$HOME/vtr-verilog-to-routing" ]; then
    echo "ERROR: VTR directory not found at ~/vtr-verilog-to-routing"
    echo "Please install VTR first (see docs/setup_guide.md)"
    exit 1
fi

# Check if venv exists
if [ ! -d "$HOME/vtr-verilog-to-routing/venv" ]; then
    echo "ERROR: Python venv not found at ~/vtr-verilog-to-routing/venv"
    echo "Please create venv (see docs/setup_guide.md)"
    exit 1
fi

echo "✓ VTR directory found"
echo "✓ Python venv found"
echo ""

# Activate venv
echo "Activating Python virtual environment..."
cd ~/vtr-verilog-to-routing
source venv/bin/activate

# Test VPR version
echo ""
echo "Testing VPR binary..."
./build/vpr/vpr --version | head -5
echo ""

# Run a quick VTR flow test
echo "Running quick VTR flow test (diffeq1 benchmark)..."
echo "This will take 1-2 seconds..."
echo ""

./vtr_flow/scripts/run_vtr_flow.py \
    ~/vtr-verilog-to-routing/vtr_flow/benchmarks/verilog/diffeq1.v \
    ~/vtr-verilog-to-routing/vtr_flow/arch/timing/EArch.xml \
    --route_chan_width 100 2>&1 | tail -5

echo ""
echo "========================================="
echo "✓ VTR setup is working correctly!"
echo "========================================="
echo ""
echo "You can now run VTR experiments."
echo "Remember to activate the venv first: vtr-activate"
echo ""
