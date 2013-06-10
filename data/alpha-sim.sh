cat log/ticks.log | ./filter.py -e high low -e bid ask -e volume | ./map/float.py -p last -r last | ./map/log.py -p last -r last | ./simulate.py -a 0.001 | ./zmq/pub.py -v > /dev/null

./zmq/sub.py | ./interpolate.py -i 1.200 | ./reduce/return.py -p last -r return -n 500 | ./reduce/volatility.py -p return -r volatility -n 500 | ./alias.py -m volatility lhs-volatility | ./zmq/pub.py -pub 'tcp://*:7777' -v > /dev/null

./zmq/sub.py | ./interpolate.py -i 1.000 | ./reduce/return.py -p last -r return -n 600 | ./reduce/volatility.py -p return -r volatility -n 600 | ./alias.py -m volatility rhs-volatility | ./zmq/pub.py -pub 'tcp://*:9999' -v > /dev/null

./zmq/sub.py -sub 'tcp://127.0.0.1:7777' -sub 'tcp://127.0.0.1:9999' | ./reduce/volatility-ratio.py -n lhs-volatility -d rhs-volatility -r ratio | ./zmq/pub.py -pub 'tcp://*:8080' -v > /dev/null

./zmq/sub.py -sub 'tcp://127.0.0.1:8080' | grep "rhs-volatility" | ./alias.py -m rhs-volatility volatility -v > data/lrv-ratio.log

cat data/lrv-ratio.log | ./map/exp.py -p last -r price | ./trade/alpha-sim.py -v > data/alpha-sim.log
