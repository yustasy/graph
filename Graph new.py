# импортируем flack и запускаем Web сервер
from flask import Flask, abort, request
import json
import datetime
from pprint import pprint
import requests
import shutil
import urllib.request
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# определяем начальные значения переменных

import pandas as pd

def plot(people):
    peoples = pd.read_csv(people+'.csv')
    peoples.info()
#    peoples['date_time'] = peoples.date_time.astype('float64')
#    peoples.info()
#    peoples['date_time'].value_counts().plot(kind="bar")
#    plt.show()
    sns.set_style('white')
    sns_plot = sns.barplot(x="date_time", y= 'количество людей в студии', data=peoples)
    sns_plot.set_xlabel("время дня",fontsize=10)
    sns_plot.set_ylabel("Число людей в поле зрения камеры",fontsize=10)
    sns_plot.tick_params(labelsize=5)
    plt.show()
    sns_plot.figure.savefig('pairplotnew.png')

plot('people')


