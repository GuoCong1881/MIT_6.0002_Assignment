# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""




def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # TODO
    result = []
    for each in degs:
        coeffi = pylab.polyfit(x, y, each)
        result.append(coeffi)
    return result


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # TODO
    nomi = ((y - estimated)**2).sum()
    denomi = ((y - y.mean())**2).sum()
    r_squared = 1- nomi/denomi
    return r_squared

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    for i in range(len(models)):
        ye = pylab.polyval(models[i], x)
        r = round(r_squared(y, ye),3)
        deg = len(models[i])-1
        if deg==1:
            se = round(se_over_slope(x, y, ye, models[i]),3)
            plot_model(x, y, ye, deg, r, se)
        else:
            plot_model(x, y, ye, deg, r)

        
def plot_model(x, y, ye, deg, r, se=0):
    pylab.plot(x, y, 'bo', x, ye, 'r-')
    pylab.xlabel('years')
    pylab.ylabel('degree Celsius')
    if deg==1:
        pylab.title(str(deg) + ' degree regression model (R-square='+ str(r) +', SE/slope =' + str(se) + ')')
    else:
        pylab.title(str(deg) + ' degree regression model (R-square='+ str(r) +')')     
    pylab.show()
        
        
        
        
        
def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # TODO
    average = pylab.array([])
    for year in years:
        oyear = []
        for city in multi_cities:
            mcity = climate.get_yearly_temp(city, year).mean()
            oyear.append(mcity)
        myear = pylab.array(oyear).mean()
        average = pylab.append(average, myear)
    return average

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # TODO
    moving_average = pylab.array([])
    for i in range(len(y)):
        j = max(i - window_length + 1, 0)
        alli, k = 0, j
        while k <= i:
            alli += y[k]
            k += 1
        avgi = alli/(i - j + 1)
        moving_average = pylab.append(moving_average, avgi)
    return moving_average
        
def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # TODO
    rmse = (((y - estimated)**2).sum()/len(y))**(1/2)
    return rmse

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # TODO
    all_std = pylab.array([])
    for year in years:
        days = len(climate.get_yearly_temp('NEW YORK', year))
        each_year_overall = pylab.array([0]*days)
        for city in multi_cities:
            each_year_city = climate.get_yearly_temp(city, year)
            each_year_overall = each_year_city + each_year_overall
        each_year_avg = each_year_overall/len(multi_cities)
        each_year_std = pylab.std(each_year_avg)
        all_std = pylab.append(all_std, each_year_std)
    return all_std
        
        

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    for each in models:
        ye = pylab.polyval(each, x)
        r = round(rmse(y, ye),4)
        pylab.plot(x, y, 'bo', x, ye, 'r-')
        pylab.xlabel('years')
        pylab.ylabel('degree Celsius')
        pylab.title(str(len(each)-1)+' degree of regression model (rmse='+str(r)+')')
        pylab.show()

if __name__ == '__main__':

    file = r'D:\6.0002\Assignment\PS5\data.csv'
    climate = Climate(file)
    # Part A.4
    data1 = pylab.array([])
    data2 = pylab.array([])
    years = pylab.array(TRAINING_INTERVAL)
    for year in TRAINING_INTERVAL:
        temp1 = climate.rawdata['NEW YORK'][year][1][10]
        temp2 = climate.get_yearly_temp('NEW YORK', year).mean()
        data1 = pylab.append(data1, temp1)
        data2 = pylab.append(data2, temp2)
        
    model1 = generate_models(years, data1, [1])
    evaluate_models_on_training(years, data1, model1)
    model2 = generate_models(years, data2, [1])
    evaluate_models_on_training(years, data2, model2)
   
    
    # Part B
    
    data3 = gen_cities_avg(climate, CITIES, years)
    model3 = generate_models(years, data3, [1])
    evaluate_models_on_training(years, data3, model3)

    # Part C
    data4 = moving_average(data3, 5)
    model4 = generate_models(years, data4, [1])
    evaluate_models_on_training(years, data4, model4)

    # Part D.2
    model5 = generate_models(years, data4, [1,2,20])
    evaluate_models_on_training(years, data4, model5)
    
    years_test = pylab.array(TESTING_INTERVAL)
    test_avg = gen_cities_avg(climate, CITIES, years_test)
    test_ma = moving_average(test_avg, 5)
    evaluate_models_on_testing(years_test, test_ma, model5)
    # Part E
    dataE = moving_average(gen_std_devs(climate, CITIES, years),5)
    modelE = generate_models(years, dataE, [1])
    evaluate_models_on_training(years, dataE, modelE)
    
