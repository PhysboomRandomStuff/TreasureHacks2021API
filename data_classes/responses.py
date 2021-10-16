import json

class BaseResponse:
  def __init__(self,success=True,errors=[],warnings=[],info=[],json=""):
    self.success=success
    self.errors=errors
    self.warnings=warnings
    self.info=info
    self.json=json
    
  def to_json(self):
    return json.dumps(self, indent = 4, default=lambda o: o.__dict__)