# hpsb_case_study


## Getting Started

1. Download the files into a location on your computer.

2. Get the event.json and meta.json files in the same directory. 

3. Open your terminal

4. Find the documents in your local computer with cd. Example; 
```zsh
cd Desktop/data
```
5. Activate your python environment. Example;
```zsh
conda activate
```
6. Install dependencies
```zsh
pip install -r requirements.txt
```
7. Write the code below to run api process.
```zsh
uvicorn recommender:recommender --reload
```
8. Open local API docs [http://127.0.0.1:8000/docs](http://localhost:8000/docs)

9. When you reach the fast-api framework click "Post"

10. Click "Try it Out"

11. Write any product you want to get recommendation and hit execute. 

12. Wait for the finish and you can see the final results in response body. 
