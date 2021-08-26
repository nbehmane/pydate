from invoke import task
from invoke.watchers import Responder

@task
def run_ubuntu_update(c):
    responder = Responder(
            pattern=r"Do you want to continue\? \[Y\/n\] ",
            response = "y\n",
            )
    c.run("apt-get upgrade --with-new-pkgs 2>&1 | tee -a upgrade_log", watchers=[responder])
