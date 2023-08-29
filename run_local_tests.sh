PYTHONPATH=$PWD
scons -i
UNIT_TEST="python -m unittest discover"

./selfdrive/test/test_fingerprints.py
echo "$UNIT_TEST common"
$UNIT_TEST common
echo "$UNIT_TEST opendbc/can"
$UNIT_TEST opendbc/can
echo "$UNIT_TEST selfdrive/boardd"
$UNIT_TEST selfdrive/boardd
echo "$UNIT_TEST selfdrive/controls"
$UNIT_TEST selfdrive/controls
echo "$UNIT_TEST selfdrive/monitoring"
$UNIT_TEST selfdrive/monitoring
#echo "$UNIT_TEST selfdrive/loggerd"
#$UNIT_TEST selfdrive/loggerd
echo "$UNIT_TEST selfdrive/car"
$UNIT_TEST selfdrive/car
#echo "$UNIT_TEST selfdrive/test"
#$UNIT_TEST selfdrive/test
echo "$UNIT_TEST selfdrive/locationd"
$UNIT_TEST selfdrive/locationd
#echo "$UNIT_TEST selfdrive/athena"
#$UNIT_TEST selfdrive/athena
echo "$UNIT_TEST selfdrive/thermald"
$UNIT_TEST selfdrive/thermald
#echo "$UNIT_TEST tools/lib/tests"
#$UNIT_TEST tools/lib/tests
