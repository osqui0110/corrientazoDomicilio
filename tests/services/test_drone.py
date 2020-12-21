# -*- coding: latin-1 -*-
import os
from pathlib import Path

import pytest

from services.drone import Drone
from tests import reports, invalid_orders
from tests import valid_orders


def test_drone_valid_file():
    # Given a valid drone
    drone = Drone(1)
    drone._order_dir_path = os.path.dirname(valid_orders.__file__)
    drone._report_dir_path = os.path.dirname(reports.__file__)
    # No report file should exist; header and locations should be writen
    # Here we can see the actual locations resulting from the statement
    # In the statement the first direction was given to be North
    # Only one turn and drone initiated looking at North
    # Not possible to still be looking at North after one turn
    expected_file_lines = [
        "== Reporte de entregas ==",
        "(-2, 4) dirección Oeste",
        "(-1, 3) dirección Sur",
        "(0, 0) dirección Oeste",
    ]
    # When drone starts delivering
    drone.run()
    expected_file_path = Path(drone._report_dir_path, "out01.txt")
    # The expected report file exists
    with open(expected_file_path, encoding="latin-1") as f:
        content = f.read().splitlines()
        for lines in zip(content, expected_file_lines):
            # Lines are as expected
            assert lines[0] == lines[1], "Lines are actually different"
    # Clean reports dir
    os.remove(expected_file_path)


def test_drone_absent_file():
    # Given a drone with absent input file
    drone = Drone(2)
    drone._order_dir_path = os.path.dirname(invalid_orders.__file__)
    drone._report_dir_path = os.path.dirname(reports.__file__)
    # When drone starts delivering, an exception is raised
    with pytest.raises(FileNotFoundError):
        drone.run()


def test_drone_invalid_input():
    # Given a drone which input leads out of bounds and contains illegal chars
    drone = Drone(1)
    drone._order_dir_path = os.path.dirname(invalid_orders.__file__)
    drone._report_dir_path = os.path.dirname(reports.__file__)
    # Expected lines don't have locations out of bounds
    # Also, initial illegal chars "B" are ignored
    expected_file_lines = [
        "== Reporte de entregas ==",
        "(0, 5) dirección Norte",
        "(0, 10) dirección Norte",
        "(0, 10) dirección Norte",
    ]
    # When drone starts delivering
    drone.run()
    expected_file_path = Path(drone._report_dir_path, "out01.txt")
    # The expected report file exists
    with open(expected_file_path, encoding="latin-1") as f:
        content = f.read().splitlines()
        for lines in zip(content, expected_file_lines):
            # Lines are as expected
            assert lines[0] == lines[1], "Lines are actually different"
    # Clean reports dir
    os.remove(expected_file_path)
