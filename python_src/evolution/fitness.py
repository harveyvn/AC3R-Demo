import json
import time
from beamngpy import Road, Vehicle
from beamngpy.sensors import Damage
from models import RoadProfiler, BNGVehicle
from simulation import Simulation
import logging
logger = logging.getLogger(__name__)


class Fitness:
    @staticmethod
    def evaluate(deap_inds):
        def _collect_police_report():
            with open("./data/sample_report.json") as file:
                report_data = json.load(file)
            return report_data

        # Collect simulation data from CrashScenario object
        def _collect_sim_data(crash_scenario):
            # JSON READ: Building scenario's streets
            bng_roads = []
            for road in crash_scenario.roads:
                bng_road = Road('road_asphalt_2lane', rid=road.name)
                bng_road.nodes.extend(road.road_nodes)
                bng_roads.append(bng_road)

            bng_vehicles = []
            for vehicle in crash_scenario.vehicles:
                trajectory = vehicle.generate_trajectory()
                initial_position = (trajectory[0][0], trajectory[0][1], 0)
                v = Vehicle("scenario_player_" + str(vehicle.name),
                            model="etk800", licence=vehicle.name, color=vehicle.color)
                v.attach_sensor('damage', Damage())
                road_pf = RoadProfiler()
                road_pf.compute_ai_script(trajectory, vehicle.color)
                bng_vehicles.append(BNGVehicle(v, initial_position, None, vehicle.rot_quat, road_pf))

            return crash_scenario, bng_roads, bng_vehicles

        individual = deap_inds[0]
        crash_scenario, bng_roads, bng_vehicles = _collect_sim_data(individual)
        # Execute crash scenario and collect simulation's result
        simulation = Simulation(bng_roads, bng_vehicles)
        start_time = time.time()
        simulation.execute_scenario(time.time() + 60 * 1)
        logger.info("--- Simulation time: %s seconds ---" % (time.time() - start_time))
        crash_scenario.sim_report = simulation.get_report()

        # Fixed sample report data
        # TODO: change the sample police report to dynamic variable
        report_data = _collect_police_report()
        crash_scenario.cal_fitness(report_data)  # Calculate fitness score
        return crash_scenario.score,
