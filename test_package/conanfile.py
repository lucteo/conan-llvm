from conans import ConanFile, CMake
import os

############### CONFIGURE THESE VALUES ##################
default_user = "lucteo"
default_channel = "testing"
#########################################################

channel = os.getenv("CONAN_CHANNEL", default_channel)
username = os.getenv("CONAN_USERNAME", default_user)

class TestLlvmConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "llvm/3.9.1@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.output.info("Running CMake")
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.output.info("Building the llvm test project")
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")
        self.copy(pattern="*", dst="bin", src="bin")

    def test(self):
        pass
