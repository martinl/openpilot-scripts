UNIT_TEST="python -m unittest discover"
scons -j$(nproc) --test 
./selfdrive/test/test_fingerprints.py
$UNIT_TEST common
$UNIT_TEST opendbc/can
$UNIT_TEST selfdrive/boardd
$UNIT_TEST selfdrive/controls
$UNIT_TEST selfdrive/monitoring
$UNIT_TEST selfdrive/loggerd
$UNIT_TEST selfdrive/car
$UNIT_TEST selfdrive/locationd
$UNIT_TEST selfdrive/athena
$UNIT_TEST selfdrive/thermald
$UNIT_TEST tools/lib/tests
./selfdrive/common/tests/test_util
./selfdrive/camerad/test/ae_gray_test
