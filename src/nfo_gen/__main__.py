import argparse
import os
from pathlib import Path
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader
import src.ansicolor as c


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
    rendered = template.render(title=show_root.name)

    filename = show_root / "tvshow.nfo"
    print(filename)
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(rendered)
        print(f"{c.YELLOW}... wrote {filename}{c.ENDC}")


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    source = Path(args.input_directory).expanduser().resolve()
    print(f"{c.BLUE}>>> nfo gen: {source}{c.ENDC}")

    source_depth = len(source.parents)

    for idx, path in enumerate(sorted(source.iterdir())):
        path_depth = len(path.parents) - source_depth
        if not path.is_dir() or path_depth != 1:
            continue
        print(idx, path, path_depth)
        process(path)


if __name__ == "__main__":
    main()
