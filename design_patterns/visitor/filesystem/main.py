from file_system_element import File, DisplayVisitor, Directory, SizeCalculatorVisitor
# Client Code
def main():
    # Create files
    file1 = File("file1.txt", 1000)
    file2 = File("file2.txt", 2000)
    file3 = File("file3.jpg", 5000)
    file4 = File("file4.mp3", 3000)

    # Create directories and build the structure
    root = Directory("root")
    root.add(file1)
    root.add(file2)

    images = Directory("images")
    images.add(file3)
    root.add(images)

    music = Directory("music")
    music.add(file4)
    root.add(music)

    # Create visitors
    size_calculator = SizeCalculatorVisitor()
    display_visitor = DisplayVisitor()

    print("\n--- Displaying File Structure ---")
    root.accept(display_visitor)

    print("\n--- Calculating Total Size ---")
    root.accept(size_calculator)
    print(f"\nTotal size: {size_calculator.total_size} bytes")

if __name__ == "__main__":
    main()