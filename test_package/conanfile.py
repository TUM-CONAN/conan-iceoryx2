import os

from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import CMake, cmake_layout


class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps", "CMakeToolchain", "VirtualRunEnv"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if can_run(self):
            binary = os.path.join(self.cpp.build.bindir, "test_package")
            self.run(binary, env="conanrun")
            if self.dependencies[self.tested_reference_str.split("#")[0]].options.shared:
                # One shared FFI library per process (HoloMQ's requirement).
                from io import StringIO
                out = StringIO()
                self.run(f"ldd {binary}", stdout=out, env="conanrun")
                if "libiceoryx2_ffi_c.so" not in out.getvalue():
                    raise Exception("test_package does not link the shared libiceoryx2_ffi_c.so")
