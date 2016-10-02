"""
Print status of all clawpack git repositories.
"""

from __future__ import print_function

import os
import sys
import time
import subprocess
import StringIO

repos_list = ['classic', 'amrclaw', 'clawutil', 'pyclaw', 'visclaw', 'riemann',
              'geoclaw']

def make_git_status_file(outdir=os.getcwd()):
    """
    Print status of all clawpack git repositories.
    Creates 2 files:
         outdir + '/claw_git_status.txt'
            contains list of last commits, what branch is checked out, and
            a short version of git status.
         outdir + '/claw_git_diffs.txt'
            contains all diffs between current working state and last commits.
        
    """

    if not os.environ.has_key('CLAW'):
        raise ValueError("*** CLAW environment variable not set ***")

    outdir = os.path.abspath(outdir)
    status_file_path = os.path.join(outdir, "claw_git_status.txt")
    diff_file_path = os.path.join(outdir, 'claw_git_diffs.txt')

    with open(status_file_path, 'w') as status_file:

        status_file.write("Clawpack Git Status \n")
        status_file.write("Diffs can be found in %s\n\n" % diff_file_path)
        status_file.write(time.strftime("%a, %d %b %Y %H:%M:%S %Z\n"))
        # status_file.write(time.strftime("%c\n"))
        status_file.write("$CLAW = %s\n" % os.environ["CLAW"])
        status_file.write("$FC = %s\n" % os.environ.get("FC", "not set"))

        for repos in repos_list:
            status_file.write(repository_status(repos))

    with open(diff_file_path, 'w') as diff_file:
        diff_file.write("Clawpack git diffs...")
        for repos in repos_list:
            diff_file.write(repository_diff(repos))


def repository_status(repository):
    r"""Return string representation of git status of *repository*

    Uses a series of system command line calls to do so but does not change
    the current working directory to avoid ending up some place we do not want
    to be.

    :Input:
     - *repository* (str) - Name of clawpack repository whose status is needed.

    :Output:
     - (str) - String with status output

    """


    # Query the repository for needed info
    repo_path = os.path.expandvars(os.path.join("$CLAW", repository.lower()))
    
    # Construct output string
    output = StringIO.StringIO()
    output.write("\n\n===========\n%s\n===========\n" % repository)
    output.write("%s\n\n" % repo_path)

    output.write("--- last commit ---\n")
    cmd = "cd %s ; git log -1 --oneline" % repo_path
    output.write(str(subprocess.check_output(cmd, shell=True)))
    output.write("\n")

    output.write("--- branch and status ---\n")
    cmd = "cd %s ; git status -b -s --untracked-files=no" % repo_path
    output.write(str(subprocess.check_output(cmd, shell=True)))
 
    output_str = output.getvalue()
    output.close()

    return output_str
    

def repository_diff(repository):
    r""""""

    # Query the repository for needed info
    repo_path = os.path.expandvars(os.path.join("$CLAW", repository.lower()))
    
    # Construct output string
    output = StringIO.StringIO()
    output.write("\n\n===========\n%s\n===========\n" % repository)
    output.write("%s\n\n" % repo_path)
    cmd = 'cd %s ; git diff --no-ext-diff' % repo_path
    output.write(subprocess.check_output(cmd, shell=True))
    cmd = 'cd %s ; git diff --cached --no-ext-diff' % repo_path
    output.write(subprocess.check_output(cmd, shell=True))
 
    output_str = output.getvalue()
    output.close()

    return output_str



if __name__=="__main__":
    path = os.getcwd()
    if len(sys.argv[1]) > 1:
        path = os.path.abspath(sys.argv[1])
    make_git_status_file(path)
