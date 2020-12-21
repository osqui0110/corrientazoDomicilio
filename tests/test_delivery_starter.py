import os
from pathlib import Path
from unittest import mock

import delivery_starter
from tests import reports, valid_orders


@mock.patch.object(
    delivery_starter.Drone, "_report_dir_path",
    os.path.dirname(reports.__file__)
)
@mock.patch.object(
    delivery_starter.Drone, "_order_dir_path",
    os.path.dirname(valid_orders.__file__)
)
def test_start_drones():
    reports_dir = os.path.dirname(reports.__file__)
    delivery_starter.start_drones()
    files = [file for file in os.listdir(reports_dir) if file != "__init__.py" and file != "__pycache__"]
    assert len(files) == 20
    for file in files:
        os.remove(Path(reports_dir, file))

