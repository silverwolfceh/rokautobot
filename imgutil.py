import cv2
import os

# Global variables for cropping and highlighting
cropping = False
start_point = (0, 0)
end_point = (0, 0)
highlighted_area = None

# Load an image from file (initially blank, will be updated)
image_path = 'screencap.png'
image = None
image_display = None

def capture_ldplayer_screen():
    """
    Capture the LDPlayer screen using ADB commands.
    """
    os.system("adb exec-out screencap -p > screencap.png")
    global image, image_display
    image = cv2.imread('screencap.png')
    image_display = image.copy()

def mouse_callback(event, x, y, flags, param):
    """
    Callback function to handle mouse events for displaying coordinates and cropping.
    """
    global cropping, start_point, end_point, image_display, highlighted_area

    # Clone the image to not overwrite the original
    if image is None:
        return

    image_display = image.copy()

    # Draw the highlighted area
    if highlighted_area:
        cv2.rectangle(image_display, highlighted_area[0], highlighted_area[1], (0, 0, 255), 2)

    # Calculate text position
    text_position_x = x + 10
    text_position_y = y

    # Check if text goes beyond image boundary
    text_size = cv2.getTextSize(f'({x}, {y})', cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
    if x + text_size[0] + 10 > image.shape[1]:
        text_position_x = x - text_size[0] - 10

    # Display mouse position on the image
    cv2.putText(image_display, f'({x}, {y})', (text_position_x, text_position_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2, cv2.LINE_AA)

    if event == cv2.EVENT_LBUTTONDOWN:
        # Record the starting coordinates
        cropping = True
        start_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping:
            # Draw a rectangle from start_point to the current mouse position
            cv2.rectangle(image_display, start_point, (x, y), (0, 255, 0), 2)
            # Display rectangle coordinates
            rect_coords = f'({start_point[0]}, {start_point[1]}) to ({x}, {y})'
            cv2.putText(image_display, rect_coords, (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

    elif event == cv2.EVENT_LBUTTONUP:
        # Record the ending coordinates
        cropping = False
        end_point = (x, y)

    # Show the image with coordinates and any cropping rectangle
    cv2.imshow('Image', image_display)

def highlight_area():
    """
    Function to input coordinates (x0, y0, x1, y1) and highlight the specified area on the image.
    """
    global highlighted_area, image_display

    # Prompt for coordinates in the console
    coord_input = input("Enter coordinates (x0, y0, x1, y1) separated by commas: ")

    try:
        # Parse the input string and convert to integers
        x0, y0, x1, y1 = map(int, coord_input.split(','))
        highlighted_area = ((x0, y0), (x1, y1))

        # Draw the highlighted area
        cv2.rectangle(image_display, (x0, y0), (x1, y1), (0, 0, 255), 2)
        cv2.imshow('Image', image_display)
    except ValueError:
        print("Invalid input. Please enter four numbers separated by commas.")

def main():
    # Initial screen capture
    capture_ldplayer_screen()

    # Create a window and bind the mouse callback function to it
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', mouse_callback)

    # Display the image
    while True:
        # Show the updated image
        if image_display is not None:
            cv2.imshow('Image', image_display)

        # Wait for a key press and handle specific keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c') and end_point != (0, 0):
            # Crop the region of interest and save when 'c' is pressed
            roi = image[start_point[1]:end_point[1], start_point[0]:end_point[0]]
            cv2.imwrite('cropped_image.png', roi)
            print("Cropped image saved as 'cropped_image.png'")
        elif key == ord('h'):
            # Open highlight area input dialog when 'h' is pressed
            highlight_area()
        elif key == ord('r'):
            # Capture the LDPlayer screen when 'R' is pressed
            capture_ldplayer_screen()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
