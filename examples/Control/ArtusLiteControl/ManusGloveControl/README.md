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
- Visual Studio

## Installation


1. Download the Manus Glove SDK (2.3.0.1) from the [Manus website](https://my.manus-meta.com/resources/downloads/quantum-metagloves)

2. Open the solution file in Visual Studio: \MANUS\MANUS_Core_2.3.0.1_SDK\MANUS_Core_2.3.0.1_SDK\ManusSDK_v2.3.0.1\SDKClient\SDKClient.sln

3. Copy the contents of the SDKClient.cpp  and SDKClient.hpp files with the respective files in this repository

4. Build Solution in Visual Studio

5. An updated exe file should be produced: \MANUS\MANUS_Core_2.3.0.1_SDK\MANUS_Core_2.3.0.1_SDK\ManusSDK_v2.3.0.1\SDKClient\Output\x64\Debug\Client\SDKClient.exe

6. In the manus_glove_controller.py file (\Sarcomere_Dynamics_Resources\examples\Control\ArtusLiteControl\ManusGloveControl\manus_glove_controller.py), change the path in line 36 to the path on your computer for the SDKClient.exe file
   
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
    python manus_glove_controller.py
    ```
