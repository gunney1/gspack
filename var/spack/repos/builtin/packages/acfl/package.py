# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re

from spack.package import *

_os_map_before_23 = {
    "ubuntu18.04": "Ubuntu-18.04",
    "ubuntu20.04": "Ubuntu-20.04",
    "ubuntu22.04": "Ubuntu-20.04",
    "sles15": "SLES-15",
    "centos7": "RHEL-7",
    "centos8": "RHEL-8",
    "rhel7": "RHEL-7",
    "rhel8": "RHEL-8",
    "rocky8": "RHEL-8",
    "amzn2": "RHEL-7",
    "amzn2023": "RHEL-7",
}

_os_map = {
    "ubuntu20.04": "Ubuntu-20.04",
    "ubuntu22.04": "Ubuntu-22.04",
    "sles15": "SLES-15",
    "centos7": "RHEL-7",
    "centos8": "RHEL-8",
    "rhel7": "RHEL-7",
    "rhel8": "RHEL-8",
    "rhel9": "RHEL-9",
    "rocky8": "RHEL-8",
    "amzn2": "AmazonLinux-2",
    "amzn2023": "AmazonLinux-2023",
}

_versions = {
    "23.04": {
        "RHEL-7": (
            "6526218484e87c195c1145f60536552fabbd25ba98c05cf096f54de18381a422",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04/arm-compiler-for-linux_23.04_RHEL-7_aarch64.tar",
        ),
        "RHEL-8": (
            "e658c9d85693cc818f2be9942d8aa71465a84e00046d6f8da72c46a76cc8a747",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04/arm-compiler-for-linux_23.04_RHEL-8_aarch64.tar",
        ),
        "RHEL-9": (
            "b71431a16e09ae910737f920aab9c720b5ec83586dba8041b0daa45fa13521d1",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04/arm-compiler-for-linux_23.04_RHEL-9_aarch64.tar",
        ),
        "SLES-15": (
            "5dc880272942f5ac2cad7556bdbdf177b62a0736061c1acb1c80ca51ccaba3be",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04/arm-compiler-for-linux_23.04_SLES-15_aarch64.tar",
        ),
        "Ubuntu-20.04": (
            "a0b3bcec541a1e78b1a48d6fa876cc0ef2846f40219c95c60ab9852882ee05d2",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04/arm-compiler-for-linux_23.04_Ubuntu-20.04_aarch64.tar",
        ),
        "Ubuntu-22.04": (
            "10cf29da14830b3a9f0f51cda893e4255ffd1093297a71886865f97958d100f7",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04/arm-compiler-for-linux_23.04_Ubuntu-22.04_aarch64.tar",
        ),
        "AmazonLinux-2": (
            "65637a34abd076906bcbd56f2a7861ec873bc8d62e321217ade6008939a0bf6b",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04/arm-compiler-for-linux_23.04_AmazonLinux-2_aarch64.tar",
        ),
        "AmazonLinux-2023": (
            "415f8e908baf550e92ef21d4146904fac0a339132cb7921b4046e47ac71cf4c9",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/23-04/arm-compiler-for-linux_23.04_AmazonLinux-2023_aarch64.tar",
        ),
    },
    "22.1": {
        "RHEL-7": (
            "bfbfef9099bf0e90480d48b3a1a741d583fc939284f869958e9c09e177098c73",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/22-1/arm-compiler-for-linux_22.1_RHEL-7_aarch64.tar",
        ),
        "RHEL-8": (
            "28116f6030c95ee8f69eba89023966974d6b44d4a686098f5c3c03e34f7495f6",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/22-1/arm-compiler-for-linux_22.1_RHEL-8_aarch64.tar",
        ),
        "SLES-15": (
            "6616dba1af4a73300ce822b645a0f1dfd363f507db5ea44cab1c6051ea388554",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/22-1/arm-compiler-for-linux_22.1_SLES-15_aarch64.tar",
        ),
        "Ubuntu-18.04": (
            "3b3dd6f416299fbd14fbaf0b1bddf7e2f4445a186de7a87e9efdae0b9d0dc3d5",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/22-1/arm-compiler-for-linux_22.1_Ubuntu-18.04_aarch64.tar",
        ),
        "Ubuntu-20.04": (
            "e6361a08f75817c8dbfb56dc72578810eaf5ffb65591215e394cb3ec6bdd9c10",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/22-1/arm-compiler-for-linux_22.1_Ubuntu-20.04_aarch64.tar",
        ),
    },
    "22.0.2": {
        "RHEL-7": (
            "e4dec577ed2d33124a556ba05584fad45a9acf6e13dccadb37b521d1bad5a826",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-2/arm-compiler-for-linux_22.0.2_RHEL-7_aarch64.tar",
        ),
        "RHEL-8": (
            "3064bec6e0e3d4da9ea2bcdcb4590a8fc1f7e0e97092e24e2245c7f1745ef4f3",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-2/arm-compiler-for-linux_22.0.2_RHEL-8_aarch64.tar",
        ),
        "SLES-15": (
            "82dea469dc567b848bcaa6cbaed3eb3faaf45ceb9ec7071bdfef8a383e929ef8",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-2/arm-compiler-for-linux_22.0.2_SLES-15_aarch64.tar",
        ),
        "Ubuntu-18.04": (
            "355f548e86b9fa90d72684480d13ec60e6bec6b2bd837df42ac84d5a8fdebc48",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-2/arm-compiler-for-linux_22.0.2_Ubuntu-18.04_aarch64.tar",
        ),
        "Ubuntu-20.04": (
            "a2a752dce089a34b91dc89c0d1dd8b58a4104bf7c9ba3affd71fd1fd593e3732",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-2/arm-compiler-for-linux_22.0.2_Ubuntu-20.04_aarch64.tar",
        ),
    },
    "22.0.1": {
        "RHEL-7": (
            "6b0ab76dce3fd44aab1e679baef01367c86f6bbd3544e04f9642b6685482cd76",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_RHEL-7_aarch64.tar",
        ),
        "RHEL-8": (
            "41e5bffc52701b1e8a606f8db09c3c02e35ae39eae0ebeed5fbb41a13e61f057",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_RHEL-8_aarch64.tar",
        ),
        "SLES-15": (
            "b578ff517dec7fa23c4b7353a1a7c958f28cc9c9447f71f7c4e83de2e2c5538f",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_SLES-15_aarch64.tar",
        ),
        "Ubuntu-18.04": (
            "becc6826ce0f6e696092e79a40f758d7cd0302227f6cfc7c2215f6483ade9748",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_Ubuntu-18.04_aarch64.tar",
        ),
        "Ubuntu-20.04": (
            "dea136238fc2855c41b8a8154bf279b7df5df8dba48d8f29121fa26f343e7cdb",
            "https://developer.arm.com/-/media/Files/downloads/hpc/arm-allinea-studio/22-0-1/arm-compiler-for-linux_22.0.1_Ubuntu-20.04_aarch64.tar",
        ),
    },
}


