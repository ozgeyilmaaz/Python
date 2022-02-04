import numpy as np 

def MAPE(y , y_pred):
    return round(100*np.nanmean(np.abs(y - y_pred)/np.abs(y)),2)

def exponential_smoothing(x, alpha, l_zero, mape = False):
    if not 0 < alpha < 1:
        return "Invalid Alpha"
    else:
        x_forecast = np.full_like(x, np.nan)
        for t in range(1, len(x)):
            if t == 1:
                x_forecast[t] = alpha * x[t-1] + (1-alpha) * l_zero
            else:
                x_forecast[t] = alpha * x[t-1] + (1-alpha) * x_forecast[t-1]
        if mape == True:
            return (x_forecast, MAPE(x, x_forecast))
        else:
            return (x_forecast)
        
x = np.array([2.92, 0.84, 2.69, 2.42, 1.83, 1.22, 0.10, 1.32, 0.56, -0.35])
alpha = 0.3
l_zero = 2

print("Forecast: ", exponential_smoothing(x, alpha, l_zero))