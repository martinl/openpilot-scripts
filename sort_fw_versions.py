import pprint
from selfdrive.car.subaru.values import FW_VERSIONS, CAR
from cereal import car
Ecu = car.CarParams.Ecu

#pprint.pprint(dir(Ecu))
pprint.pprint(Ecu)

for model, fws in FW_VERSIONS.items():
    pprint.pprint(model)
    for ecu, fw in fws.items():
      ecu_type = ecu[0]
      pprint.pprint(ecu_type)
      pprint.pprint(fw)
