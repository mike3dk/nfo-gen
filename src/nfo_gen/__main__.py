import argparse
import os
from pathlib import Path
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader
import pandas as pd

import src.ansicolor as c
from src.nfo_gen.read_gsheet import read_gsheet


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


def process(show_root, df):
    ## extract the information
    title = show_root.name
    print(f"{c.PURPLE}{title}{c.ENDC}")
    row_found = df.loc[df["title"] == title]
    info = (
        {"title": show_root.name}
        if row_found.empty
        else {
            "title": show_root.name,
            "year": row_found.iloc[0]["year"],
            "source": row_found.iloc[0]["source"],
            "tags": row_found.iloc[0]["tags"],
        }
    )
    environment = Environment(loader=FileSystemLoader("templates"))
    template = environment.get_template("tvshow.nfo")

    rendered = template.render(**info)

    filename = show_root / "tvshow.nfo"
    print(filename)
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(rendered)
        print(f"{c.YELLOW}>>> wrote {filename}{c.ENDC}")

    if row_found.empty:
        df2 = pd.DataFrame(info, index=[0], columns=df.columns)
        df = pd.concat([df, df2], ignore_index=True)
    return df


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    source = Path(args.input_directory).expanduser().resolve()
    print(f"{c.BLUE}>>> nfo gen: {source}{c.ENDC}")

    source_depth = len(source.parents)

    dframe = read_gsheet()
    for idx, path in enumerate(sorted(source.rglob("*"))):
        path_depth = len(path.parents) - source_depth
        if not path.is_dir() or path_depth != 2:
            continue
        print(idx, path, path_depth)
        dframe = process(path, dframe)

    print(f"{c.YELLOW}>>> wrote 'tvshows.csv'{c.ENDC}")
    dframe.to_csv("tvshows.csv", index=False)


if __name__ == "__main__":
    main()
