from unittest import TestCase
from pathlib import Path

from mythril.analysis.callgraph import generate_graph
from mythril.analysis.report import Report
from mythril.analysis.security import fire_lasers
from mythril.analysis.symbolic import SymExecWrapper
from mythril.ether import util
from mythril.ether.soliditycontract import SolidityContract

TEST_FILES = Path(__file__).parent / "testdata"

class GraphTest(TestCase):

    def test_generate_graph(self):
        for input_file in TEST_FILES.iterdir():
            if input_file.is_file and input_file.suffix == '.sol':
                contract = SolidityContract(str(input_file), name=None, solc_args=None)
                sym = SymExecWrapper(contract, address=(util.get_indexed_address(0)))
                issues = fire_lasers(sym)

                for issue in issues:
                    issue.add_code_info(contract)

                report = Report()
                for issue in issues:
                    report.append_issue(issue)

                html = generate_graph(sym)

                expected = (TEST_FILES / (input_file.name + ".graph.html")).read_text()
                self.assertEqual(html, expected)
