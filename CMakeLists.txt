cmake_minimum_required(VERSION 3.10)
project(numpy_cmake_example LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Use the Python executable provided by the user or environment
if(NOT PYTHON_EXECUTABLE)
    set(PYTHON_EXECUTABLE "python3")
endif()

# Find Python
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
message(STATUS "Python3 found: ${Python3_EXECUTABLE}")

# Manually get NumPy include path
execute_process(
    COMMAND "${Python3_EXECUTABLE}" -c "import numpy; print(numpy.get_include())"
    OUTPUT_VARIABLE NUMPY_INCLUDE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
    RESULT_VARIABLE NUMPY_RESULT
)
if(NOT NUMPY_RESULT EQUAL 0)
    message(FATAL_ERROR "Failed to find NumPy include directory")
endif()
message(STATUS "NumPy include dir: ${NUMPY_INCLUDE_DIR}")

# Include directories
include_directories(${Python3_INCLUDE_DIRS} ${NUMPY_INCLUDE_DIR})

# Find pybind11 using its Python-installed location
execute_process(
    COMMAND "${Python3_EXECUTABLE}" -c "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE PYBIND11_CMAKE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
    RESULT_VARIABLE PYBIND11_RESULT
)
if(NOT PYBIND11_RESULT EQUAL 0)
    message(FATAL_ERROR "Failed to find pybind11 CMake directory")
endif()
message(STATUS "pybind11 CMake dir: ${PYBIND11_CMAKE_DIR}")
list(APPEND CMAKE_PREFIX_PATH "${PYBIND11_CMAKE_DIR}")

# Find pybind11
find_package(pybind11 REQUIRED)

# Add the module
pybind11_add_module(array_add src/array_add.cpp)
target_link_libraries(array_add PRIVATE ${Python3_LIBRARIES})