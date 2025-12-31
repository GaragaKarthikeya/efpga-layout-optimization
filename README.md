# eFPGA Layout Optimization

Undergrad research project - figuring out FPGA stuff with VTR.

**Us:** Karthikeya & Lohith (2nd year, IIIT Bangalore)  
**Prof:** Madhav Rao  
**Started:** Dec 2024

## What is this?

Prof gave us a paper called GOLDS about optimizing FPGA layouts. Our job:
1. Figure out what VTR is and how to use it
2. Try to reproduce the paper's results
3. Learn as we go


## Quick Links

- [What we need to do](TODO.md)
- [Our notes](notes/)
- [Meeting notes](docs/meetings/)

## Folder Structure

```
papers/         → PDFs we're reading
notes/          → Our notes & learnings  
vtr-experiments/→ When we actually run stuff
docs/meetings/  → Meeting notes with prof
```

## VTR Setup (for ourselves)

```bash
# Install stuff
sudo apt install build-essential cmake python3 libcairo2-dev

# Get VTR v9.0.0 (stable release, Jan 2025)
wget https://github.com/verilog-to-routing/vtr-verilog-to-routing/releases/download/v9.0.0/vtr-verilog-to-routing-9.0.0.tar.gz
tar -xzf vtr-verilog-to-routing-9.0.0.tar.gz
cd vtr-verilog-to-routing-9.0.0
make -j4

# Check if it works
./vtr_flow/scripts/run_vtr_flow.py -h
```



## Useful Links

- [VTR Docs](https://docs.verilogtorouting.org/) - main documentation
- [VTR Tutorials](https://docs.verilogtorouting.org/en/latest/tutorials/) - start here
