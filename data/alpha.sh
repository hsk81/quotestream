#!/usr/bin/env sh

##
## => {'timestamp': .., 'last': [117.77], 'log': [4.76]}
##

cat log/ticks-32k.log | ./py filter -e high low -e bid ask -e volume | ./py map.float -p last | ./py map.log -p last | ./py sim -a 0.001 | ./py zmq.push -a 'ipc:///tmp/0' -v > /dev/null

##
## => {'timestamp': .., 'last': [117.77], 'log': [4.76], 'diff': [0.0033], 'lhs-vola': [0.68]}
##

./py zmq.sub -a 'ipc:///tmp/0' | ./py interpolate -i 2.5 -v | ./py reduce.diff -p log -n 240 | ./py reduce.vola -p diff -r lhs-vola -n 240 > /tmp/ticks.lhs

##
## => {'timestamp': .., 'last': [117.77], 'log': [4.76], 'diff': [0.0033], 'rhs-vola': [0.76]}
##

./py zmq.sub -a 'ipc:///tmp/0' | ./py interpolate -i 3.0 -v | ./py reduce.dilog -n 200 | ./py reduce.vola -p diff -r rhs-vola -n 200 > /tmp/ticks.rhs


##
## => {'timestamp': .., 'last': [117.74], 'log': [4.76], 'diff': [0.0012], 'lhs-vola': [0.59], 'div': [0.54]}
##

cat /tmp/ticks.lhs | ./py zmq.push -a 'ipc:///tmp/0.lhs'
cat /tmp/ticks.rhs | ./py zmq.push -a 'ipc:///tmp/0.rhs'

./py zmq.pull -a 'ipc:///tmp/0.lhs' -a 'ipc:///tmp/0.rhs' | ./py interleave.divp lhs-vola rhs-vola -v > /tmp/ticks.div

##
## => {'timestamp': .., 'price': [117.8], 'log': [4.76], 'return': [0.0018], 'rhs-vola': [1.07], 'ratio': [1.15],
##     'btc': [0.09], 'tot': [100.76], 'usd': [89.43]}
##

cat /tmp/ticks.div | grep "rhs-vola" | ./py alias -m last price | ./py alias -m diff return | ./py alias -m div ratio | ./py strategy.alpha --fee=0.000 -v > /tmp/ticks.000

##
## => PNG: {(timestamp,log)   ; (timestamp,usd),
##          (timestamp,tot)   ; (timestamp,btc),
##          (timestamp,ratio) ; (timestamp,return)}
##

cat /tmp/ticks.000 | ./graph/plot.py -p timestamp log -p timestamp usd -p timestamp tot -p timestamp btc -p timestamp ratio -p timestamp return -n 2 > /dev/null

