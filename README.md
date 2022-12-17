## SimEnv
A toolset to reliably pack and spawn RISC-V workloads for riscv-fesvr.

A workload will be packed into a `simenv`, which is basically the rootfs containing all the essentials for a simulation. The tool learns what files are required by analyzing the workload's syscall trace.

When simulating using `simenv` and proper [PK](https://github.com/s117/riscv-pk/tree/toolchain_update_gcc920) + [FESVR](https://github.com/s117/riscv-fesvr/tree/toolchain_update_gcc920), the noise introduced by the infrastructure is greatly controlled.

Run `app-repo --help` to learn how to create an app repository.

```shell
$ app-repo --help
Usage: app-repo [OPTIONS] COMMAND [ARGS]...

  The app repository management utility

Options:
  --help  Show this message and exit.

Commands:
  addckpt     Import checkpoint.
  addsysroot  Import a pristine sysroot.
  init        Create an empty app repository.
  learn       Analyze an app for how to create SimEnv.
  subrepo     Spawn a sub-repository with the selected apps.
```

Run`simenv --help` to learn how to use an app repository.

```shell
$ simenv --help  
Usage: simenv [OPTIONS] COMMAND [ARGS]...

  The simenv utility

Options:
  --repo-path DIRECTORY  Override the SimEnv repository path given by the
                         environmental variable "SIMENV_REPO_PATH".
  --help                 Show this message and exit.

Commands:
  list    List available apps and checkpoints in the SimEnv repository.
  mkgen   Generate a Makefile for a simenv, at current dir.
  spawn   Spawn a simenv.
  verify  Perform integrity checking for a simenv.
```

If your shell are bash/zsh/fish and would like to have auto-completion, run the below in your shell:
```shell
# Enable auto-completion for the 'simenv' command
eval "$(_SIMENV_COMPLETE=$(basename $SHELL)_source simenv)"

# Enable auto-completion for the 'app-repo' command 
eval "$(_APP_REPO_COMPLETE=$(basename $SHELL)_source app-repo)"
```
