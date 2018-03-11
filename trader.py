import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.feature_selection import f_regression


class Trader:
    __reg = linear_model.LinearRegression()
    __status = 0
    __buy_price = 0

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

    def selection(self, train_data, test_data):
        # process data
        train_features, train_targets = self.__process(train_data)
        test_features, test_targets = self.__process(test_data)
        # sklearn feature selection
        F_values, _ = f_regression(train_features, train_targets)

        # sort the column by f values
        features_and_f_values = list(zip(train_data.columns, F_values))
        features_and_f_values.sort(key=lambda x: x[1], reverse=True)

        # output the importance of features
        print(features_and_f_values)

        # compare the different of features
        features_num_seq = range(1, len(train_data.columns)+1)
        result_test_score = list()
        result_train_score = list()
        for num in features_num_seq:
            selected_features = [
                feature_and_f_value[0]
                for feature_and_f_value in features_and_f_values[:num]
            ]

            train_selected_features = train_features.loc[:, selected_features]
            test_selected_features = test_features.loc[:, selected_features]

            reg = linear_model.LinearRegression()
            reg.fit(train_selected_features, train_targets)

            result_train_score.append(reg.score(train_selected_features, train_targets))
            result_test_score.append(reg.score(test_selected_features, test_targets))

        # plot the result
        plt.plot(features_num_seq, result_train_score, marker='o', label='train')
        plt.plot(features_num_seq, result_test_score, marker='*', label='test')
        plt.xticks(features_num_seq)
        plt.legend()
        plt.xlabel('Number of features used')
        plt.ylabel('Score')
        plt.show()

    def predict_action(self, row):
        input_data = row.values.reshape(1, -1)
        # predict the open price of tomorrow
        tomorrow_price = self.__reg.predict(input_data)[0]

        # define variables
        today_price = row[0]
        gap = tomorrow_price - today_price

        # auto trading stragety
        if self.__status == 0 and gap > 0:
            self.__buy_price = today_price
            self.__status = 1
            return '1'
        elif self.__status == 1 and gap < 0 and tomorrow_price > self.__buy_price:
            self.__status = 0
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
    parser.add_argument('-s', '--select',
                        action='store_true',
                        help='feature selection mode')
    parser.add_argument('--score',
                        action='store_true',
                        help='compute score')
    args = parser.parse_args()
    
    # load data
    training_data = load_data(args.training)
    testing_data = load_data(args.testing)
    trader = Trader()

    if args.select:
        # feature selection
        trader.selection(training_data, testing_data)
    else:
        # training model
        trader.train(training_data, args.score)

        # output score
        if args.score:
            trader.test(testing_data)
        
        # output result
        with open(args.output, 'w') as output_file:
            for index, row in testing_data.iterrows():
                if index != 0:
                    output_file.write(action + '\n')
                action = trader.predict_action(row)

        # output message
        print('Successful output the stragety result to \'%s\'.' % args.output)