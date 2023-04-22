from PIL import Image
import os

def load_input_file():
    """Loads an input file from the input directory and returns the image"""
    filename = input("Enter the input file name: ")
    input_dir = "input"
    input_path = os.path.join(input_dir, filename)
    if not os.path.exists(input_path):
        print("Error: Input file does not exist.")
        return None
    return Image.open(input_path)

def create_composites(image):
    """Creates composites of the input image based on the number of rows and columns specified by the user"""
    patterns = [3, 4, 5]
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    for pattern in patterns:
        cols = rows = pattern
        width, height = image.size
        new_width = cols * width
        new_height = rows * height
        composite = Image.new("RGB", (new_width, new_height), (255, 255, 255))
        for row in range(rows):
            for col in range(cols):
                offset = (col * width, row * height)
                composite.paste(image, offset)
        filename = f"{os.path.splitext(os.path.basename(image.filename))[0]} - {cols}x{rows}.png"
        output_path = os.path.join(temp_dir, filename)
        composite.save(output_path)
        print(f"Composite saved to {output_path}")

def main():
    """Main function that prompts the user for the action to perform"""
    while True:
        action = input("Enter 'load' to load an input file or 'create' to create composites, or 'quit' to exit: ")
        if action == "load":
            image = load_input_file()
            if image is None:
                continue
            else:
                print("Image loaded successfully.")
        elif action == "create":
            try:
                create_composites(image)
            except NameError:
                print("Error: Input file not loaded. Please load an input file first.")
        elif action == "quit":
            break
        else:
            print("Error: Invalid input. Please enter 'load', 'create', or 'quit'.")

if __name__ == "__main__":
    main()