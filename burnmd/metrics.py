import pandas as pd

class Metrics:
    def __init__(self):
        self.num_indexes = 0
        self.data = {}

    def log_metrics(self, ind=-1, **kwargs):
        for metric_name, item in kwargs.items():
            if self.num_indexes == 0:
                self.data[metric_name] = [item]
                self.num_indexes += 1
                continue
            if metric_name not in self.data:
                self.data[metric_name] = [None] * self.num_indexes
            if len(self.data[metric_name]) < self.num_indexes:
                self.data[metric_name] += [None] * (self.num_indexes - len(self.data[metric_name]))
            if self.data[metric_name][ind] is None:
                self.data[metric_name][ind] = item
            elif ind == -1:
                self.data[metric_name].append(item)
                self.num_indexes += 1
            else:
                raise ValueError(f"Error: index of metric {metric_name} at {ind} already ocupied")
    
    def to_pandas(self):
        for k, v in self.data.items():
            if len(v) < self.num_indexes:
                v += [None] * (self.num_indexes - len(v))
        return pd.DataFrame.from_dict(self.data)
