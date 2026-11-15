import tempfile
import unittest
from pathlib import Path

from vaultcore.bank import Bank
from vaultcore.cli import run_console
from vaultcore.storage import CsvStorage


class CliTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_folder = tempfile.TemporaryDirectory()
        self.bank = Bank(CsvStorage(Path(self.temp_folder.name)))

    def tearDown(self) -> None:
        self.temp_folder.cleanup()

    def run_with(self, answers):
        replies = iter(answers)
        output = []
        run_console(self.bank, lambda _prompt: next(replies), output.append)
        return "\n".join(output)

    def test_open_search_and_exit_flow(self):
        text = self.run_with(
            ["1", "Asha Rao", "9876543210", "Savings", "500", "5", "asha", "0"]
        )
        self.assertIn("Account opened successfully. Number: VA1001", text)
        self.assertIn("VA1001 | Asha Rao", text)
        self.assertIn("Thank you", text)

    def test_invalid_menu_option_does_not_crash(self):
        text = self.run_with(["99", "0"])
        self.assertIn("Invalid option", text)


if __name__ == "__main__":
    unittest.main()
