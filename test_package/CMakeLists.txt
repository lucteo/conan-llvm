project(TestLlvm)
cmake_minimum_required(VERSION 3.4.3)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

include("share/llvm/cmake/LLVMConfig")

if(NOT LLVM_INSTALL_PREFIX)
    message(FATAL_ERROR "ERROR! LLVM NOT FOUND!")
endif()
