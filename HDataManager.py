#!/usr/bin/python3.3
# coding=utf-8
"""
Data manager module.
"""
__author__ = 'Hossein Noroozpour Thany Abady'
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import scale
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from HFile import HFile


class HDataManager():
    """
    Class for managing data.
    """
    def __init__(self, misimput='dni', trainfile='', testfile=''):
        self.classification_method = dict()
        self.model_selection_method = dict()
        self.tr = None
        self.ta = None
        self.te = None
        self.trfile = trainfile
        self.tefile = testfile
        if misimput == 'dvi':
            tr = HFile(trainfile)
            te = HFile(testfile)
            self.tr = tr.data
            self.ta = tr.classes
            self.te = te.data
        elif misimput == 'ir':
            tr = HFile(trainfile, ignore_undefined=True)
            te = HFile(testfile, ignore_undefined=True)
            self.tr = tr.data
            self.ta = tr.classes
            self.te = te.data
        elif misimput == 'mi':
            self.mean_impute()
        elif misimput == 'mei':
            self.median_impute()
        elif misimput == 'mfi':
            self.mfimput()
        else:
            raise Exception('Error: Unknown missing imputation method!')

    def mean_impute(self):
        """
        impute
        """
        tr = HFile(self.trfile)
        te = HFile(self.tefile)
        imp = Imputer(missing_values=-1)
        self.tr = imp.fit_transform(tr.data)
        self.ta = imp.fit_transform(tr.classes)
        self.te = imp.fit_transform(te.data)

    def median_impute(self):
        """
        impute
        """
        tr = HFile(self.trfile)
        te = HFile(self.tefile)
        imp = Imputer(missing_values=-1, strategy='median')
        self.tr = imp.fit_transform(tr.data)
        self.ta = imp.fit_transform(tr.classes)
        self.te = imp.fit_transform(te.data)

    def mfimput(self):
        """
        impute
        """
        tr = HFile(self.trfile)
        te = HFile(self.tefile)
        imp = Imputer(missing_values=-1, strategy='most_frequent')
        self.tr = imp.fit_transform(tr.data)
        self.ta = imp.fit_transform(tr.classes)
        self.te = imp.fit_transform(te.data)

    def standardize(self):
        """
        impute
        """
        self.tr = scale(self.tr)
        self.te = scale(self.te)

    def normalize(self):
        """
        impute
        """
        self.tr = normalize(self.tr)
        self.te = normalize(self.te)

    def do_pca(self, reduction_percentage=0.0):
        """
        impute
        :param reduction_percentage:
        """
        if len(self.tr[0]) != len(self.te[0]):
            raise Exception('Error in data!')
        n = int(len(self.tr[0]) * (100.0 - reduction_percentage))
        trpca = PCA(n).fit(self.tr)
        tepca = PCA(n).fit(self.te)
        self.tr = trpca.transform(self.tr)
        self.te = tepca.transform(self.te)
        print('Eigenvectors and eigenvalues for train set:')
        for i in range(len(trpca.explained_variance_)):
            print('\t', i, ': vector:', trpca.components_[i], '  value:', trpca.explained_variance_[i])
        print('Eigenvectors and eigenvalues for test set:')
        for i in range(len(tepca.explained_variance_)):
            print('\t', i, ': vector:', tepca.components_[i], '  value:', tepca.explained_variance_[i])

    def set_classification_method(self, method_name, method_parameter):
        """
        :param method_name:
        :param method_parameter:
        """
        print('Method name is:', method_name)
        for p in method_parameter.keys():
            print(p, ':', method_parameter[p])
        self.classification_method['name'] = method_name
        self.classification_method['parameters'] = method_parameter

    def set_model_selection_method(self, name, parameters):
        """
        :param name:
        :param parameters:
        """
        print('Method name is:', name)
        for p in parameters.keys():
            print(p, ':', parameters[p])
        self.model_selection_method['name'] = name
        self.model_selection_method['parameters'] = parameters