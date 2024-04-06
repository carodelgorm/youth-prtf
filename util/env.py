import os

data_root = r"C:/"
DATA_PATH = os.path.join(
    data_root, "Users", "CarolynGorman", "OneDrive", "Research", "data"
)
REPO_PATH = os.path.join(data_root, "Users", "CarolynGorman", "OneDrive", "repos", 
                         "youth-rtc", "youth_rtc"
                         )


def data_path(*args):
    return os.path.join(DATA_PATH, *args)


def repo_path(*args):
    return os.path.join(REPO_PATH, *args)


def src_path(*args):
    return repo_path('src', *args)