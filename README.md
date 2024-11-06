# Chess-Evaluation-Model

Chess game with opponent (black) as Machine learning model that evaluates board and plays optimal move, trained on a dataset of games found on Kaggle.
This project uses deep learning to predict the evaluation of a given chess position, in addition to React.js and Django for UI and Backend Requests.
Due to resource restrictions during training, model is still limited and does not perfectly replicate training-data to its fullest potential.

https://github.com/user-attachments/assets/e52de2f4-e224-46b9-b58a-f58f1c38e676



To Run App:<br />

  Open New Terminal for backend server: <br />
    - Run `cd backend`<br />
    - Create python venv using `python -m venv ./venv` and run venv with `venv/Scripts/activate` (windows)<br />
    - Run `python -m pip install -r requirements.txt`<br />
    - Run `python manage.py runserver`<br />
    
  Open New Terminal for frontend server: <br />
    - Run `cd frontend`<br />
    - Run `npm install`<br />
    - Run `npm start`<br />

Resources:<br />
https://www.geeksforgeeks.org/building-a-web-based-chess-game-with-react-and-chess-js/<br />
https://www.kaggle.com/datasets/ronakbadhe/chess-evaluations?select=random_evals.csv<br />
https://www.npmjs.com/package/chess.js/v/0.13.1<br />
https://towardsdatascience.com/train-your-own-chess-ai-66b9ca8d71e4<br />
https://peerdh.com/blogs/programming-insights/integrating-pytorch-with-django-for-machine-learning-applications
