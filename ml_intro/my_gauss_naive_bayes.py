import numpy as np
import scipy.stats as stats


class My_Gauss_Naive_Bayes():
    def __init__(self):
        pass
    
    def fit(self, X ,y):
        data = np.concatenate((X,y.reshape(-1,1)), axis=1)
        
        #extract labels, count class labels and calculate class frequencies
        self.labels, class_count = np.unique(y, return_counts=True)
        self.class_frequencies = class_count / len(y)
        
        #get number of features
        feature_number = data.shape[1] - 1
        
        #concatenate training set with labels
        data = np.concatenate((X,np.expand_dims(y,axis=1)),axis=1)
        
        #define arrays, where i will save for each feature conditional mean and std respectively.
        self.cond_mean_arr = np.empty((len(self.labels),feature_number))
        self.cond_std_arr = np.empty((len(self.labels),feature_number))      
        
        #for each feature i calculate mean da std conditioned on label. 
        #for each feature i fit normal distribution's mean and std and save them to cond_mean_arr and cond_std_arr.
        for k, lab in enumerate(self.labels):
            for i in range(feature_number):
                self.cond_mean_arr[k,i], self.cond_std_arr[k,i] = stats.norm.fit(data[data[:,-1]==lab,i])
    
    
        #same as above, but now for each feature i calculate unconditional mean and std.
        self.mean_arr = np.empty((feature_number,))
        self.std_arr = np.empty((feature_number,))

        for i in range(feature_number):
            self.mean_arr[i], self.std_arr[i] = stats.norm.fit(data[:,i])
            
    
    def predict(self,x):
        cond_prior = stats.norm.pdf(x, loc = self.cond_mean_arr, scale = self.cond_std_arr).prod(axis=1)
        uncond_prob = stats.norm.pdf(x, loc = self.mean_arr, scale = self.std_arr).prod(axis=1)
        result = cond_prior * self.class_frequencies / uncond_prob
        
        return self.labels[np.argmax(result)]
        