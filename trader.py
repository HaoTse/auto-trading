import pandas as pd

class Trader:

    def train(self, dataset):
        print(dataset.head())

    def predict_action(self, row):
        return '1'

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
    with open(args.output, 'w') as output_file:
        for row in testing_data:
            # We will perform your action as the open price in the next day.
            action = trader.predict_action(row)
            output_file.write(action)

            # this is your option, you can leave it empty.
            # trader.re_training(i)