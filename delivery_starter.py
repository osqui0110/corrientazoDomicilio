from services.drone import Drone

_number_of_drones: int = 20


def start_drones():
    drones = []
    for i in range(1, _number_of_drones+1):
        drone = Drone(i)
        drone.start()
        drones.append(drone)
    for drone in drones:
        drone.join()


if __name__ == "__main__":
    start_drones()
