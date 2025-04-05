# Modified AdTree Compilation Guide

​**​Important Notice​**​:  
The original AdTree implementation cannot retrieve face counts. You must use this modified version to enable mesh face counting functionality.
### Build and Run AdTree
Prebuilt executables (for **macOS**, **Linux**, and **Windows**) can be downloaded 
[here](https://github.com/tudelft3d/adtree/releases). 

AdTree depends on some third-party libraries and most dependencies are included in the distribution except 
[Boost](https://www.boost.org/). So you will need to have Boost installed first. 

Note: AdTree uses a stripped earlier version of [Easy3D](https://github.com/LiangliangNan/Easy3D), which is not 
compatible with the latest version.

You need [CMake](https://cmake.org/download/) and of course a compiler to build AdTree:

- CMake `>= 3.1`
- a compiler that supports `>= C++11`

AdTree has been tested on macOS (Xcode >= 8), Windows (MSVC >=2015), and Linux (GCC >= 4.8, Clang >= 3.3). Machines 
nowadays typically provide higher [support](https://en.cppreference.com/w/cpp/compiler_support), so you should be 
able to build AdTree on almost all platforms.

There are many options to build AdTree. Choose one of the following (or whatever you are familiar with):

- Option 1: Use any IDE that can directly handle CMakeLists files to open the `CMakeLists.txt` in the root directory 
of AdTree. Then you should have obtained a usable project and just build. I recommend using
 [CLion](https://www.jetbrains.com/clion/) or [QtCreator](https://www.qt.io/product). For Windows users: your IDE must be set for `x64`.
 
- Option 2: Use CMake to generate project files for your IDE. Then load the project to your IDE and build. For Windows users: your IDE must be set for `x64`.

- Option 3: Use CMake to generate Makefiles and then build (purely command line).
  - on Linux or macOS:
    ```
    $ cd path-to-root-dir-of-AdTree 
    $ mkdir Release
    $ cd Release
    $ cmake -DCMAKE_BUILD_TYPE=Release ..
    $ make
    ```
  - on Windows with Microsoft Visual Studio, use the `x64 Native Tools Command Prompt for VS XXXX` (don't use the x86 one), then
    ```
    $ cd path-to-root-dir-of-AdTree 
    $ mkdir Release
    $ cd Release
    $ cmake -G "NMake Makefiles" -DCMAKE_BUILD_TYPE=Release ..
    $ nmake
    ```

Don't have any experience with C/C++ programming? Have a look at [How to build AdTree step by step](./How_to_build.md).


### Citation

```bibtex
@article{du2019adtree,
  title={AdTree: Accurate, detailed, and automatic modelling of laser-scanned trees},
  author={Du, Shenglan and Lindenbergh, Roderik and Ledoux, Hugo and Stoter, Jantien and Nan, Liangliang},
  journal={Remote Sensing},
  volume={11},
  number={18},
  pages={2074},
  year={2019}
}
```

---


