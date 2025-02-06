![Recon](assets/logo.svg)

## Summary

Recon is a python application made for computed tomography (CT) research, it uses [GATE 10](https://github.com/OpenGATE/opengate) for simulating CT scans and [Dear PyGui](https://github.com/hoffstadt/DearPyGui) for the graphical user interface.

## Architecture

- Observer and Observable interfaces
- Simulation model implementing Observable
- View class, children implement Observer
    - Menu class
    - Parameters class
    - Objects class
    

## Requirements

Use DearPy GUI

Create, read, update, delete, load and save simulations 

[License](LICENSE)
