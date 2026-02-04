from module import Maze, generate, render
import sys

# Increase recursion limit for deep recursion in backtracking
sys.setrecursionlimit(10000)


def main():
    print("Testing Maze Module...")

    # Configuration
    width = 21
    height = 21
    entry = (1, 1)
    exit = (19, 19)
    seed = "test_seed"

    # Initialize
    print(f"Initializing {width}x{height} maze...")
    maze = Maze(width, height, entry, exit, seed=seed, perfect=True)

    # Place '42' (optional, but good to test if logically separated)
    # The place_42 method is in the class, so we can use it.
    res = maze.place_42()
    if res == 0:
        print("'42' pattern placed successfully.")
    else:
        print("'42' pattern skipped (maze too small).")

    # Generate
    print("Generating maze...")
    generate(maze)
    print("Generation complete.")

    # Render
    print("Rendering:")
    render(maze)

    print("Test passed!")


if __name__ == "__main__":
    main()
