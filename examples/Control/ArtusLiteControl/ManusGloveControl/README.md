# Artus Lite Manus Gloves Control

This guide provides instructions on how to use the GUI to control the Artus Lite hand robot.

## Table of Contents

- [Artus Lite Manus Gloves Control](#artus-lite-manus-gloves-control)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Control](#running-the-control)

## Requirements

- Python >= 3.10
- Requirements: Manus Glove SDK
- Artus Lite hand robot
- Windows OS

## Installation


1. Download the Manus Glove SDK from the [Manus website](https://docs.manus-meta.com/2.4.0/Plugins/SDK/getting%20started/)

## Configuration

Before running the GUI, ensure that the configuration file is updated with the correct settings for your Artus Lite hand robot. The configuration file is located at `Sarcomere_Dynamics_Resources/Control/configuration/robot_config.yaml`.

## Running the Control

To start the Manus Glove control for controlling the Artus Lite hand robot, follow these steps:

1. Navigate to the directory containing the python script:
    ```sh
    Sarcomere_Dynamics_Resources/examples/Control/ArtusLiteControl/ManusGloveControl
    ```

2. Run python script:

    ```sh
    python manus_glove_control.py
    ```