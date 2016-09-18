#!/usr/bin/python
from conan.packager import ConanMultiPackager
import platform, os

if __name__ == "__main__":
    mingw_configurations = [("4.9", "x86_64", "seh", "posix"),
                            ("4.9", "x86_64", "sjlj", "posix"),
                            ("4.9", "x86", "sjlj", "posix"),
                            ("4.9", "x86", "dwarf2", "posix")]
    builder = ConanMultiPackager(username='lucteo', mingw_configurations=mingw_configurations, visual_runtimes=["MT", "MD"])

    if platform.system() == "Windows":
        builder.add_common_builds(visual_versions=[12, 13])

    if platform.system() == "Linux":
        for ver in (filter(None,
                           os.getenv("CONAN_GCC_VERSIONS", "").split(","))
                    or ["4.8", "4.9", "5.2", "5.3"]):
            for arch in ["x86", "x86_64"]:
                builder.add({"arch": arch,
                             "build_type": "Release",
                             "compiler": "gcc",
                             "compiler.version": ver}, {})

    if platform.system() == "Darwin":
        for ver in (filter(None,
                           os.getenv("CONAN_APPLE_CLANG_VERSIONS_VERSIONS", "").split(","))
                    or ["6.0", "6.1", "7.0", "7.3", "8.0"]):
            for arch in ["x86", "x86_64"]:
                builder.add({"arch": arch,
                             "build_type": "Release",
                             "compiler": "apple-clang",
                             "compiler.version": ver}, {})
    builder.run()
