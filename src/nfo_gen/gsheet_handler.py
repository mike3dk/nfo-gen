from pathlib import Path

import pygsheets
import pandas as pd

app_root = Path(__file__).resolve().parent.parent.parent
cred_file = app_root / "cred/gsheet-777-22c1c6ad1e33.json"
gc = pygsheets.authorize(service_file=cred_file)
sheet_id = "1u264LBqXURcwJ6FEuJXgbqVBcvcHVG1ynBfNg6yImVQ"
gsheet = gc.open_by_key(sheet_id)
# sheet_name = "LearnVideoList"
# gsheet = gc.open(sheet_name)


def read_gsheet():
    try:
        # sheet_name = "source"
        # url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        # return pd.read_csv(url, keep_default_na=False)
        wks = gsheet[1]
        return wks.get_as_df()

    except Exception as err:
        print(err)


def write_gsheet(df):
    try:
        # sheet_name = "list"
        # url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

        wks = gsheet[0]
        wks.clear()
        wks.set_dataframe(df, (1, 1), nan="")
    except Exception as err:
        print(err)
