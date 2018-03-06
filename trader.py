import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.feature_selection import f_regression

class Trader:
    reg = linear_model.LinearRegression()
    status = 0

    def __process(self, dataset):
        targets = dataset.loc[1:, 'open']
        features = dataset.iloc[:-1]

        return targets, features

    def train(self, dataset):
        targets, features = self.__process(dataset)

        reg = self.reg
        reg.fit(features, targets)

        # print("Socre Training: ", reg.score(features, targets))

    def test(self, dataset):
        targets, features = self.__process(dataset)

        reg = self.reg
        # print("Score Testing: ", reg.score(features, targets))

    def selection(self, train_data, test_data):
        train_targets, train_features = self.__process(train_data)
        test_targets, test_features = self.__process(test_data)
        F_values, _ = f_regression(train_features, train_targets)

        features_and_f_values = list(zip(train_data.columns, F_values))
        features_and_f_values.sort(key=lambda x: x[1], reverse=True)

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
        
        plt.plot(features_num_seq, result_train_score, marker='o', label='train')
        plt.plot(features_num_seq, result_test_score, marker='*', label='test')
        plt.xticks(features_num_seq)
        plt.legend()
        plt.xlabel('Number of features used')
        plt.ylabel('Score')
        plt.show()

    def predict_action(self, row):
        if self.status == 0:
            self.status = 1
            return '1'
        else:
            return '0'

    def re_training(self, i):
        print(i)

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
    args = parser.parse_args()
    
    load_data(args.training)
    # The following part is an example.
    # You can modify it at will.
    training_data = load_data(args.training)
    trader = Trader()
    trader.train(training_data)
    
    testing_data = load_data(args.testing)
    # trader.test(testing_data)

    # feature selection
    # trader.selection(training_data, testing_data)

    with open(args.output, 'w') as output_file:
        for index, row in testing_data.iterrows():
            # We will perform your action as the open price in the next day.
            action = trader.predict_action(row)
            output_file.write(action + '\n')

            # this is your option, you can leave it empty.
            # trader.re_training(i)