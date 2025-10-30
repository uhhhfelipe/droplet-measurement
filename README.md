# Circle Measurement Tool (OpenCV)

This repository provides a simple **interactive image measurement tool** built with Python and OpenCV.  
It allows users to draw circles on droplet or colony images to automatically calculate the **diameter (mm)** and **area (mm²)** of each region of interest.  
All results are saved to an annotated image and a `.csv` file for further analysis.

---

## 🧪 Features
- Interactive circle drawing using the mouse.
- Automatic calculation of diameter and area.
- Real-time display of drawn circle before saving.
- Saves annotated images to an output folder.
- Stores results (filename, diameter, area) in a CSV file.
- Adjustable pixel-to-mm calibration factor.

---

## ⚙️ Requirements

Make sure you have **Python 3.8+** installed, then install dependencies:

```bash
pip install opencv-python numpy
```

---

## 📂 Folder Structure

```
project/
│
├── images/          # Folder containing your input images (.jpg or .png)
├── results/      # (Created automatically) Folder where annotated images are saved
├── data.csv        # CSV file created with all measurements
└── droplet-measurement.py          # The main script
```

---

## ▶️ How to Run

1. Place all input images in the `images/` folder.
2. Open the terminal in your project directory.
3. Run the script:

```bash
python droplet-measurement.py
```

4. The interactive window will open for each image.

---

## 🖱️ Controls

| Key / Mouse Action | Function |
|--------------------|-----------|
| **Left click + drag** | Draw a circle around the droplet or colony |
| **C** | Confirm selection and save results |
| **R** | Reset current selection |
| **ESC** | Skip the current image without saving |

---

## 📏 Measurement Calibration

The script converts pixel dimensions to millimeters using a constant:

```python
px_to_mm = 0.008
```

This factor must correspond to your imaging setup (camera sensor, magnification, microscope, etc.).  
To calibrate it:
1. Capture an image containing a known scale (e.g., ruler or calibration slide).
2. Measure the number of pixels per millimeter in that image.
3. Update the value of `px_to_mm` in the script accordingly.

Example:  
If 1 mm corresponds to 125 pixels in your setup, then:
```python
px_to_mm = 1 / 125  # = 0.008 mm/pixel
```

---

## 💾 Output Example

For an image named `sample1.jpg`, after drawing and confirming the circle:
- The script saves an annotated copy as `results/sample1.jpg`.
- A row is added to `data.csv`:

| File | Diameter (mm) | Area (mm²) |
|------|----------------|------------|
| sample1.jpg | 2.56 | 5.15 |

---

## ⚠️ Notes

- The program supports `.jpg` and `.png` by default. Add more extensions if necessary.
- Make sure to close the image window (press `ESC`) before processing the next image.
- The CSV header is created only once; additional results are appended.

---

## 🧑‍💻 Author

Developed by **Felipe Porteiro**  
For biological image analysis and droplet measurement automation.  
Compatible with Python 3 and OpenCV 4.

---

## 📜 License

This project is released under the **MIT License**.  
You are free to use, modify, and distribute this code with proper attribution.
