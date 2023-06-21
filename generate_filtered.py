import os.path
import urllib.request
import pandas


def main():
    sort_exclude_list()  # Only needed to be run if exclude_list needs to be resorted (after adding IDs)
    generate_filtered()


def fetch_items(url, filename, skip_if_exists=True):
    """
    Download items-complete.json
    """
    if not skip_if_exists or not os.path.isfile(filename):
        print("Downloading " + filename)
        urllib.request.urlretrieve(url, filename)


def generate_filtered():
    # fetch item list if not already downloaded
    source_url = "https://raw.githubusercontent.com/osrsbox/osrsbox-db/dae12e3400add0c71465f07a334f9d8f86bebce8/docs/items-complete.json"
    input_filename = "items-complete.json"
    fetch_items(source_url, input_filename)

    # load item list for parsing
    df = pandas.read_json("items-complete.json")
    df = df.transpose()
    df = df.convert_dtypes()

    # Remove items tagged with:
    #  - "members"
    #  - "incomplete"
    #  - "noted"
    #  - "quest_item"
    #  - "stacked"
    #  - "duplicate"
    # Also remove IDs contained in exclude_list:
    #  - mistagged items (items which should have been tagged members, quest_item, etc)
    #  - clue-scroll-only rewards
    #  - unobtainable items
    #  - holiday event items
    #  - mini-game items
    #  - random-event items
    #  - etc
    exclude_list = pandas.read_csv("exclude_list.csv")
    df = df[
        (~df["members"])
        & (~df["incomplete"])
        & (~df["noted"])
        & (~df["quest_item"])
        & (df["stacked"].isnull())
        & (~df["duplicate"])
        & (~df["id"].isin(exclude_list["id"]))
    ]

    # keep relevant columns
    df = pandas.DataFrame(
        df,
        columns=[
            "id",
            "name",
            # "last_updated",
            # "incomplete",
            # "members",
            # "tradeable",
            # "tradeable_on_ge",
            # "stackable",
            # "stacked",
            # "noted",
            # "noteable",
            # "linked_id_item",
            # "linked_id_noted",
            # "linked_id_placeholder",
            # "placeholder",
            # "equipable",
            # "equipable_by_player",
            # "equipable_weapon",
            # "cost",
            # "lowalch",
            # "highalch",
            # "weight",
            # "buy_limit",
            # "quest_item",
            # "release_date",
            # "duplicate",
            # "examine",
            # "icon",
            # "wiki_name",
            "wiki_url",
            # "equipment",
            # "weapon",
        ],
    )
    df.set_index("id", inplace=True)

    # save
    df.to_csv("filtered.csv")


def sort_exclude_list():
    """
    read exclude_list.csv
    sort IDs
    write exlcude_list.csv
    """
    exclude_list = pandas.read_csv("exclude_list.csv")
    exclude_list.sort_values(by=["id"], inplace=True)
    exclude_list.to_csv("exclude_list.csv", index=False)


if __name__ == "__main__":
    main()
