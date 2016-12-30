#!/usr/bin/python
from conan.packager import ConanMultiPackager
import platform, os

if __name__ == "__main__":
    builder = ConanMultiPackager(username='lucteo')

    builder.add_common_builds()

    # Keep only Release builds
    filtered_builds = []
    for settings, options in builder.builds:
        if settings["build_type"] == "Release":
             filtered_builds.append([settings, options])
    builder.builds = filtered_builds

    builder.run()
