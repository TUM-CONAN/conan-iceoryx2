import os
from textwrap import dedent
from conan import ConanFile
from conan.tools.files import apply_conandata_patches, export_conandata_patches, update_conandata, copy, rm, chdir, mkdir, collect_libs, replace_in_file, save, rename
from conan.tools.env import VirtualRunEnv, VirtualBuildEnv
from conan.tools.scm import Git
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
from conan.tools.microsoft import VCVars
from conan.tools.layout import basic_layout

class Iceoryx2Conan(ConanFile):

    name = "iceoryx2"
    version = "0.8.0"
    
    license = "Apache License 2.0"
    author = "Ulrich Eck"
    url = "https://github.com/TUM-CONAN/conan-iceoryx2.git"
    description = "Recipe to build iceoryx using conan"    

    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_examples": [True, False],
        "build_testing": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "build_examples": False,
        "build_testing": False,
    }

    def export(self):
        update_conandata(self, {"sources": {
            "commit": "v{}".format(self.version),
            "url": "https://github.com/eclipse-iceoryx/iceoryx2.git"
            }}
            )

    def source(self):
        git = Git(self)
        sources = self.conan_data["sources"]
        git.clone(url=sources["url"], target=self.source_folder)
        git.checkout(commit=sources["commit"])


    @property
    def is_win(self):
        return self.settings.os == "Windows" or self.settings.os == "WindowsStore"

    @property
    def is_uwp_armv8(self):
        return self.settings.os == "WindowsStore" and self.settings.arch == "armv8"
    
    @property
    def is_win_x64(self):
        return self.settings.os == "Windows" and self.settings.arch == "x86_64"

    def _patch_sources(self):
        apply_conandata_patches(self)

    def generate(self):

        tc = CMakeToolchain(self)
        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            tc.variables[var_name] = var_value

        for option, value in self.options.items():
            add_cmake_option(option, value)

        tc.cache_variables["BUILD_CXX"] = True

        tc.generate()

        deps = CMakeDeps(self)

        deps.generate()

    def layout(self):
        cmake_layout(self, 
            src_folder="src",
            build_folder="src/target/ff/cc/build")
 
    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def _iceoryx2_cxx_lib_name(self):
        name = "iceoryx2_cxx"
        # if self.settings.build_type == "Debug":
        #     name += "d"
        return name

    def _iceoryx2_c_lib_name(self):
        name = "iceoryx2_ffi_c"
        # if self.settings.build_type == "Debug":
        #     name += "d"
        return name

    def package(self):
        cmake = CMake(self)
        cmake.install()

        lib_build_path = os.path.join(self.build_folder, "iceoryx2-cxx")

        if self.settings.os == "Linux":
            if self.options.shared:
                rm(self, "*.a", os.path.join(self.package_folder, "lib"), recursive=False)
            else:
                rm(self, "*.so", os.path.join(self.package_folder, "lib"), recursive=False)
        elif self.settings.os == "Macos":
            if self.options.shared:
                rm(self, "*.a", os.path.join(self.package_folder, "lib"), recursive=False)
            else:
                rm(self, "*.dylib", os.path.join(self.package_folder, "lib"), recursive=False)
        elif self.is_win:
            copy(self, "*.dll", os.path.join(self.package_folder, "lib"), os.path.join(self.package_folder, "bin"))

    def package_info(self):
        self.cpp_info.libs = [self._iceoryx2_c_lib_name(), self._iceoryx2_cxx_lib_name()]
        self.cpp_info.includedirs.append(os.path.join("include", "iceoryx2", f"v{self.version}"))
