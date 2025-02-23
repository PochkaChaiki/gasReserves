from enum import Enum


ZERO_C_TO_K = 273
NORM_TEMP_C = 20
PRES_STD_COND = 0.101325 * 1e6

COEF_K = 3326400
ADIABATIC_INDEX = 1.3
PIPE_ROUGHNESS = 0.0001

SEISMIC_EXPLR_WORK_KRITERIAS = {
    '3D-сейсмика': 1,
    '2D-сейсмика': 0.5,
    'Отсутствует': 0,
}

HYDROCARBON_PROPERTIES = {
    'Есть': 1,
    'Отсутствуют': 0,
}

class RESULT(Enum):
    EVALUATION_ERROR = 0
    SUCCESS = 1
    PASSED_LIMIT = 2