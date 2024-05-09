from typing import Annotated

import io
import matplotlib

matplotlib.use('AGG')
import matplotlib.pyplot as plt
from fastapi import FastAPI, Response, BackgroundTasks

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Annotated[str | None, "Buenas noches"]):
    return {"item_id": item_id, "q": q}


def create_img():
    plt.rcParams['figure.figsize'] = [7.50, 3.50]
    plt.rcParams['figure.autolayout'] = True
    fig = plt.figure(
    )  # make sure to call this, in order to create a new figure
    plt.plot([1, 2])
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    plt.close(fig)
    return img_buf


@app.get('/img')
def get_img(background_tasks: BackgroundTasks):
    # img_buf = create_img()
    img_buf = bars_graph()
    background_tasks.add_task(img_buf.close)
    headers = {'Content-Disposition': 'inline; filename="out.png"'}
    return Response(img_buf.getvalue(),
                    headers=headers,
                    media_type='image/png')


def bars_graph():
    plt.rcParams['figure.figsize'] = [7.50, 3.50]
    plt.rcParams['figure.autolayout'] = True
    fig = plt.figure(
    )  # make sure to call this, in order to create a new figure

    fig, ax = plt.subplots()
    fruits = ['Pepito', 'Juanita', 'Fabian', 'Lukas']
    counts = [40, 100, 30, 55]
    bar_labels = ['red', 'blue', '_red', 'orange']
    bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']
    ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

    ax.set_ylabel('fruit supply')
    ax.set_title('Fruit supply by kind and color')
    ax.legend(title='Fruit color')

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    plt.close(fig)
    return img_buf
