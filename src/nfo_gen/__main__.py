import argparse
import subprocess
from pathlib import Path
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader
import pandas as pd

import ansicolor as c
from nfo_gen.gsheet_handler import read_gsheet, write_gsheet


class SplitArgs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(","))


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--input-directories",
        # type=List[Path],
        required=True,
        default=[],
        help="Input directories",
        action=SplitArgs,
    )
    return parser.parse_args(argv)


def process(title, path, df):
    ## extract the information
    print(f"{c.PURPLE}{title}{c.ENDC}")
    row_found = df.loc[df["title"] == title]
    info = (
        {"title": title, "found": "only in file"}
        if row_found.empty
        else {
            "title": title,
            "year": row_found.iloc[0]["year"],
            "source": row_found.iloc[0]["source"],
            "tags": " / ".join(
                [x.strip() for x in row_found.iloc[0]["tags"].split(",")]
            ),
            "author": row_found.iloc[0]["author"],
            "url": row_found.iloc[0]["url"],
            "image": row_found.iloc[0]["image"],
            "found": "yes",
        }
    )
    environment = Environment(loader=FileSystemLoader("templates"))
    template = environment.get_template("tvshow.nfo")

    rendered = template.render(**info)

    filename = f"{path}/tvshow.nfo"
    print(filename)
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(rendered)
        print(f"{c.YELLOW}>>> wrote {filename}{c.ENDC}")

    if row_found.empty:
        df2 = pd.DataFrame(info, index=[0], columns=df.columns)
        df = pd.concat([df, df2], ignore_index=True)
    else:
        df.loc[df["title"] == title, "found"] = "YES"

    return df


def clean(path, root):
    ret = path.replace(root, "")
    return ret.split("/")[-1]


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    sources = [Path(inpath).expanduser().resolve() for inpath in args.input_directories]
    source_depth = 1

    dframe = read_gsheet()
    dframe["found"] = "only in sheet"

    for source in sources:
        print(f"{c.BLUE}>>> nfo gen: {source}{c.ENDC}")
        ## using pythong rglob, too slow
        # for idx, path in enumerate(sorted(source.rglob("*"))):
        #     path_depth = len(path.parents) - source_depth
        #     if not path.is_dir() or path_depth != 2:
        #         continue
        #     print(idx, path, path_depth)
        #     dframe = process(path, dframe)

        cmd = f"find {source} -type d -mindepth {source_depth} -maxdepth {source_depth}"
        res = subprocess.check_output(cmd, shell=True)
        res = res.decode("utf-8")
        paths = res.splitlines()
        rows = [(clean(p, source.as_posix()), p) for p in paths]
        for idx, (title, path) in enumerate(sorted(rows)):
            print(idx, title, path)
            dframe = process(title, path, dframe)

    print(f"{c.YELLOW}>>> wrote 'tvshows.csv'{c.ENDC}")
    dframe.to_csv("tmp/tvshows.csv", index=False)
    write_gsheet(dframe)


if __name__ == "__main__":
    main()
