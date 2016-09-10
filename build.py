#!/usr/bin/python
from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    mingw_configurations = [("4.9", "x86_64", "seh", "posix"),
                            ("4.9", "x86_64", "sjlj", "posix"),
                            ("4.9", "x86", "sjlj", "posix"),
                            ("4.9", "x86", "dwarf2", "posix")]
    builder = ConanMultiPackager(username='lucteo', mingw_configurations=mingw_configurations)
    builder.add_common_builds()
    builder.run()
