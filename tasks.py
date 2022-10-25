import shlex
import sys

from invoke import task  # pyright: reportMissingModuleSource=false


@task
def install_deps(c):
    "Install the python dependencies"
    c.run("poetry install", pty=True)


@task
def setup_repository(c):
    "Setup pre-commit hooks. Only needs to be done once per git checkout"
    c.run("pre-commit install", pty=True)


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


@task
def failfast(c):
    "Run the tests"
    run_with_passthrough(c, "pytest-watch -c -- -x", pty=True)


@task
def lint(c):
    "lint with flake8"
    c.run(
        "flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics",
        pty=True,
    )


@task
def coverage(c):
    "See code coverage estimations"
    c.run("python -m pytest --cov=ms", pty=True)


@task
def start(c):
    c.run("FLASK_ENV=development flask run", pty=True)


@task
def staging(c):
    c.run("git checkout staging && git merge main && git push && git checkout main")


@task
def docs(c):
    c.run(f"echo {20*'-'}")
    c.run("echo 'when happy do mkdocs gh-deploy'")
    c.run("mkdocs serve")
    c.run(f"echo {20*'-'}")
    c.run("echo 'when happy do mkdocs gh-deploy'")


#####################################################################
# Helper functions


def run_with_passthrough(c, cmd, *args, **kwargs):
    return c.run(" ".join([cmd, passthrough_args()]), *args, **kwargs)


def passthrough_args() -> str:
    try:
        dashdash_position = sys.argv.index("--")
    except ValueError:
        return ""
    return " ".join(map(shlex.quote, sys.argv[dashdash_position + 1 :]))
