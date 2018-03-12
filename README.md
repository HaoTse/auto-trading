# Auto trading

## Run
```shell
$ python trade.py
```
會輸出 output.csv 檔案，接著執行
```shell
$ python calc.py
```
會輸出獲利成果

- `$ python trade.py --score` 可輸出 train 及 test 的 score
- `$ python trade.py -s` 或 `$ python trade.py --select` 可觀察選擇參數的比較結果

## Strategy
### buy-and-hold (baseline)
- 一開始購買一張股票 hold 到最後

### greedy
1. 保持自己手上一定有一張股票
2. 當股市開始下跌時，會認為是長到最高點後開始下跌，判斷此時賣出若為賺錢就將股票賣出
3. 其他時候就保持持有一張股票的狀態

## Result
| mehtod       | profit |
| ------------ | ------ |
| buy-and-hold | 45.04  |
| greedy       | 63.87  |