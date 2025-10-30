import cv2
import numpy as np
import os
import csv
import glob

# Global variables used by the mouse callback and main loop.
drawing = False  # Tracks whether the left mouse button is currently pressed.
center = (0, 0)  # Circle center in the resized image coordinate system.
radius = 0       # Radius in the resized image coordinate system.

# Mouse callback: records center on LBUTTONDOWN, updates radius on MOUSEMOVE while drawing,
# and finalizes radius on LBUTTONUP.
def draw_circle(event, x, y, flags, param):
    global center, radius, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        # Set the center and start drawing
        center = (x, y)
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        # While dragging, update radius to current mouse position
        if drawing:
            dx = x - center[0]
            dy = y - center[1]
            radius = int(np.sqrt(dx * dx + dy * dy))
    elif event == cv2.EVENT_LBUTTONUP:
        # Finish drawing and set final radius
        drawing = False
        dx = x - center[0]
        dy = y - center[1]
        radius = int(np.sqrt(dx * dx + dy * dy))

# Process all images in folder_path and write results to csv_file and save annotated images to output_dir.
def process_images_from_folder(folder_path, output_dir, csv_file):
    # Collect image file paths (supports .jpg and .png; extend if needed).
    image_paths = glob.glob(os.path.join(folder_path, '*.jpg'))
    image_paths += glob.glob(os.path.join(folder_path, '*.png'))

    # Ensure output directory exists.
    os.makedirs(output_dir, exist_ok=True)

    # Open CSV file once in append mode and write header if file does not exist.
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['File Name', 'Diameter (mm)', 'Droplet Area'])

        # Iterate over each image path.
        for image_path in image_paths:
            # Reset globals for each new image (important when running multiple images).
            global center, radius, drawing
            center = (0, 0)
            radius = 0
            drawing = False

            image = cv2.imread(image_path)
            if image is None:
                print(f"Error loading image: {image_path}")
                continue

            # Create a smaller view for interactive selection so large images fit on screen.
            height, width = image.shape[:2]
            resize_factor = 0.5  # Display at 50% size for selection
            resized_image = cv2.resize(image, (int(width * resize_factor), int(height * resize_factor)))

            window_name = 'Image'
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.setMouseCallback(window_name, draw_circle)

            print(f"\nProcessing: {os.path.basename(image_path)}")
            print("Instructions: Left click and drag to draw a circle. Press 'c' to confirm and save, 'r' to reset selection, or ESC to skip this image.")

            confirmed = False
            while True:
                # Show a copy so we don't modify resized_image while drawing
                img_copy = resized_image.copy()
                if radius > 0:
                    # Draw the interactive circle on the display copy (green, thickness 2)
                    cv2.circle(img_copy, center, radius, (0, 255, 0), 2)

                cv2.imshow(window_name, img_copy)
                key = cv2.waitKey(1) & 0xFF

                if key == 27:  # ESC pressed -> skip this image without saving
                    print("Skipped image (ESC pressed).")
                    break
                elif key == ord('r'):  # Reset selection
                    center = (0, 0)
                    radius = 0
                    drawing = False
                    print("Selection reset (r pressed).")
                elif key == ord('c'):  # Confirm selection and proceed to save
                    if radius > 0:
                        confirmed = True
                        break
                    else:
                        print("No selection to confirm. Draw a circle first.")

            # If user confirmed, scale the coordinates back to original image size and save results.
            if confirmed:
                scale = 1 / resize_factor
                original_center = (int(center[0] * scale), int(center[1] * scale))
                original_radius = int(round(radius * scale))

                # Conversion factors: radius in pixels to mm (example factor 0.008 mm per pixel)
                # IMPORTANT: Make sure 0.008 is correct for your setup (pixel-to-mm calibration).
                px_to_mm = 0.008
                diameter_mm = original_radius * 2 * px_to_mm
                area_mm2 = np.pi * (original_radius * px_to_mm) ** 2

                # Annotate the original image with results (text and circle).
                cv2.putText(image, f"DIAMETER: {diameter_mm:.2f} mm", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(image, f"AREA: {area_mm2:.2f} mm^2", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.circle(image, original_center, original_radius, (0, 255, 0), 2)

                # Save annotated image to output directory with same base name
                base_name = os.path.basename(image_path)
                output_path = os.path.join(output_dir, base_name)
                cv2.imwrite(output_path, image)
                print(f"Saved annotated image to: {output_path}")

                # Write measured values to CSV (filename, diameter, area)
                writer.writerow([base_name, f"{diameter_mm:.2f}", f"{area_mm2:.2f}"])

            # Close windows related to this image before moving on to the next.
            cv2.destroyAllWindows()

# === Configuration: change these paths as needed ===
folder_path = 'images'      # Folder containing input images
output_dir = 'results'   # Folder where annotated images will be saved
csv_file = 'data.csv'      # CSV output file

# Run the processing function
process_images_from_folder(folder_path, output_dir, csv_file)
