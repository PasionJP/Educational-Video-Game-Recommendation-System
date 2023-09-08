# Educational-Video-Game-Recommendation-System
[<img src="https://i.ytimg.com/vi/4fC8pzA6mmA/maxresdefault.jpg" width="50%">](https://www.youtube.com/watch?v=4fC8pzA6mmA "Educational-Video-Game-Recommendation-System")


## Install Python Requirements
   Install the required Python packages by running the following command in your project directory:

   ```bash
   $ pip install -r requirements.txt
   ```


## Setting-up the database

1. **Install XAMPP:**
   If you haven't already, download and install XAMPP from the official website (https://www.apachefriends.org/index.html). XAMPP provides a local server environment that includes Apache, MySQL, and PHP, which is necessary for running the database for your app.

2. **Import Database:**
   - Start XAMPP and ensure that the Apache and MySQL modules are running.
   - Open your web browser and go to http://localhost/phpmyadmin.
   - Log in to phpMyAdmin if prompted.
   - Click on the "Import" tab.
   - Click the "Choose File" button and navigate to the `games.sql` file located in the `db` folder of your project.
   - Click "Go" to import the database schema and data. Ensure that you create the necessary database and tables as specified in your `games.sql` file.
   
4. **Run `updateGames.py` to Populate the Database:**
   Before starting the server, run the `updateGames.py` script located in the `GameLibrary-All` folder. This script adds games to the database for the games library. Open your terminal and navigate to the `GameLibrary-All` folder, then execute the following command:

   ```bash
   $ python updateGames.py
   ```

   This will populate the database with the necessary game data.


## Set Environment Variables

Now that you have XAMPP installed, the database imported, and the game data populated, proceed with setting up the environment variables and starting the Flask server as per your initial instructions:

```bash
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
```

## Start Server

You can start the Flask server with the following command:

```bash
$ flask run
```

Or alternatively:

```bash
$ python -m flask run
```



## USER INTERFACE
**User - Home Page (PC)**
![1 1-Educgames](https://github.com/PasionJP/Educational-Video-Game-Recommendation-System/assets/46522023/2a1fa496-d2a0-45cb-ae62-916ddee84d4f)


**User - Homepage (Mobile)**

<img width="156" alt="1 2-Educgames" src="https://github.com/PasionJP/Educational-Video-Game-Recommendation-System/assets/46522023/4ef635e7-1ed2-4cde-9172-1bb859d11300">
<img width="154" alt="1 3-Educgames" src="https://github.com/PasionJP/Educational-Video-Game-Recommendation-System/assets/46522023/b5896dee-73bd-4f74-aa34-0be2bf8d8acc">


**User - Sign up Page**
![2-Educgames](https://github.com/PasionJP/Educational-Video-Game-Recommendation-System/assets/46522023/4d8ec244-da8d-4209-90ba-c5510c4f820f)


**User - Sign in Page**
![3-Educgames](https://github.com/PasionJP/Educational-Video-Game-Recommendation-System/assets/46522023/922af7c9-7e80-442b-9e39-385e40aa84f0)


**All games Page**
<img width="960" alt="4-Educgames" src="https://github.com/PasionJP/Educational-Video-Game-Recommendation-System/assets/46522023/4e10a351-72ce-4e06-95e1-33f6bd11b7b3">


**User - Profile Page**
![5-Educgames](https://github.com/PasionJP/Educational-Video-Game-Recommendation-System/assets/46522023/c91f188e-0da9-4e90-a5be-ab2b94c5f3af)


**Recommendation Page (Educational Video Game Recommendation System)**
![6-Educgames](https://github.com/PasionJP/Educational-Video-Game-Recommendation-System/assets/46522023/4d877728-42fa-4a37-aa24-5f07d70f2c3c)


**Admin - Sign in Page**
![7-Educgames](https://github.com/PasionJP/Educational-Video-Game-Recommendation-System/assets/46522023/5aafd147-60ba-4f4b-a9eb-92c673f0a490)


**Admin - Home Page**
![8-Educgames](https://github.com/PasionJP/Educational-Video-Game-Recommendation-System/assets/46522023/ccad31b8-185f-47a7-99ea-f11e10f30be3)


**Admin - Add Game Page**
![9-Educgames](https://github.com/PasionJP/Educational-Video-Game-Recommendation-System/assets/46522023/5f56dbcb-1200-4c83-a044-1001830e789f)


**Admin  - Manage/View Games Page**
<img width="960" alt="10-Educgames" src="https://github.com/PasionJP/Educational-Video-Game-Recommendation-System/assets/46522023/3299f817-652f-443a-9a8f-0ff7d006e329">


**Admin - Manage Users Page**
![11-Educgames](https://github.com/PasionJP/Educational-Video-Game-Recommendation-System/assets/46522023/f9bfb0ed-1223-4037-aea5-f85a94856b0d)
