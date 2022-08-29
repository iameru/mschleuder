import shlex
import sys

from invoke import task  # pyright: reportMissingModuleSource=false


@task
def install_deps(c):
    "Install the python dependencies"
    c.run("poetry install")


@task
def setup_repository(c):
    "Setup pre-commit hooks. Only needs to be done once per git checkout"
    c.run("pre-commit install")


@task
def test_reset(c):
    """
    Clear caches and everything.

    Shouldn't usually be necessary, try this if tdd is weird
    """
    c.run("rm -rf .pytest_cache .testmondata", echo="both")


@task
def test(c):
    "Run the tests"
    run_with_passthrough(c, "pytest-watch -c", pty=True)
    # run_with_passthrough(c, "pytest", pty=True)


@task
def start(c):
    c.run("FLASK_ENV=development flask run")


#####################################################################
## Helper functions


def run_with_passthrough(c, cmd, *args, **kwargs):
    return c.run(" ".join([cmd, passthrough_args()]), *args, **kwargs)


def passthrough_args() -> str:
    try:
        dashdash_position = sys.argv.index("--")
    except ValueError:
        return ""
    return " ".join(map(shlex.quote, sys.argv[dashdash_position + 1 :]))
