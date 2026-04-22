import cv2

def check_cameras():
    index = 0
    arr = []
    while index < 5:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if cap.read()[0]:
            print(f"Camera index {index} is working with CAP_DSHOW.")
            arr.append(index)
            cap.release()
        else:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                print(f"Camera index {index} is working with default backend.")
                arr.append(index)
                cap.release()
            else:
                print(f"Camera index {index} is not responding.")
        index += 1
    return arr

if __name__ == "__main__":
    print("Checking for available cameras...")
    working_indices = check_cameras()
    if not working_indices:
        print("No working cameras found. Please check your connection and Windows Privacy Settings.")
    else:
        print(f"Working camera indices: {working_indices}")
