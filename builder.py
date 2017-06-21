import sys
import click
import os
import shutil
import subprocess
from packageinfo import BUILD, VERSION, NAME


def bootstrap_common():
    if not os.path.exists("buildrecipes-common"):
        subprocess.check_call([
            "git", "clone",
            "http://github.com/simphony/buildrecipes-common.git",
            ])
    sys.path.insert(0, "buildrecipes-common")

bootstrap_common()
import common

workspace = common.workspace()
common.edmenv_setup()
clone_dir = "PyFoam-{VERSION}".format(VERSION=VERSION)


@click.group()
def cli():
    pass


@cli.command()
def egg():
    _clean()
    common.run("wget https://openfoamwiki.net/images/3/3b/PyFoam-"+VERSION+".tar.gz --no-check-certificate")
    common.run("tar -xzf PyFoam-"+VERSION+".tar.gz")
    shutil.copy(
        os.path.join("files", "setup.py"),
        os.path.join("PyFoam-0.6.4", "setup.py")
        )
    os.makedirs("dist")

    with common.cd(clone_dir):
        common.edmenv_run("python setup.py bdist_egg")

    shutil.copy(
        os.path.join(clone_dir, "dist", "{NAME}-{VERSION}-py2.7.egg".format(
        NAME=NAME, VERSION=VERSION)),
        "dist")
    common.run("edm repack-egg -b {BUILD} dist/{NAME}-{VERSION}-py2.7.egg".format(
        NAME=NAME, VERSION=VERSION, BUILD=BUILD))


@cli.command()
def upload_egg():
    egg_path = "dist/{NAME}-{VERSION}-{BUILD}.egg".format(
        NAME=NAME,
        VERSION=VERSION,
        BUILD=BUILD)
    click.echo("Uploading {} to EDM repo".format(egg_path))
    common.upload_egg(egg_path)
    click.echo("Done")


@cli.command()
def clean():
    _clean()

def _clean():
    click.echo("Cleaning")
    common.clean(["dist", clone_dir, "buildrecipes-common", "PyFoam-0.6.4.tar.gz", "PyFoam-0.6.4"])


cli()
