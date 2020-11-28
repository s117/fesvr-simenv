#!/usr/bin/env python3
import os
import pathlib
import shlex
import sys
from typing import Dict, Optional, List

import bashlex
import click
import yaml
from bashlex.errors import ParsingError

from SyscallAnalysis.libsyscall.analyzer.file_usage import stat_file_usage
from SyscallAnalysis.libsyscall.analyzer.syscall_trace_constructor import SyscallTraceConstructor

from .libsimenv.manifest_db import save_to_manifest_db
from .libsimenv.stdin_file_extractor import extract_stdin_file_from_shcmd
from .libsimenv.app_manifest import build_manifest
from .libsimenv.utils import fatal, warning


@click.command()
@click.pass_context
@click.option("-n", "--app-name", required=True, help="The app name.")
@click.option("-c", "--app-cmd-file", required=True,
              type=click.File(),
              help="A single-line text file that contains the command to run this app.")
@click.option("-w", "--app-init-cwd", required=True,
              help="The CWD where you started this app. Use the target path, not host path.")
@click.option("-m", "--memsize", required=True,
              type=click.INT,
              help="The amount of RAM this app needs.")
@click.option("-s", "--strace", required=True,
              type=click.File(),
              help="The FESVR syscall trace file.")
@click.option("-i", "--pristine-sysroot", required=True,
              type=click.Path(exists=True, dir_okay=True, file_okay=False),
              help="The path to a pristine sysroot including all the files the app needs.")
@click.option("-o", "--post-sim-sysroot", required=True,
              type=click.Path(exists=True, dir_okay=True, file_okay=False),
              help="The path to the sysroot after the app has run.")
@click.option("--copy-spawn", is_flag=True,
              help="When spawning this simenv, copying all it's input instead of making symbolic link.")
def main(ctx, app_name, app_cmd_file, app_init_cwd, memsize, strace, pristine_sysroot, post_sim_sysroot, copy_spawn):
    """
    Create a new simenv by learning the syscall trace, then add it to the database, so that it can be spawn later.
    """
    print("Generating manifest for app %s" % app_name)
    app_cmd = app_cmd_file.read().strip()

    try:
        stdin_files = extract_stdin_file_from_shcmd(app_cmd)
    except ParsingError as ex:
        warning("Fail to parse app cmd to analyze additional input file given by stdin redirect: %s" % ex)
        stdin_files = []
    else:
        if stdin_files:
            for f in stdin_files:
                if pathlib.PurePosixPath(f).is_absolute():
                    warning("The app command used absolute path to indicates stdin redirect, which is not supported")
            print("Recognized following file(s) passed as the input via stdin from the app run command [%s]" % app_cmd)
            for f in stdin_files:
                print("   - %s" % f)

    trace_analyzer = SyscallTraceConstructor(app_init_cwd)
    strace_str = strace.read()
    trace_analyzer.parse_strace_str(strace_str)

    file_usage_info = stat_file_usage(trace_analyzer.syscalls)
    manifest = build_manifest(app_name, app_cmd, app_init_cwd, memsize, pristine_sysroot, post_sim_sysroot,
                              file_usage_info,
                              stdin_files,
                              copy_spawn)

    save_to_manifest_db(app_name, manifest, db_path=ctx.obj['manifest_db_path'])
    print("Done.")


if __name__ == '__main__':
    main()
