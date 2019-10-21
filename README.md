# NASA Space Apps Challenge Hackathon
## EXO PLANET BACKEND 

**Front End**
https://github.com/starflock/exo-plan-it

**Project Link**
https://2019.spaceappschallenge.org/challenges/planets-near-and-far/build-planet-workshop/teams/starflock/project

https://exo-planet-starflock.herokuapp.com/

***Heroku Commands***
```
heroku login
heroku git:remote -a exo-planet-starflock-backend
git push heroku master
heroku config -s >> .env
gunicorn app:app test_mode
```

## More Info https://devcenter.heroku.com/articles/git


***Docker Commands***
```
sudo docker build -t exo_planet_backend .
sudo docker run -it -p 5001:5001 exo_planet_backend
```
