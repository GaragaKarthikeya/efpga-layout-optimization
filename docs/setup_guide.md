# How to Install VTR

## Ubuntu Instructions


```bash
# Step 1: Install ALL dependencies at once
sudo apt update
sudo apt install -y build-essential cmake python3 python3-pip python3-venv \
    libcairo2-dev libfontconfig1-dev libreadline-dev tcl-dev libffi-dev \
    bison flex libgtk-3-dev libx11-dev libeigen3-dev libtbb-dev

# Step 2: Download VTR (pick ONE option)

# Option A: Get stable release v9.0.0 (recommended, less issues)
cd ~
wget https://github.com/verilog-to-routing/vtr-verilog-to-routing/releases/download/v9.0.0/vtr-verilog-to-routing-9.0.0.tar.gz
tar -xzf vtr-verilog-to-routing-9.0.0.tar.gz
cd vtr-verilog-to-routing-9.0.0

# Option B: OR get latest git version (what Karthikeya used)
# cd ~
# git clone https://github.com/verilog-to-routing/vtr-verilog-to-routing.git
# cd vtr-verilog-to-routing

# Step 3: Build (change -j4 to match your CPU cores, check with: nproc)
make -j4

# Step 4: Create Python venv for VTR scripts
python3 -m venv venv
source venv/bin/activate
pip install prettytable

# Step 5: TEST IT
./vpr/vpr --version
./vpr/vpr vtr_flow/arch/timing/EArch.xml vtr_flow/benchmarks/blif/tseng.blif --route_chan_width 100
```

If that last command runs and says "VPR succeeded" - you're done! 🎉

---

## Common Ubuntu Issues

### "tcl.h not found" or "readline.h not found"
```bash
sudo apt install tcl-dev libreadline-dev
```

### "ffi.h not found"
```bash
sudo apt install libffi-dev
```

### Build runs out of memory
```bash
make -j2   # use fewer cores
```

### "No module named prettytable"
```bash
source ~/vtr-verilog-to-routing/venv/bin/activate  # or wherever you installed
pip install prettytable
```

---

## Our Setups

### Karthikeya ✅ DONE
- **OS:** Fedora 43
- **VTR version:** 9.0.0-dev from git (commit 8cb20aa52)
- **VTR location:** `~/vtr-verilog-to-routing/`
- **Python venv:** `~/vtr-verilog-to-routing/venv/`
- **Issues faced:**
  - Fedora uses Clang 21 which is too new
  - Had to manually add `#include <cstdint>` to `yosys/libs/json11/json11.cpp`
  - Needed to install: `tcl-devel`, `readline-devel`, `libffi-devel`
  - Build took ~20 mins on Ryzen 7 7735HS with `-j16`
- **Test result:** tseng benchmark runs at 152 MHz, routing succeeds in 12 iterations

### Lohith
- **OS:** Ubuntu
- **VTR version:** 
- **VTR location:**
- **Issues faced:**

---

## After Installing

### Add Convenient Aliases (Recommended)

Add these to your `~/.bashrc` for easier VTR usage:
```bash
export PATH="/home/karthikeya/vtr-verilog-to-routing/vtr_flow/scripts:$PATH"
alias vtr-activate='source ~/vtr-verilog-to-routing/venv/bin/activate'
```

Then reload: `source ~/.bashrc`

**Note**: If you installed VTR following this guide after Dec 13, 2024, these are already configured!

### Test Your Installation

**Option 1 - Automated test (easiest)**:
```bash
cd ~/efpga-layout-optimization
./vtr-experiments/test_setup.sh
```

**Option 2 - Manual VPR test**:
```bash
cd ~/vtr-verilog-to-routing
./build/vpr/vpr vtr_flow/arch/timing/EArch.xml vtr_flow/benchmarks/blif/tseng.blif --route_chan_width 100
```

**Option 3 - Full VTR flow test** (Verilog → BLIF → Place → Route):
```bash
vtr-activate  # or: source ~/vtr-verilog-to-routing/venv/bin/activate
cd ~/vtr-verilog-to-routing
./vtr_flow/scripts/run_vtr_flow.py \
    ~/vtr-verilog-to-routing/vtr_flow/benchmarks/verilog/diffeq1.v \
    ~/vtr-verilog-to-routing/vtr_flow/arch/timing/EArch.xml \
    --route_chan_width 100
```

You should see it pack → place → route → "VPR succeeded" (or "OK" for full VTR flow)

### Important Notes

- **tseng benchmark**: Only available as `.blif` file, not Verilog. Use `diffeq1.v` for Verilog tests.
- **Always activate venv** before running `run_vtr_flow.py` scripts (use `vtr-activate` alias)
- **VPR vs VTR**: VPR only works with BLIF files. Use full VTR flow for Verilog files.
