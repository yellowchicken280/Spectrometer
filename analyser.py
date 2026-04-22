import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import csv
from datetime import datetime

def save_results(snapshot):
    """Processes the snapshot, saves the graph and CSV, and displays the plot."""
    shape = snapshot.shape
    
    b_dist, g_dist, r_dist, i_dist = [], [], [], []
    
    for i in range(shape[1]):
        b_val = np.mean(snapshot[:, i, 0])
        g_val = np.mean(snapshot[:, i, 1])
        r_val = np.mean(snapshot[:, i, 2])
        i_val = (r_val + b_val + g_val) / 3

        r_dist.append(r_val)
        g_dist.append(g_val)
        b_dist.append(b_val)
        i_dist.append(i_val)
    
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.imshow(cv2.cvtColor(snapshot, cv2.COLOR_BGR2RGB))
    plt.title("Captured Spectrum")

    plt.subplot(2, 1, 2)
    plt.plot(r_dist, color='r', label='Red')
    plt.plot(g_dist, color='g', label='Green')
    plt.plot(b_dist, color='b', label='Blue')
    plt.plot(i_dist, color='k', label='Mean Intensity')
    plt.legend(loc="upper left")
    plt.xlabel("Pixel Position (Horizontal)")
    plt.ylabel("Intensity (0-255)")
    plt.title("Intensity Distribution")
    plt.tight_layout()
    
    # Auto-save the result
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_filename = f"results/spectrum_{timestamp}.png"
    csv_filename = f"results/spectrum_{timestamp}.csv"
    
    plt.savefig(img_filename)
    print(f"Graph saved as {img_filename}")
    
    # Save data to CSV
    with open(csv_filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Pixel', 'Red', 'Green', 'Blue', 'Mean Intensity'])
        for i in range(len(r_dist)):
            writer.writerow([i, r_dist[i], g_dist[i], b_dist[i], i_dist[i]])
    print(f"Data saved as {csv_filename}")
    
    plt.show()

def main():
    # Get camera index from command line argument, default to 0
    camera_index = 0
    if len(sys.argv) > 1:
        try:
            camera_index = int(sys.argv[1])
        except ValueError:
            print(f"Invalid camera index '{sys.argv[1]}', using default 0")
    
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    # Create results directory if it doesn't exist
    if not os.path.exists('results'):
        os.makedirs('results')

    roi_selected = False
    r = None
    cropped = None

    print(f"Using Camera Index: {camera_index}")
    print("Controls:")
    print("  'r' - Select ROI (Auto-saves after selection)")
    print("  's' - Save/Show Graph again for current ROI")
    print("  'q' - Quit")
    
    while(True):
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Try changing camera_index.")
            break

        if roi_selected and r is not None:
            try:
                cropped = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                cv2.imshow('roi', cropped)
            except:
                roi_selected = False
        
        cv2.imshow('frame', frame)
        
        k = cv2.waitKey(1)
        
        # 's' key: Save current ROI again
        if k & 0xFF == ord('s') and roi_selected and cropped is not None:
            save_results(cropped.copy())

        # 'r' key: Select ROI and auto-save
        elif k & 0xFF == ord('r'):
            r = cv2.selectROI('frame', frame)
            if r[2] > 0 and r[3] > 0:
                roi_selected = True
                # Crop immediately and save
                cropped = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                save_results(cropped.copy())
            
        elif k & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
