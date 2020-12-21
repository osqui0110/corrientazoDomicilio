# -*- coding: latin-1 -*-
import logging
import os
from enum import Enum
from pathlib import Path
from threading import Thread
from typing import Tuple, List

import orders
import reports

logging.basicConfig()
logger = logging.getLogger("deliver_starter")
logger.setLevel(logging.DEBUG)


class Cardinal(Enum):
    NORTH = "Norte"
    SOUTH = "Sur"
    EAST = "Este"
    WEST = "Oeste"

    @property
    def left(self):
        return {
            "Norte": Cardinal.WEST,
            "Sur": Cardinal.EAST,
            "Oeste": Cardinal.SOUTH,
            "Este": Cardinal.NORTH,
        }[self.value]

    @property
    def right(self):
        return {
            "Norte": Cardinal.EAST,
            "Sur": Cardinal.WEST,
            "Oeste": Cardinal.NORTH,
            "Este": Cardinal.SOUTH,
        }[self.value]

    @property
    def unit_vector(self):
        return {"Norte": (0, 1), "Sur": (0, -1), "Oeste": (-1, 0), "Este": (1, 0)}[
            self.value
        ]


class Direction:
    def __init__(self):
        self.__cardinal: Cardinal = Cardinal.NORTH

    def rotate_left(self):
        self.__cardinal = self.__cardinal.left

    def rotate_right(self):
        self.__cardinal = self.__cardinal.right

    @property
    def cardinal(self):
        return self.__cardinal

    @property
    def unit_vector(self):
        return self.__cardinal.unit_vector

    def restart(self):
        self.__cardinal = Cardinal.NORTH


class Drone(Thread):
    _max_distance = 10
    _max_load = 3
    _report_dir_path = os.path.dirname(reports.__file__)
    _order_dir_path = os.path.dirname(orders.__file__)

    def __init__(self, drone_id: int):
        assert drone_id > 0, "invalid id provided"
        Thread.__init__(self)
        self.__id: int = drone_id
        self.__location: Tuple[int, int] = (0, 0)
        self.__direction: Direction = Direction()
        self.__load = 0
        self.__set_instance_file_names()

    def __set_instance_file_names(self):
        file_str = "0" + str(self.__id) if self.__id < 10 else str(self.__id)
        self.__orders_file_name = f"in{file_str}.txt"
        self.__reports_file_name = f"out{file_str}.txt"

    def __advance(self):
        x: int = self.__location[0] + self.__direction.unit_vector[0]
        y: int = self.__location[1] + self.__direction.unit_vector[1]
        d: float = (x ** 2 + y ** 2) ** 0.5
        if d > self._max_distance:
            logger.error(f"La dirección {(x, y)} se encuentra fuera de rango.")
            return
        self.__location = (x, y)

    def __restart_position(self):
        self.__location = (0, 0)
        self.__direction.restart()

    def __unload_and_write_report(self):
        logger.info(f"Dron {self.__id} entregando almuerzo y notificando su posición!")
        self.__load -= 1
        file_path = Path(self._report_dir_path, self.__reports_file_name)
        with open(file_path, "a+") as f:
            if not f.tell():
                f.write("== Reporte de entregas ==\n")
            f.write(f"{self.__location} dirección {self.__direction.cardinal.value}\n")

    def __deliver_lunch(self, instruction: str):
        for char in instruction:
            if char == "A":
                self.__advance()
            elif char == "I":
                self.__direction.rotate_left()
            elif char == "D":
                self.__direction.rotate_right()
            else:
                # Invalid chars in files will just be ignored
                logger.error(f"{char} no es una opción válida como instrucción")
        self.__unload_and_write_report()
        if self.__load == 0:
            logger.info(f"Dron {self.__id} ha entregado su carga y volverá al local")
            self.__restart_position()

    def __deliver(self, deliveries_instructions: List[str]):
        deliveries_count: int = len(deliveries_instructions)
        logger.info(f"Dron {self.__id} entregando {deliveries_count} corrientazos!")
        self.__load = deliveries_count
        for instruction in deliveries_instructions:
            self.__deliver_lunch(instruction)

    def __slice_deliveries(self, content: List[str]):
        for job in range(0, len(content), self._max_load):
            yield content[job : job + self._max_load]

    def run(self):
        logger.info(f"Dron {self.__id} ha empezado su labor")
        file_path = Path(self._order_dir_path, self.__orders_file_name)
        with open(file_path) as f:
            content = f.read().splitlines()
            logger.info(f"Dron {self.__id} entregará {len(content)} corrientazos hoy")
            for deliveries in self.__slice_deliveries(content):
                self.__deliver(deliveries)