def get_os(ver):
    spack_os = spack.platforms.host().default_os
    if ver.startswith("22."):
        return _os_map_before_23.get(spack_os, "")
    else:
        return _os_map.get(spack_os, "RHEL-7")


def get_armpl_version_to_3(spec):
    """Return version string with 3 numbers"""
    version_len = len(spec.version)
    assert version_len == 2 or version_len == 3
    if version_len == 2:
        return spec.version.string + ".0"
    elif version_len == 3:
        return spec.version.string


def get_armpl_prefix(spec):
    if spec.version.string.startswith("22."):
        return join_path(
            spec.prefix,
            "armpl-{}_AArch64_{}_arm-linux-compiler_aarch64-linux".format(
                get_armpl_version_to_3(spec), get_os(spec.version.string)
            ),
        )
    else:
        return join_path(
            spec.prefix,
            "armpl-{}_{}_arm-linux-compiler".format(
                get_armpl_version_to_3(spec), get_os(spec.version.string)
            ),
        )


def get_acfl_prefix(spec):
    if spec.version.string.startswith("22."):
        return join_path(
            spec.prefix,
            "arm-linux-compiler-{0}_Generic-AArch64_{1}_aarch64-linux".format(
                spec.version, get_os(spec.version.string)
            ),
        )
    else:
        return join_path(
            spec.prefix,
            "arm-linux-compiler-{0}_{1}".format(spec.version, get_os(spec.version.string)),
        )


def get_gcc_prefix(spec):
    dirlist = next(os.walk(spec.prefix))[1]
    return join_path(spec.prefix, next(dir for dir in dirlist if dir.startswith("gcc")))


