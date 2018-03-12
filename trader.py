import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.feature_selection import f_regression


class Trader:
    __reg = linear_model.LinearRegression()
    __status = 0
    __buy_price = [0]

    def __process(self, dataset):
        features = dataset.iloc[:-1]
        targets = dataset.loc[1:, 'open']

        return features, targets

    def train(self, dataset, output_score=False):
        features, targets = self.__process(dataset)

        reg = self.__reg
        reg.fit(features, targets)

        if output_score:
            print("Socre Training: ", reg.score(features, targets))

    def test(self, dataset):
        features, targets = self.__process(dataset)

        reg = self.__reg
        print("Score Testing: ", reg.score(features, targets))

    def predict_action(self, row):
        input_data = row.values.reshape(1, -1)
        # predict the open price of tomorrow
        tomorrow_price = self.__reg.predict(input_data)[0]

        # define variables
        today_price = row[0]
        gap = tomorrow_price - today_price

        # auto trading stragety
        if gap > 0:
            if self.__status == 1:
                return '0'
            self.__buy_price.append(today_price)
            self.__buy_price.sort()
            self.__status += 1
            return '1'
        elif gap < 0 and self.__status != -1 and tomorrow_price > self.__buy_price[-1]:
            if self.__status == -1:
                return '0'
            self.__buy_price.pop()
            self.__status -= 1
            return '-1'
        else:
            return '0'


def load_data(file_name):
    titles = ['open', 'high', 'low', 'close']
    df = pd.read_csv(file_name, delimiter=',', header=None)
    df.columns = titles
    
    return df


if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')
    parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')
    parser.add_argument('--score',
                        action='store_true',
                        help='display the model score')
    args = parser.parse_args()
    
    # load data
    training_data = load_data(args.training)
    testing_data = load_data(args.testing)
    trader = Trader()

    # training model
    trader.train(training_data, args.score)

    # output score
    if args.score:
        trader.test(testing_data)
    
    # output result
    action = 0
    with open(args.output, 'w') as output_file:
        for index, row in testing_data.iterrows():
            if index != 0:
                output_file.write(action + '\n')
            action = trader.predict_action(row)

    # output message
    print('Successful output the stragety result to \'%s\'.' % args.output)