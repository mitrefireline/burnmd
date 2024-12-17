import hydra
from omegaconf import DictConfig, OmegaConf
from burnmd.historical_fire_utils import get_historical_error
from simfire.sim.simulation import FireSimulation
from simfire.utils.config import Config
from burnmd.metrics import Metrics
import imageio
import numpy as np
from hydra.utils import instantiate
from hydra.utils import get_method
import json

def get_simulator(cfg, scenario):
    cfg.historical.year = scenario["year"]
    cfg.historical.state = scenario["state"]
    cfg.historical.fire = scenario["fire"]
    sim_config = Config(config_dict=cfg)
    return FireSimulation(sim_config)


def get_hist_layer(cfg, scenario):
    cfg.historical.year = scenario["year"]
    cfg.historical.state = scenario["state"]
    cfg.historical.fire = scenario["fire"]
    sim_config = Config(config_dict=cfg)
    sim = FireSimulation(sim_config)
    return sim.config.historical_layer

@hydra.main(version_base=None, config_path="../conf", config_name="historical_evaluation")
def main(cfg: DictConfig) -> None:
    metrics = Metrics()
    with open(cfg.historical_fires_file, 'r') as f:
        scenarios = json.load(f)
    for scenario in scenarios:
        print(scenario)
        get_sim_func = get_method(cfg.simulator_initializer)
        sim = get_sim_func(cfg.simulator_config, scenario)
        hist_layer = get_hist_layer(cfg.hist_layer_config, scenario)
        images = get_historical_error(sim, hist_layer, metrics, fire_name=f"{scenario['state']}_{scenario['fire']}_{scenario['year']}")
        images *= 255
        print(list(images))
        imageio.mimsave(f"{scenario['state']}_{scenario['fire']}_{scenario['year']}.gif", list(images), loop=0, pilmode="RGB")
    metrics.to_pandas().to_csv("errors.csv")
        #with imageio.get_writer("test.gif", mode="I") as writer:
        #    for frame in images:
        #        writer.append_data(frame*255)

if __name__ == "__main__":
    main()
