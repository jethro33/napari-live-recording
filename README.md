# napari-live-recording

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/jacopoabramo/napari-live-recording/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-live-recording.svg?color=green)](https://pypi.org/project/napari-live-recording)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-live-recording.svg?color=green)](https://python.org)


<!--[![tests](https://github.com/jethro33/napari-live-recording/workflows/tests/badge.svg)](https://github.com/jacopoabramo/napari-live-recording/actions)-->
<!--[![codecov](https://codecov.io/gh/jethro33/napari-live-recording/branch/master/graph/badge.svg)](https://codecov.io/gh/jacopoabramo/napari-live-recording)-->

----------------------------------

This [napari] plugin was generated with [Cookiecutter] using with [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/docs/plugins/index.html
-->

## Description

`napari-live-recording` (or `nlr`, if you like acronyms) is a <a href="#why-medium-weight">medium-weight</a> plugin part of the napari ecosystem that provides an easy 
access point for controlling area detector devices (most commonly reffered to as cameras) with a common interface.
Other than that, the plugin also allows to create computation pipelines that can be executed real-time in a flow starting directly from the camera stream.

> [!NOTE]
> 
> ### Why medium weight?
> `napari-live-recording` relies on multithreading to handle camera control
> image processing and data storage via a common pipelined infrastructure.
> More details are provided in the documentation.

The plugin allows two modes of operation:

- live view (continously acquiring from the currently active camera and show the collected data on the napari viewer);
- recording (stream data to disk from the currently active cameras).

When recording, the plugin allows to store images according to the following formats:

- ImageJ TIFF
- OME-TIFF

> [!NOTE]
> Future releases will also add further file formats to the recording options, specifically:
> - HDF5
> - MP4
>
> Furthermore, we will provide a method to add custom metadata to the recorded image files.

## Supported cameras

`napari-live-recording` aims to maintain itself agnostic for the type of cameras it controls. Via a common API (Application Programming Interface),
it possible to define a controller for a specific camera. Instructions
on how to do so are provided in the documentation.

By default, the plugin is shipped with the following interfaces:

- an [OpenCV](./src/napari_live_recording/control/devices/opencv.py) camera grabber;
- a [Micro-Manager](./src/napari_live_recording/control/devices/micro_manager.py) interface via the package [`pymmcore-plus`](https://pypi.org/project/pymmcore-plus/);
- an interface to the [microscope](./src/napari_live_recording/control/devices/pymicroscope.py) python package.

## Installation

You can install `napari-live-recording` via [pip]. It is reccomended to install `napari-live-recording` in a virtual environment. This can be do so via:

- [venv], for example:
    
        python -m venv nlr
        nlr\Scripts\activate
        pip install napari-live-recording

- [conda] or [mamba]

        mamba create -n nlr python=3.10 napari-live-recording

Alternatively, if you want to install the plugin using the source code, you can do so by cloning the project and installing locally:

    git clone https://github.com/jacopoabramo/napari-live-recording
    cd napari-live-recording
    pip install .

## Documentation

You can review the documentation of this plugin [here](./docs/README.md)

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## Acknowledgments

The developers would like to thank the [Chan-Zuckerberg Initiative (CZI)](https://chanzuckerberg.com/) for providing funding
for this project via the [napari Ecosystem Grants](https://chanzuckerberg.com/science/programs-resources/imaging/napari/napari-live-recording-camera-control-through-napari/).

<p align="center">
  <img src="https://images.squarespace-cdn.com/content/v1/63a48a2d279afe2a328b2823/5830fddc-a02b-451a-827b-3d4446dcf57b/Chan_Zuckerberg_Initiative.png" width="150">
</p>

## License

Distributed under the terms of the [MIT] license,
"napari-live-recording" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/jacopoabramo/napari-live-recording/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
[venv]: https://docs.python.org/3/library/venv.html
[mamba]: https://mamba.readthedocs.io/en/latest/user_guide/mamba.html#mamba
[conda]: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
