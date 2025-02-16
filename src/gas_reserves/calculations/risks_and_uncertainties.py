from src.gas_reserves.constants import SEISMIC_EXPLR_WORK_KRITERIAS, HYDROCARBON_PROPERTIES

SIDE_OF_SQUARE = 4000.0

def calculate_study_coef(values: dict, weights: dict) -> float:
    study_coef = 0
    for param in values:
        study_coef += weights[param] * values[param]
    return study_coef



def prepare_values(kriterias: dict,
                   area: float,
                   effective_thickness: float,
                   exploration_wells_amount: int,
                   ) -> dict:
    grid_density = SIDE_OF_SQUARE**2 / area * exploration_wells_amount

    core_research = (kriterias.get('core_research', 0) * SIDE_OF_SQUARE**2 / 3
                     / area / effective_thickness)
    return dict(
        seismic_exploration_work = SEISMIC_EXPLR_WORK_KRITERIAS[
            kriterias.get('seismic_exploration_work', 'Отсутствует')
        ],
        grid_density = grid_density if grid_density < 1 else 1,
        core_research = core_research if core_research < 1 else 1,
        c1_reserves = kriterias.get('c1_reserves', 0),
        hydrocarbon_properties = HYDROCARBON_PROPERTIES[
            kriterias.get('HYDROCARBON_PROPERTIES', 'Отсутствует')
        ]
    )


def prepare_weights(params: dict) -> dict:
    w_sum = 0
    for param in params.keys():
        w_sum += params[param]

    if w_sum != 1:
        for param in params.keys():
            params[param] = params[param] / w_sum

    if w_sum == 0:
        params = {param: 1/5 for param in params.keys()}

    return params
