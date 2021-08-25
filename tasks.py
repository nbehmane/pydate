from invoke import task
from invoke.watchers import Responder

@task
def run_update(c):
    responder = Responder(
            pattern=r"Do you want to continue\? \[Y\/n\] ",
            response = "\n",
            )
    c.run("apt-get upgrade", watchers=[responder])
