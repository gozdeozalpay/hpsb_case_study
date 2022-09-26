# hpsb_case_study


## Getting Started

1. Download the files into a location on your computer.

2. Open your terminal

3. Find the documents in your local computer with cd. Example; 
```zsh
cd Desktop/data
```
4. Activate your python environment. Example;
```zsh
conda activate
```
5. Install dependencies
```zsh
pip install -r requirements.txt
```
6. Write the code below to run api process.
```zsh
uvicorn recommender:recommender --reload
```
7. Open local API docs [http://127.0.0.1:8000/docs](http://localhost:8000/docs)
