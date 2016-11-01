#!/usr/bin/env python
# Copyright (C) 2016 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - https://cuckoosandbox.org/.
# See the file 'docs/LICENSE' for copying permission.

import os
import setuptools
import sys

# Update the MANIFEST.in file to include the one monitor version that is
# actively shipped for this distribution and exclude all the other monitors
# that we have lying around. Note: I tried to do this is in a better manner
# through exclude_package_data, but without much luck.

excl, monitor = [], os.path.join("cuckoo", "data", "monitor")
latest = open(os.path.join(monitor, "latest"), "rb").read().strip()
for h in os.listdir(monitor):
    if h != "latest" and h != latest:
        excl.append(
            "recursive-exclude cuckoo/data/monitor/%s *  # AUTOGENERATED" % h
        )

if not os.path.isdir(os.path.join(monitor, latest)) and \
        not os.environ.get("ONLYINSTALL"):
    sys.exit(
        "Failure locating the monitoring binaries that belong to the latest "
        "monitor release. Please include those to create a distribution."
    )

manifest = []
for line in open("MANIFEST.in", "rb"):
    if not line.strip() or "# AUTOGENERATED" in line:
        continue

    manifest.append(line.strip())

manifest.extend(excl)

open("MANIFEST.in", "wb").write("\n".join(manifest) + "\n")

def githash():
    """Extracts the current Git hash."""
    git_head = os.path.join(".git", "HEAD")
    if os.path.exists(git_head):
        head = open(git_head, "rb").read().strip()
        if not head.startswith("ref: "):
            return head

        git_ref = os.path.join(".git", head.split()[1])
        if os.path.exists(git_ref):
            return open(git_ref, "rb").read().strip()

cwd_path = os.path.join("cuckoo", "data-private", ".cwd")
open(cwd_path, "wb").write(githash() or "")

setuptools.setup(
    name="Cuckoo",
    version="2.0.0",
    author="Stichting Cuckoo Foundation",
    author_email="cuckoo@cuckoofoundation.org",
    packages=[
        "cuckoo",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        # TODO: should become stable.
        # "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Flask",
        "Framework :: Pytest",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: Security",
    ],
    url="https://cuckoosandbox.org/",
    license="GPLv3",
    description="Automated Malware Analysis System",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "cuckoo = cuckoo.main:main",
        ],
    },
    install_requires=[
        "alembic==0.8.0",
        "androguard==3.0",
        "beautifulsoup4==4.4.1",
        "chardet==2.3.0",
        "click==6.6",
        "Django==1.8.4",
        "django_extensions==1.6.7",
        "dpkt==1.8.7",
        "Flask==0.10.1",
        "HTTPReplay==0.1.17",
        "jsbeautifier==1.6.2",
        "lxml==3.6.0",
        "oletools==0.42",
        "peepdf==0.3.2",
        "pefile2==1.2.11",
        "Pillow==3.2",
        "pymisp==2.4.50",
        "pymongo==3.0.3",
        "python-dateutil==2.4.2",
        "python-magic==0.4.12",
        "sflock==0.2.2",
        "SQLAlchemy==1.0.8",
        "wakeonlan==0.2.2",
    ],
    extras_require={
        ":sys_platform == 'win32'": [
            "requests==2.7.0",
        ],
        ":sys_platform == 'darwin'": [
            "requests==2.7.0",
        ],
        ":sys_platform == 'linux2'": [
            "requests[security]==2.7.0",
            "scapy==2.3.2",
        ],
        "distributed": [
            "flask-sqlalchemy==2.1",
            "gevent==1.1.1",
            "psycopg2==2.6.2",
        ],
        "postgresql": [
            "psycopg2==2.6.2",
        ],
    },
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=[
        "coveralls",
        "pytest",
        "pytest-cov",
        "responses==0.5.1",
        "flask-sqlalchemy==2.1",
    ],
)
