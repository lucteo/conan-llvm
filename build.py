#!/usr/bin/python
from conan.packager import ConanMultiPackager
import platform, os

if __name__ == "__main__":
    builder = ConanMultiPackager(username='lucteo')

    visual_versions = [12, 14]
    builder.add_common_builds(visual_versions=visual_versions)

    # Keep only Release builds
    filtered_builds = []
    for settings, options in builder.builds:
        if settings["build_type"] == "Release":
             filtered_builds.append([settings, options])
    builder.builds = filtered_builds

    builder.run()
