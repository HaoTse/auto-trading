# Auto trading

## Prerequisite
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

> [official StockProfitCalculator](https://github.com/NCKU-CCS/StockProfitCalculator)

### usage
```shell
trader.py [-h] [--training TRAINING] [--testing TESTING]
                 [--output OUTPUT] [-s] [--score]
```

### optional arguments
```shell
-h, --help           show this help message and exit
--training TRAINING  input training data file name
--testing TESTING    input testing data file name
--output OUTPUT      output file name
-s, --select         feature selection mode
--score              compute score
```

## Method
輸入當天的 open, high, low, close 四個值作為 features，並將隔天的 open 作為 targets，將 （features, targets）做 linear regression 的訓練，發現成效不錯
```shell
Socre Training:  0.9951864824553518
Score Testing:  0.9909212274108665
```
因此使用 linear regression model 來預測隔天的 open price，並根據 stragety 來做動作


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
| mehtod       | profit |
| ------------ | ------ |
| buy-and-hold | 45.04  |
| trend        | 63.87  |

## Todo
- 使用 linear regression 雖然預測的成效分數不錯，但是可能會有預測結果與真實情況是差不多的，不過事實上會造成上漲或下跌的預測錯誤的情形，因此可以試著使用 classifer 的方法來預測會是上漲還是下跌來比較
