"""Start the VaultCore banking console application."""

from pathlib import Path

from vaultcore.bank import Bank
from vaultcore.cli import run_console
from vaultcore.storage import CsvStorage


def main() -> None:
    data_folder = Path(__file__).parent / "data"
    bank = Bank(CsvStorage(data_folder))
    run_console(bank)


if __name__ == "__main__":
    main()