class Acfl(Package):
    """Arm Compiler combines the optimized tools and libraries from Arm
    with a modern LLVM-based compiler framework.
    """

    homepage = "https://developer.arm.com/tools-and-software/server-and-hpc/arm-allinea-studio"
    url = "https://developer.arm.com/-/media/Files/downloads/hpc/arm-compiler-for-linux/22-1/arm-compiler-for-linux_22.1_Ubuntu-20.04_aarch64.tar"

    maintainers("annop-w")

    # Build Versions
    for ver, packages in _versions.items():
        acfl_os = get_os(ver)
        pkg = packages.get(acfl_os)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1])

    # Only install for Aarch64
    conflicts("target=x86_64:", msg="Only available on Aarch64")
    conflicts("target=ppc64:", msg="Only available on Aarch64")
    conflicts("target=ppc64le:", msg="Only available on Aarch64")

    executables = [r"armclang", r"armclang\+\+", r"armflang"]

    variant("ilp64", default=False, description="use ilp64 specific Armpl library")
    variant("shared", default=True, description="enable shared libs")
    variant(
        "threads",
        default="none",
        description="Multithreading support",
        values=("openmp", "none"),
        multi=False,
    )

    provides("blas")
    provides("lapack")
    provides("fftw-api@3")

    # Licensing - Not required from 22.0.1 on.

    # Run the installer with the desired install directory
    def install(self, spec, prefix):
        exe = Executable(
            "./arm-compiler-for-linux_{0}_{1}.sh".format(spec.version, get_os(spec.version.string))
        )
        exe("--accept", "--force", "--install-to", prefix)

    @classmethod
    def determine_version(cls, exe):
        regex_str = r"Arm C\/C\+\+\/Fortran Compiler version ([\d\.]+) " r"\(build number (\d+)\) "
        version_regex = re.compile(regex_str)
        try:
            output = spack.compiler.get_compiler_version_output(exe, "--version")
            match = version_regex.search(output)
            if match:
                if match.group(1).count(".") == 1:
                    return match.group(1) + ".0." + match.group(2)
                return match.group(1) + "." + match.group(2)
        except spack.util.executable.ProcessError:
            pass
        except Exception as e:
            tty.debug(e)

    @classmethod
    def determine_variants(cls, exes, version_str):
        compilers = {}
        for exe in exes:
            if "armclang" in exe:
                compilers["c"] = exe
            if "armclang++" in exe:
                compilers["cxx"] = exe
            if "armflang" in exe:
                compilers["fortran"] = exe
        return "", {"compilers": compilers}

    @property
    def cc(self):
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("c", None)
        return join_path(get_acfl_prefix(self.spec), "bin", "armclang")

    @property
    def cxx(self):
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("cxx", None)
        return join_path(get_acfl_prefix(self.spec), "bin", "armclang++")

    @property
    def fortran(self):
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes["compilers"].get("fortran", None)
        return join_path(get_acfl_prefix(self.spec), "bin", "armflang")

    @property
    def lib_suffix(self):
        suffix = ""
        suffix += "_ilp64" if self.spec.satisfies("+ilp64") else ""
        suffix += "_mp" if self.spec.satisfies("threads=openmp") else ""
        return suffix

    @property
    def blas_libs(self):
        armpl_prefix = get_armpl_prefix(self.spec)

        libname = "libarmpl" + self.lib_suffix

        # Get ArmPL Lib
        armpl_libs = find_libraries(
            [libname, "libamath", "libastring"],
            root=armpl_prefix,
            shared=self.spec.satisfies("+shared"),
            recursive=True,
        )

        armpl_libs += find_system_libraries(["libm"])

        return armpl_libs

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def fftw_libs(self):
        return self.blas_libs

    @property
    def libs(self):
        return self.blas_libs

    @property
    def headers(self):
        armpl_dir = get_armpl_prefix(self.spec)

        suffix = "include" + self.lib_suffix

        incdir = join_path(armpl_dir, suffix)

        hlist = find_all_headers(incdir)
        hlist.directories = [incdir]
        return hlist

    def setup_run_environment(self, env):
        arm_dir = get_acfl_prefix(self.spec)
        armpl_dir = get_armpl_prefix(self.spec)
        gcc_dir = get_gcc_prefix(self.spec)

        env.set("ARM_LINUX_COMPILER_DIR", arm_dir)
        env.set("ARM_LINUX_COMPILER_INCLUDES", join_path(arm_dir, "includes"))
        env.append_path("ARM_LINUX_COMPILER_LIBRARIES", join_path(arm_dir, "lib"))
        env.prepend_path("PATH", join_path(arm_dir, "bin"))
        env.prepend_path("CPATH", join_path(arm_dir, "include"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(arm_dir, "lib"))
        env.append_path("LD_LIBRARY_PATH", join_path(armpl_dir, "lib"))
        env.prepend_path("LIBRARY_PATH", join_path(arm_dir, "lib"))
        env.prepend_path("MANPATH", join_path(arm_dir, "share", "man"))

        env.set("GCC_DIR", gcc_dir)
        env.set("GCC_INCLUDES", join_path(gcc_dir, "include"))
        env.append_path("GCC_LIBRARIES", join_path(gcc_dir, "lib"))
        env.append_path("GCC_LIBRARIES", join_path(gcc_dir, "lib64"))
        env.set("COMPILER_PATH", gcc_dir)
        env.prepend_path("PATH", join_path(gcc_dir, "binutils_bin"))
        env.prepend_path("CPATH", join_path(gcc_dir, "include"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(gcc_dir, "lib"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(gcc_dir, "lib64"))
        env.prepend_path("LIBRARY_PATH", join_path(gcc_dir, "lib"))
        env.prepend_path("LIBRARY_PATH", join_path(gcc_dir, "lib64"))
        env.prepend_path("MANPATH", join_path(gcc_dir, "share", "man"))

    @run_after("install")
    def check_install(self):
        arm_dir = get_acfl_prefix(self.spec)
        armpl_dir = get_armpl_prefix(self.spec)
        gcc_dir = get_gcc_prefix(self.spec)
        armpl_example_dir = join_path(armpl_dir, "examples")
        # run example makefile
        make(
            "-C",
            armpl_example_dir,
            "CC=" + self.cc,
            "F90=" + self.fortran,
            "CPATH=" + join_path(arm_dir, "include"),
            "COMPILER_PATH=" + gcc_dir,
        )
        # clean up
        make("-C", armpl_example_dir, "clean")
