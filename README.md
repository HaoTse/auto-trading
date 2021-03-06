# Auto trading

## Prerequisite

### enviornment
- python 3.6.4

### requirements
```shell
pip install -r requirements.txt
```

## Command
```shell
$ python trade.py
```
會輸出 output.csv 檔案，接著執行
```shell
$ python calc.py
```
會輸出獲利成果

> [official Stock Profit Calculator](https://github.com/NCKU-CCS/StockProfitCalculator)

### usage
```shell
trader.py [-h] [--training TRAINING] [--testing TESTING]
                 [--output OUTPUT] [--score]

optional arguments:
  -h, --help           show this help message and exit
  --training TRAINING  input training data file name
  --testing TESTING    input testing data file name
  --output OUTPUT      output file name
  --score              display the model score
```

```shell
calc.py [-h] [--strategy STRATEGY] [--trading TRADING]

optional arguments:
  -h, --help           show this help message and exit
  --strategy STRATEGY  input action file name
  --trading TRADING    input stock file name
```

## Method
輸入當天的 open, high, low, close 四個值作為 features，並將隔天的 open 作為 targets，將 （features, targets）做 random forest regression 的訓練，發現成效不錯
```shell
Socre Training:  0.9987994882767667
Score Testing:  0.9748482213863732
```
因此使用 regression model 來預測隔天的 open price，並根據 stragety 來做動作

- 測試使用 classification 的方法發現準確度不如 regression，猜測此 data 分佈較符合 regression 的特性

## Strategy
### buy-and-hold (baseline)
- 一開始購買一張股票 hold 到最後

### trend
從 training data 的趨勢可以發現
- 若隔天下跌的話，前面有機會已經上漲了很長的時間
- 相反的，若隔天上漲的話，前面可能已經下跌一陣子了，並且接下來有機會持續上漲
![Imgur](https://i.imgur.com/Il3Z2Ct.png)

因此制定策略為
1. 當預測股市上漲時，就買入股票
2. 當預測股市下跌時，會認為是長到最高點後開始下跌，判斷此時賣出若為賺錢就將股票賣出

## Result
| strategy     | profit |
| ------------ | ------ |
| buy-and-hold | 45.04  |
| trend        | 131.48 |

- 因為 random forest 的每次結果都不同，因此這裡的結果是由 10 次平均而來的，運行 10 次的結果如下
```shell
Profit: 143.37747199999984
Profit: 118.63338999999979
Profit: 123.29311999999982
Profit: 117.11340499999977
Profit: 110.44665399999997
Profit: 113.76510499999995
Profit: 123.09441999999979
Profit: 140.64031999999992
Profit: 157.10815399999973
Profit: 167.3366409999996
```