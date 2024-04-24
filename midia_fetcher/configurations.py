import socket

from pathlib import Path
from midia_fetcher.paths import MainzPaths
from midia_fetcher.ssh import SshSource
from midia_fetcher.aws import AwsSource
from midia_fetcher.local import Cache, DiskSource
from midia_fetcher.datasource import Chain


def get_configuration(name=None):
    if name is None:
        name = socket.gethostname()

    if name == "solace":
        ssh = SshSource("tuntiger", MainzPaths())
        aws = AwsSource()
        remote = Chain([ssh, aws])
        return Cache(remote, "/mnt/storage/science/midia_rawdata")
    elif name == "spot":
        remote = SshSource("tuntiger", MainzPaths())
        return remote
    elif name == "nighthaven":
        remote = SshSource("tuntiger", MainzPaths())
        return Cache(remote, "/mnt/storage/midia/rawdata")
    elif name == "tiger":
        remote = DiskSource(MainzPaths())
        return Cache(remote, "/mnt/btrfs/midia_cached_data")
    elif name == "midiaor":
        remote = DiskSource(MainzPaths())
        return Cache(remote, "/home/_common_/midia_cached_data")
    elif name == "pingu":
        ssh = SshSource("midia", MainzPaths())
        aws = AwsSource()
        remote = Chain([ssh, aws])
        return Cache(remote, "/home/matteo/msdata")
    else:
        aws = AwsSource()
        cache_folder = Path.home() / "msdata"
        cache_folder.mkdir(parents=False, exist_ok=True)
        return Cache(aws, str(cache_folder))
    raise NotImplementedError()
