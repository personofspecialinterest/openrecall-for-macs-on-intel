import os
import sys
import argparse

parser = argparse.ArgumentParser(description="OpenRecall")

parser.add_argument(
    "--storage-path",
    default=None,
    help="Path to store the screenshots and database",
)

parser.add_argument(
    "--primary-monitor-only",
    action="store_true",
    help="Only record the primary monitor",
    default=False,
)

args = parser.parse_args()


def get_appsupport_folder(app_name="openrecall"):
    if sys.platform == "darwin":
        home = os.path.expanduser("~")
        path = os.path.join(home, "Library", "Application Support", app_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


if args.storage_path:
    appsupport_folder = args.storage_path
    screenshots_path = os.path.join(appsupport_folder, "screenshots")
    db_path = os.path.join(appsupport_folder, "recall.db")
else:
    appsupport_folder = get_appsupport_folder()
    db_path = os.path.join(appsupport_folder, "recall.db")
    screenshots_path = os.path.join(appsupport_folder, "screenshots")

if not os.path.exists(screenshots_path):
    try:
        os.makedirs(screenshots_path)
    except:
        pass
