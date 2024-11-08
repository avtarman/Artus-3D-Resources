# General Example for Artus API

The general example demonstrates how to use the Artus API to control the Artus Lite hand robot. It provides a simple command-line interface to connect to the robot, send commands, and retrieve robot states.

## Requirements
- Python >= 3.10
- Required Python packages: `pyyaml`
- Artus Lite hand robot
- Make sure you have installed the requirements for Artus API. Refer to the [README](../../README.md) for more information.

## Installation

1. Install the required Python packages:
    ```sh
    pip install pyyaml
    ```

## Configuration

Before running the example, ensure that the configuration file is updated with the correct settings for your Artus Lite hand robot. The configuration file is located at `examples/general_example/config/artus_config.yaml`.

## Running the Example

To run the general example, execute the following command:
```sh
python3 path/to/general_example.py
```