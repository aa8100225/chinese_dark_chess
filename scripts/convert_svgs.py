import os

os.environ["DYLD_LIBRARY_PATH"] = "/opt/homebrew/lib:" + os.environ.get(
    "DYLD_LIBRARY_PATH", ""
)
os.environ["PKG_CONFIG_PATH"] = "/opt/homebrew/lib/pkgconfig:" + os.environ.get(
    "PKG_CONFIG_PATH", ""
)
import argparse
import cairosvg  # type: ignore


def convert_svg_to_png(directory: str, allow_overwrite: bool = False) -> None:
    abs_directory = os.path.abspath(directory)
    files = os.listdir(abs_directory)
    for file in files:
        if file.endswith(".svg"):
            full_path = os.path.join(abs_directory, file)
            png_filename = os.path.join(abs_directory, file.replace(".svg", ".png"))
            if not os.path.exists(png_filename) or allow_overwrite:
                cairosvg.svg2png(url=full_path, write_to=png_filename)
                print(f"Converted {file} to {png_filename}")
            else:
                print(f"File {png_filename} already exists, skipping conversion.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert SVG files to PNG format in a specified directory."
    )
    parser.add_argument(
        "directory", type=str, help="Directory to search for SVG files."
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Allow overwriting existing PNG files."
    )
    args = parser.parse_args()

    convert_svg_to_png(args.directory, args.overwrite)


if __name__ == "__main__":
    main()
