from conans import ConanFile, ConfigureEnvironment, CMake
from conans.tools import download, unzip, untargz
import os, platform
from contextlib import contextmanager

@contextmanager
def inDir(directory):
    lastDir = os.getcwd()
    try:
        os.makedirs(directory)
    except OSError:
        pass

    try:
        os.chdir(directory)
        yield directory
    finally:
        os.chdir(lastDir)

class LlvmConan(ConanFile):
    name = 'llvm'
    version = '3.9.1'
    url = 'https://github.com/lucteo/conan-llvm.git'
    license = 'BSD'
    settings = 'os', 'compiler', 'build_type', 'arch'
    exports = '*'
    options = {'shared': [True, False]}
    default_options = 'shared=True'

    archiveName = 'llvm-3.9.1.src.tar.xz'
    folderName = 'llvm-3.9.1.src'

    def extractFromUrl(self, url):
        self.output.info('download {}'.format(url))
        filename = os.path.basename(url)
        download(url, filename)
        if platform.system() != 'Windows':
            self.run('tar xf %s' % filename)
        else:
            self.run('7z x %s -so | 7z x -si -ttar' % filename)
        os.unlink(filename)

    def source(self):
        url = 'http://llvm.org/releases/3.9.1/llvm-3.9.1.src.tar.xz'
        self.extractFromUrl(url)

    def build(self):
        cmake = CMake(self.settings)
        with inDir('build'):
            srcDir = os.path.join(self.conanfile_directory, self.folderName)
            installDir = os.path.join(self.conanfile_directory, 'install')
            # No shared libraries on windows (with MSVC)
            sharedLibs = 'ON' if self.options.shared and platform.system() != 'Windows' else 'OFF'
            self.output.info('Configuring CMake...')
            cmakeCmd = ('cmake "{srcDir}" {cmd}'
                     ' -DCMAKE_INSTALL_PREFIX="{installDir}"'
                     ' -DLLVM_INCLUDE_TOOLS=ON'
                     ' -DLLVM_INCLUDE_TESTS=OFF'
                     ' -DLLVM_INCLUDE_EXAMPLES=OFF'
                     ' -DLLVM_INCLUDE_GO_TESTS=OFF'
                     ' -DLLVM_BUILD_TOOLS=ON'
                     ' -DLLVM_BUILD_TESTS=OFF'
                     ' -DLLVM_TARGETS_TO_BUILD=X86'
                     ' -DLLVM_BUILD_LLVM_DYLIB={sharedLibs}'
                     ''.format(srcDir=srcDir,
                           cmd=cmake.command_line,
                           installDir=installDir,
                           sharedLibs=sharedLibs))
            self.output.info('Cmake command line: ' + cmakeCmd)
            self.run(cmakeCmd);
            self.output.info('Building...')
            extraFlags = ('-j4' if platform.system() != 'Windows' else '')
            buildCmd = ('cmake --build . {cfg} -- {extraFlags}'
                     ''.format(cfg=cmake.build_config, extraFlags=extraFlags))
            self.output.info('Build command line: ' + buildCmd)
            self.run(buildCmd);
            self.output.info('Installing...')
            installCmd = 'cmake --build . {cfg} --target install'.format(cfg=cmake.build_config)
            self.output.info('Install command line: ' + installCmd)
            self.run(installCmd);

    def conan_info(self):
        self.info.settings.build_type = 'Release'

    def package(self):
        self.copy('*', dst='', src='install')
