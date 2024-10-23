@echo off
cd /d "%~dp0"
start "" python  ..\..\Tracking\gui_data\artus_lite_gui_publisher.py
timeout /t 5 /nobreak
python .\gui_controller.py