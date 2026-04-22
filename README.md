DIY Spectrometer Analyser

This application extracts the intensity distribution of wavelengths from a light source captured via a camera. It is designed to work with a low-cost, scratch-built spectrometer.

Prerequisites:
- Python 3.7+
- OpenCV (opencv-python)
- Matplotlib

Installation:
pip install opencv-python matplotlib

Usage:
1. Connect your spectrometer camera.
2. Run the application:
   python analyser.py [camera_index]
   (Optional: camera_index defaults to 0)

Controls:
- R: Select a Region of Interest (ROI) by dragging over the spectrum. Results are saved automatically after selection.
- S: Re-save and display the graph for the currently selected ROI.
- Q: Quit the application.

Results:
Captured spectrum images and CSV data are automatically saved in the 'results/' directory.

Hardware build instructions:
https://www.instructables.com/DIY-Low-Cost-Spectrometer/

License:
Distributed under the MIT License.
