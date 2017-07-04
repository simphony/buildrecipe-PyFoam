# Basic template for edm setup.
# Copy this file to retrieve the buildcommons repository
# This template can be used as is on trivial "setup.py only"
# packages.
# It requires the additional files:
# - a packageinfo.py containing the relevant data.
# - an endist.dat file, containing the relevant data.
import sys
import click
import os
import subprocess
import shutil

from packageinfo import BUILD, VERSION, NAME

# The version of the buildcommon to checkout.
BUILDCOMMONS_VERSION="v0.2"


def bootstrap_devenv():
    try:
        os.makedirs(".devenv")
    except OSError:
        pass

    if not os.path.exists(".devenv/buildrecipes-common"):
        subprocess.check_call([
            "git", "clone", "-b", BUILDCOMMONS_VERSION,
            "http://github.com/simphony/buildrecipes-common.git",
            ".devenv/buildrecipes-common"
            ])
    sys.path.insert(0, ".devenv/buildrecipes-common")


bootstrap_devenv()
import buildcommons as common  # noqa

workspace = common.workspace()
common.edmenv_setup()
clone_dir = "PyFoam-{VERSION}".format(VERSION=VERSION)


@click.group()
def cli():
    pass


@cli.command()
def egg():
    if not os.path.exists("PyFoam-{}.tar.gz".format(VERSION)):
        common.run("wget https://openfoamwiki.net/images/3/3b/PyFoam-"+VERSION+".tar.gz --no-check-certificate")

    common.run("tar -xzf PyFoam-"+VERSION+".tar.gz")

    shutil.copy(
        os.path.join("files", "setup.py"),
        os.path.join(clone_dir, "setup.py")
        )

    with common.cd(clone_dir):
        common.local_repo_to_edm_egg(".", name=NAME, version=VERSION, build=BUILD)


@cli.command()
def upload_egg():
    egg_path = os.path.join(clone_dir, "endist", "{NAME}-{VERSION}-{BUILD}.egg".format(
        NAME=NAME,
        VERSION=VERSION,
        BUILD=BUILD))
    click.echo("Uploading {} to EDM repo".format(egg_path))
    common.upload_egg(egg_path)
    click.echo("Done")


@cli.command()
def clean():
    click.echo("Cleaning")
    common.clean(["endist", ".devenv", clone_dir, "PyFoam-0.6.4.tar.gz", "PyFoam-0.6.4"])


cli()
