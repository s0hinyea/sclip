from dataclasses import dataclass

@dataclass
class Gunshot:
  rms_value: float
  rms_index: int
  sample_number: int
  timestamp: float

  