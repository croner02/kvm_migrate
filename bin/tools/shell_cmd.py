from bin.log import logger
import subprocess
import sys
import select
import os
from config import config
from collections import defaultdict



def get_exception():

    return sys.exc_info()[1]


def run(args, cwd=None, use_safe_shell=False):
    env = os.environ
    if isinstance(args, list) and use_safe_shell:
        args = " ".join(x for x in args)
        shell = True
    elif isinstance(args, basestring) and use_safe_shell:
        shell = True
    elif isinstance(args, basestring):
        shell = True
    else:
        logger.error("Argument 'args' to run_command must be list or string")
        raise Exception("Argument 'args' to run_command must be list or string")

    kwargs = dict(
        shell=shell,
        preexec_fn=os.setsid,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    if cwd and os.path.isdir(cwd):
        kwargs["cwd"] = cwd

    try:
        cmd = subprocess.Popen(args, **kwargs)
        logger.debug("%s exec successfully" % args)
        global rc, stdout, stderr
        stdout = ''
        stderr = ''
        rpipes = [cmd.stdout, cmd.stderr]
        while True:
            rfd, wfd, efd = select.select(rpipes, [], rpipes, 1)
            if cmd.stdout in rfd:
                dat = os.read(cmd.stdout.fileno(), 9000)
                stdout += dat
                if not dat:
                    rpipes.remove(cmd.stdout)
            if cmd.stderr in rfd:
                dat = os.read(cmd.stderr.fileno(), 9000)
                stderr += dat
                if not dat:
                    rpipes.remove(cmd.stderr)
            if (not rpipes or not rfd) and cmd.poll() is not None:
                break
            elif not rpipes and cmd.poll() is None:
                cmd.wait()
                break
        cmd.stdout.close()
        cmd.stderr.close()
        rc = cmd.returncode
    except (OSError, IOError):
        get_exception()
    return rc, stdout, stderr


def shell_run(args, host=None, exec_mode='localhost', cwd=None, use_safe_shell=False):
    result = defaultdict(list)
    if exec_mode == 'remote':
        args = "sshpass -p %s ssh -p %s %s@%s %s" % (config.USER_INFO["password"],
                                                     config.USER_INFO["port"],
                                                     config.USER_INFO["user"],
                                                     host, args)
    elif exec_mode == "localhost":
        args = args
    else:
        logger.error("Argument 'exec_mode' must be 'localhost'or 'remote'")
        raise Exception("Argument 'exec_mode' must be 'localhost'or 'remote'")
    re_rc, re_stdout, re_stderr = run(args, cwd=cwd, use_safe_shell=use_safe_shell)
    result["stdout"] = {host: re_stdout}
    result["stderr"] = {host: re_stderr}
    return result
