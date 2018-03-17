import random
from numpy import mean, sum

def IsNumeric(input):
    try:
        float(input)
        return True
    except (ValueError, TypeError):
        return False


class RegressionTree:
    def fit(self, feature_set, label_set, resolution):
        self.min_size = resolution
        self.tree = self.split(feature_set, label_set)
    
    def split(self, feature_set, label_set):
        if (len(feature_set) <= self.min_size):
            return mean(label_set)
        feature_count = len(feature_set[0])
        sortable_split = []
        for j in range(feature_count):
            for i in range(len(feature_set)):
                s = feature_set[i][j]
                #attempt split
                y1_average = mean([label_set[k] for k in range(len(feature_set)) if feature_set[k][j] < s])
                y2_average = mean([label_set[k] for k in range(len(feature_set)) if feature_set[k][j] >= s])
                y1_deviation = sum([label_set[k] * label_set[k] - y1_average * y1_average for k in range(len(feature_set)) if feature_set[k][j] < s])
                y2_deviation = sum([label_set[k] * label_set[k] - y2_average * y2_average for k in range(len(feature_set)) if feature_set[k][j] >= s])
                sortable_split.append((j,s,y1_deviation + y2_deviation))
        sortable_split = sorted(sortable_split, key=lambda x: x[2], reverse=False)
        sortable_split = sortable_split[0]
        #select the most efficient split
        lower_step = self.split(*zip(*[(feature_set[k],label_set[k]) for k in range(len(feature_set)) if feature_set[k][sortable_split[0]] < sortable_split[1]]))
        upper_step = self.split(*zip(*[(feature_set[k],label_set[k]) for k in range(len(feature_set)) if feature_set[k][sortable_split[0]] >= sortable_split[1]]))
        return ((sortable_split[0], sortable_split[1]), lower_step, upper_step)

    def predict(self, feature_set):
        predictions=[]
        for i in range(len(feature_set)):
            features = feature_set[i]
            view = self.tree
            while(True):
                split_node , lower_step, upper_step = view
                feature_index, threshold = split_node  
                feature_value = features[feature_index]
                if (feature_value < threshold):
                    view = lower_step
                else:
                    view = upper_step
                if (IsNumeric(view)):
                    predictions.append(float(view))
                    break
        return predictions

def generate_equation():
    a = random.randrange(0,100)
    b = random.randrange(0,100)
    c = random.choice(['+','-'])
    res = (a+b) if (c=='+') else (a-b)
    return str(a).zfill(2) + c + str(b).zfill(2), res

def serialize(str_input):
    l = []
    for c in str_input:
        try:
            ans = float(c)
            l.append(int(ans))
        except (ValueError, TypeError):
            if (c=='+'): l.append(0)
            if (c=='-'): l.append(1)

    return l

sample_size=2000
validation_size = 400

sample_set, label_set = zip(*[generate_equation() for x in range(sample_size)])
validation_set, validation_labels = zip(*[generate_equation() for x in range(validation_size)])

sample_set_serialized, validation_set_serialized = [serialize(x) for x in sample_set],[serialize(x) for x in validation_set]

classifier = RegressionTree()
classifier.fit(sample_set_serialized, label_set, 10)

for a in range(10):
    res = classifier.predict([validation_set_serialized[a]])
    res = str(res[0])
    print(str(validation_set[a]) + "=" + res)

