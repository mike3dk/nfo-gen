import pandas as pd


def read_gsheet():
    try:
        sheet_id = "1u264LBqXURcwJ6FEuJXgbqVBcvcHVG1ynBfNg6yImVQ"
        sheet_name = "list"
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

        return pd.read_csv(url, keep_default_na=False)
    except Exception as err:
        print(err)
