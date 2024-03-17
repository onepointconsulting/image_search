# Image Search

Simple image and text vector based search implementation using models like Llava, Clip and OpenAI embeddings. Requires Ollama and OpenAI for semantic embeddings to be executed.

The CLIP model is used to generate image embeddings. Llava is used to describe image and OpenAI is used to provide semantic embeddings.

The backbone for search is a local LanceDB instance.

A REST API offers the core functionality:

- image upload
- text search (using OpenAI semantic embeddings)
- image search (using CLIP embeddings)
- combined text and image search (using OpenAI semantic embeddings and CLIP embeddings)
- image retrieval

You can view access the Swagger based REST documentation via:

```
http://<server>:<port>/docs
```

## Development instructions

Please make sure to install [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) first.

```bash
conda create -n multimodal_experiments python=3.12
conda activate multimodal_experiments
pip install poetry
poetry install
```

Make sure you install Ollama and get an OpenAI key. You will also require a .env file. See the .env_local file with the variables you need.

## Running Unit Tests

Here it is how you should run unit tests:

```
python -m unittest
```

## Bootstrap the DB

```
python .\image_search\bootstrap\initial_images_bootstrap.py
```

## Running the REST server

```
python .\image_search\rest\server.py
```

After starting the server you will be able to use the Swagger UI offered by FastAPI on: 
http://127.0.0.1:8888/docs

Using the Swagger UI you will be able to perform the basic operations for adding images and searching in different ways, as well as visualizing images.

## Configuration

The configuration for the project can be found in the `.env_local` file.