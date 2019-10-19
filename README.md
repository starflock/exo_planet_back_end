## EXO PLANET BACKEND https://github.com/starflock/exo-plan-it

https://exo-planet-starflock.herokuapp.com/

***Heroku Commands***
```
heroku login
heroku git:remote -a exo-planet-starflock-backend
git push heroku master
```

## More Info https://devcenter.heroku.com/articles/git


***Docker Commands***
```
sudo docker build -t exo_planet_backend .
sudo docker run -it -p 5001:5001 exo_planet_backend
```
