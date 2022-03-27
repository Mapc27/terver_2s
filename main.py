import csv

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.datastructures import FormData
import uvicorn

from services import Statistics

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def create_upload_file(request: Request):
    a: FormData = await request.form()
    file = a['csv'].file.read()
    reader = csv.reader(file.decode().splitlines(), delimiter=',')
    data = list(zip(*reader))

    hrefs = []
    for array in data:
        statistics = Statistics(array=array)
        if statistics.ready():
            hrefs.append(f"/{statistics.get_index()}")
        else:
            del statistics

    return templates.TemplateResponse("index.html", {"request": request, "hrefs": hrefs})


@app.get("/{index}")
async def table(request: Request, index: int):
    statistics = Statistics.get_instance(index)
    if not statistics:
        return 404

    if not statistics.ready():
        return "Значения этого столбца не являются числом"

    script, div = statistics.get_plot_components()

    return templates.TemplateResponse("table.html", {
        "request": request,
        "name": statistics.name,
        "number": statistics.number,
        "min": statistics.min,
        "max": statistics.max,
        "interval_step": statistics.interval_step,
        "number_of_groups": statistics.number_of_groups,
        "intervals": statistics.intervals,
        "numbers_of_each_interval": statistics.numbers_of_each_interval,
        "mean_values": statistics.mean_values,
        "relative_frequencies": statistics.relative_frequencies,
        "sample_mean": statistics.sample_mean,
        "z": statistics.z,
        "z_2": statistics.z_2,
        "n_accumulated": statistics.n_accumulated,
        "z_3_multiplication_relative_frequencies": statistics.z_3_multiplication_relative_frequencies,
        "dispersion": statistics.dispersion,
        "standard_deviation": statistics.standard_deviation,
        "fashion": statistics.fashion,
        "median": statistics.median,
        "coefficient_of_asymmetry": statistics.coefficient_of_asymmetry,
        "coefficient_of_kurtosis": statistics.coefficient_of_kurtosis,
        "coefficient_of_variation": statistics.coefficient_of_variation,
        "confidence_interval_of_sample_mean": statistics.confidence_interval_of_sample_mean,
        "confidence_interval_of_dispersion": statistics.confidence_interval_of_dispersion,
        "the_script": script,
        "the_div": div,
        "list": statistics.list
    })
