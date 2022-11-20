from typing import Dict, Union


def validate_data(data: Dict[str, Union[float]]):
    if not isinstance(data, dict):
        return False, 'Wrong data format'
    for key, value in data.items():
        if not isinstance(key, str) and len(key) != 3:
            return False, f'Wrong key format: {key}'
        if not isinstance(value, (int, float)):
            return False, f'Wrong amount format: {key}: {value}'
    return True, None
