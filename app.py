

from flask import Flask, jsonify, render_template, request

from bokeh.embed import components
from bokeh.plotting import figure

import pickle
import numpy as np


app = Flask(__name__)


# function to create time steps
def create_time_steps(length):
    return list(range(-length, 0))


# function to create input data
def make_data(d_hist, d_pred, data):
    hist, true, pred, base = data[d_hist][d_pred][0], \
                data[d_hist][d_pred][1], data[d_hist][d_pred][2], \
                data[d_hist][d_pred][3]

    return hist, true, pred, base


# function to calculate model prediction errors
def model_score_rmse(true, pred):
    metric_rmse = np.sqrt(np.square(np.subtract(true, pred)).mean())
    metric_cv_rmse = (metric_rmse / true.mean()) * 100

    return metric_cv_rmse


# create plot
def bokeh_plot(hist, true, pred, base):
    # create an empty plot
    p = figure(
        plot_width = 800,
        plot_height = 300,
        x_axis_label='Time (Hour)',
        y_axis_label='Electricity Load (kWh)'
    )

    num_in = create_time_steps(len(hist))
    num_out = len(true)

    # plot lines
    p.line(num_in, np.expm1(hist),
            legend_label = "History", line_color = 'blue')
    p.line(np.arange(num_out), np.expm1(true),
           legend_label = "True Future", line_color = 'red')
    p.circle(np.arange(num_out), np.expm1(pred), fill_color = "green",
             line_color = "green", legend_label="Predicted Future (New Model)", size = 6)
    p.circle(np.arange(num_out), np.expm1(base), fill_color = "orange",
             line_color = "orange", legend_label="Predicted Future (Baseline)", size = 6)

    p.legend.location = "top_left"
    p.sizing_mode = "scale_both"

    # render template
    script, div = components(p)

    return script, div


def load_data():
    file = open("plot.pkl", "rb")
    data_to_plot = pickle.load(file)
    file.close()
    return data_to_plot


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)

    hist_day = a
    pred_day = b

    # load raw data
    data_to_plot = load_data()

    # creat input data for bokeh plotting
    hist, true, pred, base = make_data(hist_day, pred_day, data_to_plot)

    # calculate model prediction errors
    baseline_error = model_score_rmse(np.expm1(true), np.expm1(base))
    new_model_error = model_score_rmse(np.expm1(true), np.expm1(pred))
    error_results = {'baseline': "{:.2f}".format(baseline_error),
                     'new_model': "{:.2f}".format(new_model_error)}
    
    # bokeh plotting
    script, div = bokeh_plot(hist, true, pred, base)

    return jsonify(baseline_error = error_results['baseline'],
           newmodel_error = error_results['new_model'],
           html_plot = render_template('update_plot.html',
                                     div_bok=div, script_bok=script))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
