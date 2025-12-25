#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from two_stock_picker.crew import TwoStockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    inputs = {
        "sector": "Electric Vehicles",
        "year": datetime.now().year
    }

    crew = TwoStockPicker().crew()
    crew.kickoff(inputs)