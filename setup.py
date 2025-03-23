import os
import sys
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        pybind11_cmake_dir = subprocess.check_output(
            [sys.executable, "-c", "import pybind11; print(pybind11.get_cmake_dir())"],
            text=True
        ).strip()
        
        cmake_args = [
            f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}',
            f'-DPYTHON_EXECUTABLE={sys.executable}',
            f'-DCMAKE_PREFIX_PATH={pybind11_cmake_dir}',
        ]
        build_args = ['--config', 'Release']

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

setup(
    name='numpy_cmake_example',
    version='0.1.0',
    author='Your Name',
    description='A NumPy + C++ example with CMake and pybind11',
    long_description='',
    ext_modules=[CMakeExtension('numpy_cmake_example/array_add')],
    cmdclass={'build_ext': CMakeBuild},
    packages=['numpy_cmake_example'],
    install_requires=['numpy', 'pybind11>=2.6'],
    zip_safe=False,
)