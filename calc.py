import pandas as pd

def load_data(filename):
    df = pd.read_csv(filename, delimiter=',', header=None)
    return df

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--strategy',
                        default='output.csv',
                        help='input strategy file name')
    parser.add_argument('--trading',
                        default='testing_data.csv',
                        help='input trading data file name')
    args = parser.parse_args()

    strategy_data = load_data(args.strategy)
    trading_data = load_data(args.trading).iloc[1:, [0, 3]]

    total = 0
    status = 0
    for index, row in strategy_data.iterrows():
        if row[0] == 1:
            status += 1
            total = total - trading_data.iloc[index, 0]
        elif row[0] == -1:
            status -= 1
            total = total + trading_data.iloc[index, 0]
        else:
            continue

    if status == 1:
        total += trading_data.iloc[-1, 1]
    elif status == -1:
        total -= trading_data.iloc[-1, 1]        

    print('Profit: ' + str(total))