from PIL import Image
import os

# Global variables
patterns = [2, 3, 4, 5]
temp_dir = 'temp'
output_dir = 'output'
products = {
    'Almofada': (2000, 1000),
    'Poster': (1000, 3000),
    'Testes': (2000, 2000)
}

def load_input_file():
    """Loads an input file from the input directory and returns the image"""
    filename = input("Enter the input file name: ")
    input_dir = "input"
    input_path = os.path.join(input_dir, filename)
    if not os.path.exists(input_path):
        print("Error: Input file does not exist.")
        return None
    return Image.open(input_path)

def create_temp_directory(temp_dir):
    """Creates the temporary directory if it doesn't already exist"""
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

def create_composites_from_image(image, patterns, temp_dir):
    """Creates composites from the input image and saves them to the temp directory"""
    create_temp_directory(temp_dir)
    dpi = 150
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
        composite.save(output_path, dpi=(dpi, dpi))
        print(f"Composite saved to {output_path}")

def create_output_directory(output_dir):
    """Creates the output directory if it doesn't already exist"""
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

def process_product_images(products, temp_dir, output_dir):
    """Resizes the composites ({image} - {cols}x{rows}) to the largest dimension of each product and then crop the excess
    then saves the resulting products images to the output directory as output/{product}/{image} - {cols}x{rows}.png"""
    create_output_directory(output_dir)
    for product, size in products.items():
        product_dir = os.path.join(output_dir, product)
        create_output_directory(product_dir)
        for filename in os.listdir(temp_dir):
            image = Image.open(os.path.join(temp_dir, filename))
            cols, rows = size
            width, height = image.size
            aspect_ratio = width / height
            canvas_ratio = cols / rows
            if aspect_ratio > canvas_ratio:
                new_height = rows
                new_width = int(rows * aspect_ratio)
                new_image = image.resize((new_width, new_height))
                x = (new_width - cols) // 2
                y = 0
            elif aspect_ratio < canvas_ratio:
                new_width = cols
                new_height = int(cols / aspect_ratio)
                new_image = image.resize((new_width, new_height))
                x = 0
                y = (new_height - rows) // 2
            else:
                new_image = image.resize((cols, rows))
                x = 0
                y = 0
            new_image = new_image.crop((x, y, x + cols, y + rows))
            output_path = os.path.join(product_dir, filename)
            new_image.save(output_path)
            print(f"Product {product} image saved to {output_path}")


def main():
    """Main function that prompts the user for the action to perform"""
    while True:
        action = input("Enter 'load' to load an input file, 'create' to create composites, 'crop' to crop composites, or 'quit' to exit: ")
        if action == "load":
            image = load_input_file()
            if image is None:
                continue
            else:
                print("Image loaded successfully.")
        elif action == "create":
            try:
                create_composites_from_image(image, patterns, temp_dir)
            except NameError:
                print("Error: Input file not loaded. Please load an input file first.")
        elif action == "crop":
            try:
                process_product_images(products, temp_dir, output_dir)
            except FileNotFoundError:
                print("Error: Composites not found. Please create composites first.")
        elif action == "quit":
            break
        else:
            print("Error: Invalid input. Please enter 'load', 'create', 'crop', or 'quit'.")

if __name__ == "__main__":
    main()