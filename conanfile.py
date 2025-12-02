import os
from textwrap import dedent
from conan import ConanFile
from conan.tools.files import update_conandata, copy, rm, chdir, mkdir, collect_libs, replace_in_file, save, rename
from conan.tools.env import VirtualRunEnv, VirtualBuildEnv
from conan.tools.scm import Git
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
from conan.tools.microsoft import VCVars
from conan.tools.layout import basic_layout

class ZenohCConan(ConanFile):

    name = "iceoryx2"
    version = "0.7.0"
    
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

    exports_sources = "CMakeLists.txt"

    def export(self):
        update_conandata(self, {"sources": {
            # "commit": "v{}".format(self.version),
            "commit": "196c471bd2732ca1a53766c71223e36cba0eaaae",  # dec 2nd, 2025
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
        cmake_layout(self)
        # force custom build folder - maybe expected from the cmake scripts / cargo integration.
        self.folders.build = "target/ff/cc/build"

    def patch_sources(self):
        pass

    def build(self):
        self.patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def _iceoryx2_cxx_lib_name(self):
        name = "iceoryx2_cxx"
        # if self.settings.build_type == "Debug":
        #     name += "d"
        return name

    def _iceoryx2_bb_cxx_lib_name(self):
        name = "iceoryx2-bb-cxx"
        # if self.settings.build_type == "Debug":
        #     name += "d"
        return name

    def _iceoryx2_c_lib_name(self):
        name = "iceoryx2_ffi_c"
        # if self.settings.build_type == "Debug":
        #     name += "d"
        return name

    def package(self):
        if self.is_win:
            bin_path = None
            folder = "release" if self.settings.build_type == "Release" else "debug"
            bin_path = os.path.join(self.build_folder, folder, "target", folder)

            # clean up before recursive copy
            rm(self, "*.dll", os.path.join(bin_path, "deps"))
            rm(self, "*.lib", os.path.join(bin_path, "deps"))
            # Manually copy the files in the target (needs to be adapted if debug build is enabled ..)

            copy(self, "*.dll", bin_path, os.path.join(self.package_folder, "bin"), keep_path=False)
            copy(self, "*.lib", bin_path, os.path.join(self.package_folder, "lib"), keep_path=False)
            copy(self, "*.h", os.path.join(self.build_folder, folder, "include"), os.path.join(self.package_folder, "include"))
            copy(self, "*.h", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
        else:
            cmake = CMake(self)
            cmake.install()

            lib_build_path = os.path.join(self.build_folder, "iceoryx2-cxx")


            # copy(self, "*.h", os.path.join(self.source_folder, "iceoryx2-cxx", "include"), os.path.join(self.package_folder, "include", "iceoryx2", f"v{self.version}"))
            # copy(self, "*.hpp", os.path.join(self.source_folder, "iceoryx2-cxx", "include"), os.path.join(self.package_folder, "include", "iceoryx2", f"v{self.version}"))

            if self.settings.os == "Linux":
                if self.options.shared:
                    rm(self, "*.so", os.path.join(self.package_folder, "lib"), recursive=False)
                    # copy(self, "*.so", lib_build_path, os.path.join(self.package_folder, "lib"), keep_path=False)
                else:
                    rm(self, "*.so", os.path.join(self.package_folder, "lib"), recursive=False)
                    # copy(self, "*.a", lib_build_path, os.path.join(self.package_folder, "lib"), keep_path=False)
            elif self.settings.os == "Macos":
                if self.options.shared:
                    rm(self, "*.dylib", os.path.join(self.package_folder, "lib"), recursive=False)
                    # copy(self, "*.dylib", lib_build_path, os.path.join(self.package_folder, "lib"), keep_path=False)
                else:
                    rm(self, "*.dylib", os.path.join(self.package_folder, "lib"), recursive=False)
                    # copy(self, "*.a", lib_build_path, os.path.join(self.package_folder, "lib"), keep_path=False)
            elif self.is_win:
                if self.options.shared:
                    pass
                    # copy(self, "*.dll", lib_build_path, os.path.join(self.package_folder, "bin"), keep_path=False)
                else:
                    rm(self, "*.dll", os.path.join(self.package_folder, "bin"), recursive=False)
                    # copy(self, "*.lib", lib_build_path, os.path.join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [self._iceoryx2_c_lib_name(), self._iceoryx2_bb_cxx_lib_name(), self._iceoryx2_cxx_lib_name()]
        self.cpp_info.includedirs.append(os.path.join("include", "iceoryx2", f"v{self.version}"))
