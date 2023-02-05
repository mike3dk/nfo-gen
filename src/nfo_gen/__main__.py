import argparse
import os
from pathlib import Path
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--input-directory",
        type=Path,
        required=True,
        help="Input directory with emergency responder GeoJSON files",
    )
    return parser.parse_args(argv)


def process(show_root):
    print(show_root.name)
    ## find the torrent file with this name

    ## extract the information

    current_dir = Path(__file__).parent
    tpl_path = current_dir / "templates/tvshow.nfo"
    print(tpl_path)

    environment = Environment(loader=FileSystemLoader("templates"))
    template = environment.get_template("tvshow.nfo")
    rendered = template.render(name=show_root.name)

    filename = show_root.parent / "tvshow.nfo"
    print(filename)
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(rendered)
        print(f"... wrote {filename}")


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    source = Path(args.input_directory).expanduser().resolve()
    print(f">>> nfo gen: {source}")

    for idx, path in enumerate(sorted(source.iterdir())):
        if not path.is_dir():
            continue
        print(idx, path)
        if idx > 1:
            continue

        process(path)


if __name__ == "__main__":
    main()
