<h1 align="center">
        🐭 Oxy® Mouse
    </h1>
    <p align="center">
        <p align="center">Generate mouse movements with Python & different algorithms</p>
    </p>
<h4 align="center">
    <a href="https://discord.gg/cZZ7Bw4xN3">
        <img src="https://img.shields.io/static/v1?label=Chat%20on&message=Discord&color=blue&logo=Discord&style=flat-square" alt="Discord">
    </a>
</h4>


OxyMouse is a Python library for generating mouse movements. 

It is designed to work with any browser control library that supports 2D moving of the mouse cursor.

## Installation

```bash
pip install oxymouse
```

## Usage

Specify `algorithm` an algorithm.

Supported algorithms:

`bezier`, `gaussian`, `perlin`

```python

from oxymouse import OxyMouse

mouse = OxyMouse(algorithm="bezier")
movements = mouse.generate_coordinates()
```


