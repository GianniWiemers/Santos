# Santos

Main project is in `whats-on-my-mind`

# Info & Dependencies
Project is based on:
https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project
More information on how this project is structured can be found on that webpage.

Python server is in `api` subfolder. By default this server runs on port 5000.
The python server handles api calls and game logic.
Start using the command `yarn start-api`
Python dependencies are in `requirements.txt`. Make sure to install these dependencies into your python environment before running.

React app is in `src` subfolder. By default this app runs on port 3000.
The react app handles serving client-facing javascript and html.
Start using the command `yarn start`

`yarn` is a javascript package manager, it can be installed via npm, or if that causes problems it can also be installed separately:
https://linuxize.com/post/how-to-install-yarn-on-ubuntu-20-04/

# How to run
In 2 separate terminals run:
`yarn start`
`yarn start-api`

When you make changes, simply refresh the webpage at `localhost:3000`, the changes will automatically appear there.