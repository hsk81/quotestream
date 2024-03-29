# Quote Stream - FX Streaming Engine

This project is about a trading system for Bitcoins intended to be applied to the [Bitstamp.net](http://bitstamp.net) exchange. But it can also be used with other exchanges and on other kind of time series provided these are offered via a JSON based API.

The basic idea of the system is to model the trading quotes as a stream/pipe of data, and offer small tools that take the stream, apply a specific operation to it and hand it over to the next tool in the processing chain.

This approach has been loosely inspired by the UNIX approach, where the whole system is simply a collection of simple commands that do their job well. A crucial difference is though the fact the UNIX commands work in general on a hierarchical file system as a source and/or target of data, whereas here the quote stream is used as a carrier of data instead.

## Installation

```sh
$ ./setup.sh && source ./bin/activate
```

```sh
[qs] $ ./setup.py install
```

## Quote Structure

The actual data in the stream is JSON-like, and some example quotations might look like the following:

```json
{"volume": "10482.13511879", "last": "117.80", "timestamp": 1368230343.756902, "bid": "117.15", "vwap": "117.52", "high": "119.98", "low": "109.20", "ask": "117.90", "open": "117.90"}
{"volume": "10482.48787536", "last": "117.90", "timestamp": 1368230351.260416, "bid": "117.90", "vwap": "117.92", "high": "119.98", "low": "109.20", "ask": "117.95", "open": "117.90"}
{"volume": "10479.48787536", "last": "117.90", "timestamp": 1368230353.784478, "bid": "117.90", "vwap": "117.93", "high": "119.98", "low": "109.20", "ask": "117.95", "open": "117.90"}
...
```

According to the official JSON specification the double quote delimiters `"` are mandatory, but each tool in the processing chain also accepts entries where single quote delimiters `'` are used. More importantly each of them *produces* tuples with single quote delimiters (due to some implementation details).

The structure of the tuple is arbitrary, except for `timestamp` which is always required. The `volume`, `high` and `low` values are for the last 24 hours; `last`, `bid` and `ask` contain the most recent values.

+ `last`: last BTC price;
+ `high`: last 24 hours price high;
+ `low`: last 24 hours price low;
+ `vwap`: last 24 hours volume weighted average price.;
+ `volume`: last 24 hours volume;
+ `bid`: highest buy order;
+ `ask`: lowest sell order.;
+ `timestamp`: Unix timestamp date and time;
+ `open`: first price of the day.

This composition is true for the initial, unprocessed quote stream: Except for `timestamp` each component can be removed or transformed; also new ones can be calculated and added to the quotes in the stream. In theory it is possible to remove the `timestamp`, but since most of the tools assume its presence it should not be.

## Tool Chain

Let's start with the most basic operation: Asking the exchange for quotes and recording them for later usage into a file. You do this with the `ticker` tool:
```sh
$ ./py ticker -v > log/ticks.log
```
This tool polls the exchange's ticker URL almost every second and stores the reported quotes in `log/ticks.log`; plus thanks to the `-v` (`--verbose`) switch the quotes are also printed on the terminal.

Each tool should have a `-h` (`--help`) switch, printing a short description what it's supposed to do and showing other optional or mandatory arguments. In the ideal case a tool should have optional arguments only, read from the standard input and write to the standard output.

Although not always possible following this philosophy allows for a quick and simple "plumbing" of different tools together in a chain. Mandatory options can in the most cases avoided by using reasonable defaults, for example:
```sh
$ ./py ticker -h
usage: ticker.py [-h] [-v] [-i INTERVAL] [-u URL]

Polls exchange for new ticks: The poll interval limits the maximum possible
tick resolution, so keeping it as low as possible is desired. But since the
exchange does impose a request limit per time unit it's not possible to poll
beyond that cap (without getting banned).

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         verbose logging (default: False)
  -i INTERVAL, --interval INTERVAL
                        seconds between polls (default: 1.000 [s])
  -u URL, --url URL     API (default: https://www.bitstamp.net/api/ticker/)
```

### Cat, Filter, Float, Logarithm, Simulate and Publish

Let's plunge into analyzing the following chain:

```sh
$ cat log/ticks.log | ./py filter -e high low -e bid ask -e volume | ./py map.float -p last | ./py map.log -p last | ./py sim -a 0.001 | ./py zmq.pub -v > /dev/null
```
It first takes the recorded ticks and prints them via the standard UNIX command `cat` to the standard output. Then in a second step, the `high`, `low`, `bid`, `ask` and `volume` components of each quote are *excluded* using the `filter` tool. In the next two steps the `last` value is mapped with `map.float` to a floating point number (from a string) and then with `map.log` to its logarithmic value.

The `simulate` tool ensures that the quote stream flows with a 1000 fold *acceleration* compared to its original real time speed. In this case the stream is actually slowed down, since otherwise without the simulator the tool chain would try  to process the stream as fast as possible, which is not always desirable since in general we'd like to have some CPU power left for other purposes.

Finally, with `zmq.pub` the stream is published on the default TCP port `tcp://*:8888`, where it can be subscribed to from a different terminal or even from a different machine (in the same network). With the help of this publisher we can fork a quote stream, and apply different tool chains to each sub-stream.

Since the quotes are now published, we suppress the standard output by wiring it to `/dev/null`. But we still would like to see that the stream is flowing and have therefore the `-v` (`--verbose`) switch activated. In contrast to the standard output the quotes' timestamps are formatted properly if we use the verbose switch; the actual publication keeps the UNIX timestamp format though!

As a summary, quotes provided to the tool chain as input look like this:

```json
{"volume": "10482.13511879", "last": "117.80", "timestamp": 1368230343.756902, "bid": "117.15", "vwap": "117.52", "high": "119.98", "low": "109.20", "ask": "117.90", "open": "117.90"}
```
The published output on the TCP port looks like this:

```json
{"timestamp": 1368230927.929788, "last": [117.80], "log": [4.768139014266231]}
```

And the output we see on the terminal looks like this:

```json
[2013-05-11 04:59:03.756901] {"timestamp": 1368230343.756902, "last": [117.80], "last": [4.768988271217486]}
```
We have thrown away everything we're not interested in and have mapped the `last` component with the *logarithm* function. The reason behind using the logarithm instead of the original value is due to some advantageous mathematical properties.

### Subscribe, Interpolate, Return, Volatility, Alias and Publish

Now, it's time to apply some advanced operations:

```sh
$ ./py zmq.sub | ./py interpolate -i 1.200 | ./py reduce.diff -p log -n 500 | ./py reduce.vola -p diff -n 500 | ./py alias -m vola lhs-vola | ./py zmq.pub -a "tcp://*:7777" -v > /dev/null ## "*" implies on any IP address
```

With `zmq.sub` we subscribe to the previously published stream by default assumed to be on the *local* machine at `tcp://127.0.0.1:8888`.

Then we create with `interpolate` a homogeneous time series by sampling the stream every 1.2 seconds. Inhomogeneous to homogeneous time series conversion is a big subject in algorithmic trading, because many of the higher level operators assume a homogeneous interval between each quote in the stream. But this is only achievable via interpolation: The current implementation simply takes the most recent tick for an interpolated quote and does not try something more advanced like a linear interpolation.

Once we have a homogeneous stream, we calculate for each quote with `reduce.diff` *overlapping* returns of the last corresponding 10 minutes (500 * 1.2 seconds). Calculating returns basically centers the time series around zero and plots only the consecutive (but overlapping) differences.

Based on the returns we can now calculate with `reduce.vola` the activity for each 10 minute window of the quote stream. By default the so called *annualized volatility* is delivered. Once the calculation is done, we *move* (rename) the `vola` component with `alias` to `lhs-vola` (to avoid later a name clash).

Finally we publish the stream again in a similar fashion like before; except this time we need to use the non default port `7777`, since the default has already been used.

Second volatility calculation:

```sh
$ ./py zmq.sub | ./py interpolate -i 1.000 | ./py reduce.diff -p log -n 600 | ./py reduce.vola -p diff -n 600 | ./py alias -m vola rhs-vola | ./py zmq.pub -a "tcp://*:9999" -v > /dev/null ## "*" implies on any IP address
```

For reasons to explained later we *repeat* the previous calculation, but this time our interpolation interval is 1.0 second, and we store the volatility in `rhs-vola`. The following image shows the effect of changing the interpolation interval and calculating the corresponding volatilities:

![Logs, Returns & Volatilies](./readme/lrv-111.png "Logarithms, Returns and Volatilities")

The plot shows the logarithm, return and volatility for *three* different interpolation interval values: Two of them are similar, but one is quite distinct. The observed effect is an apparent shift relative to each other. This makes sense since the larger the interpolation interval, the fewer the number of homogeneous ticks (since we sample less), and therefore the corresponding curves lag behind the ones with the smaller interpolation intervals.

### Double Subscribe, Ratio and Publish

So we have now *two* volatility time series, and would like to bring them together:

```sh
$ ./py zmq.sub -a "tcp://127.0.0.1:7777" -a "tcp://127.0.0.1:9999" | ./py interleave.div -p lhs-vola rhs-vola | ./py zmq.pub -a "tcp://*:7799" -v > /dev/null ## "*" implies on any IP address
```
First with `zmq.sub` we subscribe to *both* streams at `tcp://127.0.0.1:7777` and `tcp://127.0.0.1:9999`: The subscription is fair in the sense that it tries to take alternatively from each input queue as long as each queue has a quote to deliver.

The `interleave.div` divides the `lhs-vola` with `rhs-vola` values; since these two volatilities are slightly off from each other (due to different interpolations), we actually end up calculating a **trend indicator**: If the ratio is higher than one we have a positive or negative trend, if it hovers around one there is no trend, and if it is less then one then we should observe a mean reverting behavior. The following figure shows this quite clearly:

![Alpha Strategy](./readme/pnl-alpha[ratio=1.75|1.25].[fee=20].png "USD Price [B], Log Returns [R], PnL Percent [C], Volatility Ratio [M], BTC & USD Account [M&Y], Volatility [G]")

The figure shows a period of about 30 days, and has the following sub-plots charted:

+ The `blue` plot shows the original price for Bitcoins denominated in US dollars; the `red` plot show the logarithmic returns of the price; the `cyan` plot and the plot immediately below it with the two `magenta` and `yellow` plots show the performance and behavior of of a trading strategy which is based on the volatility ratio and which we'll analyze in detail below; the `magenta` plot (2nd column and row) shows the volatility ratio: it's not extremely clear cut, but when you look at the peaks which are above the value of 2.0 then you can observe  in most cases also a corresponding trend in the original price; the `green` plot displays the price volatility.

Once the trend indicator (named simply as `div`) is calculated, we publish it with `zmq.pub` on the port `7799` and print verbosely the current stream on the terminal.

### Subscribe, Grep and Alias

Now it's time to do some cleanup and renaming:

```sh
$ ./py zmq.sub -a "tcp://127.0.0.1:7799" | grep "rhs-vola" | ./py alias -m rhs-vola vola -v > data/lrv-ratio.log
```

We again start with `zmq.sub` and subscribe to our quote stream (which has by now already been processed quite a bit). Then we remove with the UNIX command `grep` the quotes with `lhs-vola`, since we don't need two volatility entries anymore, and rename the remaining `rhs-vola` with `alias` to simply `vola`.

It might be a little confusing why we did not use the `filter` tool to exclude `lhs-vola`; to understand why we need to look at the quote stream before and after this tool chain is applied to:

```json
[2013-05-11 10:01:16.631573] {"diff": [0.000512776696989], "div": [0.9458681141583831], "lhs-vola": [1.002482455930246], "log": [4.762515756711868], "timestamp": 1368248476.631574}
[2013-05-11 09:41:28.056668] {"diff": [0.013604480532464], "div": [0.9466786310311711], "log": [4.761575465152227], "rhs-vola": [1.058946957362173], "timestamp": 1368247288.056668}
[2013-05-11 09:41:28.056668] {"diff": [0.013604480532464], "div": [0.9474912350833481], "log": [4.761575465152227], "rhs-vola": [1.058038764698504], "timestamp": 1368247288.056668}
[2013-05-11 10:01:26.646501] {"diff": [0.000512776696989], "div": [0.9457270087825611], "lhs-vola": [1.000615836114313], "log": [4.762515756711868], "timestamp": 1368248486.646501}
[2013-05-11 09:41:28.056668] {"diff": [0.013604480532464], "div": [0.9465401920177001], "log": [4.761575465152227], "rhs-vola": [1.057129791796101], "timestamp": 1368247288.056668}
[2013-05-11 10:01:26.646501] {"diff": [0.000512776696989], "div": [0.944771148642325], "lhs-vola": [0.9987457276592241], "log": [4.762515756711868], "timestamp": 1368248486.646501}
...
```

As you can see the `lhs-vola` and `rhs-vola` quote stream are not really merged, but simply *interleaved*! Therefore just excluding `lhs-vola` would be the wrong approach, since then we'd end up with some quotes which don't have *any* volatility information left; that's why we have to completely remove on sub-stream and continue with the remaining one.

Well, after the application of the tool chain we get:

```json
[2013-05-11 09:41:28.056668] {"vola": [1.061764501517898], "timestamp": 1368247288.056668, "log": [4.761575465152227], "div": [0.9530805730440061], "diff": [0.013604480532464]}
[2013-05-11 09:41:28.056668] {"vola": [1.061430109754043], "timestamp": 1368247288.056668, "log": [4.761575465152227], "div": [0.9518803908740491], "diff": [0.013604480532464]}
[2013-05-11 09:41:28.056668] {"vola": [1.061095612610575], "timestamp": 1368247288.056668, "log": [4.761575465152227], "div": [0.950677177059818], "diff": [0.013604480532464]}
...
```

Finally, we print verbosely again the quote stream on the terminal, *and* we store our calculations into a file. We could have simply published it again and continued with the new quote stream, but I wanted to simulate based on the `ratio` and `vola` entries various trading strategies: It does not make sense to calculate again and again these two numbers during development. In a production environment wiring this stage of the quote stream directly with the next one (via `zmq.pub` and `zmq.sub`) makes of course sense, and such a buffering into a file is not required.

### Cat, Exponentiate, and Alpha Sim

Now it's time to run a simulation to test and analyze a relatively simple strategy:

```sh
$ cat data/lrv-ratio.log | ./py map.exp -p log | ./py trade.alpha -v > data/alpha.log
```
First, we access our stored (and processed) quote stream via the UNIX command `cat` and exponentiate the `last` entry the get the original `price`, which we also need in the decision process of our trading strategy. The input to `trade.alpha` looks then like:

```json
{"diff": [0.00025433428139200003], "timestamp": 1368232031.982519, "div": [0.9589355359453091], "vola": [0.350167924307066], "exp": [117.96999999999998], "log": [4.770430354853751]}
```
So, we have now the following components of a quote:

+ `exp`: the original, most recent price for a Bitcoin in US dollars;
+ `log`: the logarithm of the most recent price;
+ `diff`: 10 minute overlapping differences of `log`;
+ `vola`: 10 minute activity ("variance") of `diff`;
+ `div`: trend indicator with *one plus* for a trend, *around one* for no trend and *one minus* for a mean reverting time series;
+ `timestamp`: point in time when the quote has been generated.

Our trading strategy is simple and has only two rules:

1. If there is a strong trend (ratio > 2.50) then either buy Bitcoins for a positive trend or sell them for a negative one. For each trade use only 1/1000 of your current account balance.

2. If there is a weak or no trend (ratio < 1.25) then sell Bitcoins; again use only 1/1000 of the current account balance per trade.

The logic behind the first rule is to detect and follow a trend and buy/sell into it (if our account balance allows it). The second rule ensures that we're *not* exposed in Bitcoins whenever the market direction is uncertain: We forgo potential gains should the price suddenly go up, but we also minimize our potential losses in case of a major dip.

Since we know now how this particular strategy works, let's analyze it's performance (see previous figure 1st column, 2nd and 3rd row):

+ PnL percent: The `cyan` plot shows that the strategy seems to work; as long as there are from time to time larger movements (positive or sometimes also negative) we make a profit; but periods of little market activity are a loss.

+ USD and BTC balance: The `magenta` and `yellow` double plots show the development of our USD and BTC account balance. We started with 100 USD and 0 BTC; during strong positive trends the BTC balance went up and the USD went down; and otherwise we minimized our BTC exposure.

Another important point to mention are the *fees*: The above plots and performance returns are the results of a simulation with a fee rate of 20/1000. The overall performance at the end of 30 days is strongly dependent on the fee structure:

```
Fee % | 0.500  0.400  0.300  0.200  0.100  0.000
PnL % |-0.427 -0.190 +0.048 +0.286 +0.525 +0.765
```

Interestingly the 30-day PnL seems to depend *linearly* on the fee. Break even is achieved somewhere between a fee rate of 0.30 and 0.40 percent: Bitstamp.net allows you trade depending on your monthly volume as low as 0.22 percent, therefore based on this simple analysis a monthly return of 0.25 percent seems quite reasonable.

But of course 30 days of data does not tell us a lot! This analysis could e.g. be enhanced by using Monte Carlo simulations which would create time series which would qualitatively correspond to our price history. For each of these "alternate realities" we'd run our trading strategy and see how its profits/losses change.

On the other hand it is very encouraging to observe a very strong correlation between fees and profit: As long as the fees are sufficiently low, the bottom line should be positive (for almost *any* sub-period and/or price history).

## Improvement Options

There are three ways to improve this still basic trading system: One is w.r.t. *technology*, the other w.r.t. to the applied *mathematics*, and another w.r.t. the trading *strategy*. Let's investigate each option:

### Technology

The options here are vast, but I focus only on the most obvious ones. First, we'll look at how fast our solution is:

![Time Measurement - IPC/1GQPS](./readme/diff-t.e3.ipc.png "Less than 1 Giga Quotes per Second")

The measurement were taken using an optimized chain of tool chains:

```sh
$ head -n 8192 /tmp/ticks.log | ./py filter -e high low -e bid ask -e volume | ./py map.float -p last | ./py map.log -p last | ./py sim -a 0.001 | ./py zmq.pub -a 'ipc:///tmp/8888' > /dev/null
```
We copied our ticks to the `/tmp` folder to ensure they reside in RAM and we used the `ipc:///tmp/8888` UNIX socket for interprocess communication (instead of TCP); the effect of both of these changes were not measurable though. We took measurements only for the first `8192` quotes. Then we started the (modified) interpolation tool chains

```sh
$ ./py zmq.sub -a 'ipc:///tmp/8888' | ./py interpolate -i 5.0 | ./py reduce.diff -p log -n 120 | ./py reduce.vola -p diff -n 120 | ./py alias -m vola lhs-vola | ./py zmq.push -a "ipc:///tmp/7777" > /dev/null
```

and

```sh
$ ./py zmq.sub -a 'ipc:///tmp/8888' | ./py interpolate -i 6.0 | ./py reduce.diff -p log -n 100 | ./py reduce.vola -p diff -n 100 | ./py alias -m vola rhs-vola | ./py zmq.push -a "ipc:///tmp/9999" > /dev/null
```

which again use the IPC protocol instead of TCP; by interpolating less (every `5` or `6` seconds) we gained some significant performance. Further, we used the following tool chain

```sh
./py zmq.pull -a 'ipc:///tmp/7777' -a 'ipc:///tmp/9999' | ./py interleave.div -p lhs-vola rhs-vola | grep "rhs-vola" | ./py alias -m rhs-vola vola | ./py map.exp -p log | ./py map.now -r now | ./py filter -i timestamp now | ./py reduce.diff -p now -r dt > /tmp/dt.log
```

which combines the former three tool chains into a single one and measures how fast the quote stream is flowing using `map.now` and `reduce.diff`. We omitted `trade.alpha` (with the required `alias` renames) to investigate how fast the system can process the quote stream just *before* feeding it into the actual trading strategy; plus in all cases we omitted verbose printing.

Chain combination/merging did also help to improve performance by pushing the bulk of the measurements below `1`ms towards `0.1`ms. Our simulation tries to keep an average speed of `1`ms, but we observe a range between about `0.1`ms and `200`ms, where the average and median speeds are `6.53`ms and `0.15`ms. The share of speeds larger than `1`ms is `4.5%`.

This odd behavior might have an explanation: Python's garbage collector cleans up in regular intervals un-referenced objects from the memory; this process (or some other) causes these slowdowns to about `200`ms; to make up for this lost time the simulator accelerates the quote stream speed to about `0.1`ms and tries so to keep the average around the target speed of `1`ms. It fails in doing so because offsetting the median to `0.15`ms is not enough to bring down the average as much as desired.

Obviously this behavior is very much to be avoided, and we'd like to keep as many measurements as possible tightly around `1`ms (jitter reduction). This can probably be fixed by investigating Python's garbage collector, the processes running on the system during the simulation and/or the underlying [ZeroMQ](http://zeromq.org) transport layer.

These measurements show one fact very clearly though: If required the system has very much the capacity to run at a quote stream speed of `0.15`ms! Since the exchange itself delivers the quotes every `1-10` seconds, the current performance is more than enough for our purposes.

We could use another Python interpreter, e.g. [PyPy](http://pypy.org) which promises faster execution times. Further, rewriting and combining various tools within the different chains is another option (although it would be contrary to the *one tool for one task* approach). The quote stream uses JSON, which has longer parsing times compared to simpler position based message protocols; it is possible to replace it but we'd loose the great flexibility it offers compared to the others. Increasing the number of CPU cores might also have an effect, although during the simulation the available four cores were not used `100%`; other possibilities might be to increase CPU cache or to use faster RAM.

### Mathematics

Inhomogeneous to homogeneous time series conversion is not trivial and it would be preferable to have methods which calculate *directly* sophisticated quantities like volatilies or correlations.

This is possible thanks to convolution operators: Calculating these must be efficient, and therefore a full convolution is not feasible! But thanks to the *exponential moving average* (EMA) operator which can be constructed very quickly in an interative fashion, we can build a pleathora of complex but fast operators based upon it.

The basic definition of `EMA[τ;z]` is

```mma
EMA[t_{n}] := μ·EMA[t_{n-1}] + (1-μ)·z_{n-1};
```

with

```mma
μ := exp[-α]; α := (t_{n} - t_{n-1})/τ;
```

where

+ `τ` is a time range used here for scaling (between one minute and mutiple weeks); and
+ `z` is an inhomogeneous times series with `z_{n-1}` representing the previous tick.

So `EMA[t_{n}]` is then the *weighted average* of the last EMA and the previous tick. We've used here the *previous point* definiton which relies on the previous tick `z_{n-1}` instead of the next tick `z_{n}`.
