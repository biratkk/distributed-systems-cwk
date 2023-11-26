import logging
from sensor import generate_random_data
from matplotlib import pyplot as plt

import matplotlib
import matplotlib.image as img

matplotlib.use("agg")
import azure.functions as func
import time
import base64
import io

x_label = "Number of sensor groups"
y_label = "Time taken (ns)"


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Triggered HTTP Request trigger")

    num_of_generations = req.params.get("generate_quantity")

    if num_of_generations is None:
        return "Please make sure that there is a generate_quantity parameter"

    generation_list = [int(x) for x in num_of_generations.split(",")]
    time_taken_list = []

    for num_gen in generation_list:
        start_time = time.perf_counter_ns()
        for _ in range(num_gen):
            generate_random_data()
        end_time = time.perf_counter_ns()
        time_taken_list.append(end_time - start_time)

    fig, ax = plt.subplots()
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.scatter(generation_list, time_taken_list, c="black")
    ax.plot(
        generation_list,
        time_taken_list,
    )

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_bytes = buf.getvalue()
    return func.HttpResponse(body=img_bytes, mimetype="image/jpeg")
