## atool-simenv
A new toolset to reliably packing, then spawning a RISC-V workload (app) for any simulation purpose.

An app is packed into a `simenv`, which is basically the rootfs containing all the essentials for a simulation. The tool learns what are the essentials by analyzing the workload's syscall trace. When simulating with the proper PK/FESVR, the dynamic instruction stream is even reproducible.  

The motivation is to help Dr. Rotenberg's microarchitecture research group and ECE721 students using SPEC CPU2006 and CPU2017 workloads (usually checkpointed workloads) with ease.

At the time, run `atool-simenv --help` to see how to use it (docs are incoming). 
  
```
Usage: atool-simenv [OPTIONS] COMMAND [ARGS]...

  The simenv utility

Options:
  --db-path DIRECTORY             Override the manifest directory path.
  --checkpoints-archive-path DIRECTORY
                                  Override the checkpoint archive directory
                                  path.

  --help                          Show this message and exit.

Commands:
  learn   Create a new simenv by learning the syscall trace.
  list    List the simenv for available apps and checkpoints.
  mkgen   Generate a Makefile for a simenv, at current dir.
  spawn   Spawn a simenv.
  verify  Perform integrity checking for a simenv.
```

\* If you are using bash/zsh/fish, you can run `eval "$(_ATOOL_SIMENV_COMPLETE=source_$(basename $SHELL) atool-simenv)"` to enable the auto completion for atool-simenv.

## Misc.

- `SpecResultVerification/spike_trim.py` - Trim out the extra header/tail message produced by spike or pk during the simulation. Useful if you want to automatically verify the STDOUT output of a SPEC simulation.
- `Checkpointing/ChkptDescFileGen/smpt2ckptdesc.py` - Convert the Simpoint output file to the checkpoint job description file accepted by Spike.
- `Checkpointing/DumpHTIF/chkpt_htif_dump.py` - Show the HTIF syscalls recorded in a checkpoint file. When restoring a checkpoint, those syscalls will be executed in sequence to bring back the state of [HTIF FESVR](https://github.com/s117/riscv-fesvr).
- `TetherSim/SimTetheringController.py` - Controller for [721sims](https://github.ncsu.edu/jli95/721sim/tree/trace_support) working in tethering mode.


## To work with trace dump

- `CpuTraceAnalysis/trace2google.py` - Analyze the trace dumped by [spike](https://github.com/s117/riscv-isa-sim/tree/WIB_trace_support) or [721sim](https://github.ncsu.edu/jli95/721sim/tree/trace_support) and output the result in Google's Trace Event Format.
- To visualize the result, use [speedscope](https://github.com/jlfwong/speedscope) (recommend) or Chromium's *about://tracing* .
  - if `ignore_symbol.yaml` exists in CWD, it will be read to filter out the defined function calls. See `CpuTraceAnalysis/ignore_symbol.yaml` for an example.

- `CpuTraceAnalysis/trace2tracevis.py` - Analyze and visualize the trace dumped by [spike](https://github.com/s117/riscv-isa-sim/tree/WIB_trace_support) or [721sim](https://github.ncsu.edu/jli95/721sim/tree/trace_support) in a homebrew timeline frontend (using [timeline-js](https://github.com/visjs/vis-timeline)).
  - if `ignore_symbol.yaml` exists in CWD - Will be read to filter out the defined function calls. See `CpuTraceAnalysis/ignore_symbol.yaml` for an example.
  - **It's recommended to use `trace2google.py`.** Because the trace_vis frontend uses timeline-js, which is not intended for visualizing tracing result, it can be very slow and unresponsive when working with trace with a large amount of event.

![image-20201105011703029](https://raw.githubusercontent.com/s117/anycore-dbg-supplement/master/README.assets/image-20201105011703029.png)

<p align=center>Viewing the trace2google.py output with speedscope</p>

![image-20201105011839379](https://raw.githubusercontent.com/s117/anycore-dbg-supplement/master/README.assets/image-20201105011839379.png)

<p align=center>Viewing the trace2google.py output with Chrome's about:tracing</p>

![image-20200813043919822](https://raw.githubusercontent.com/s117/anycore-dbg-supplement/master/README.assets/image-20200813043919822.png)

<p align=center>Viewing the trace using homebrew TraceVis frontend (use timeline-js)</p>

**WIP**.