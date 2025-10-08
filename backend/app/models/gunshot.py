from dataclasses import dataclass

@dataclass
class Gunshot:
  rms_value: float
  rms_index: int
  luminance: float
  sample_number: int
  timestamp: float

  