## Active Collab Timer

Way better than the official app.

## Get started

- Install eel: `pip3 install eel` or use the version in the requirements file
- Create a `config.json` with your username, password, url
- Run app.py: `python3 app.py`

### Vue development

- To build, navigate to `vue/` and run `npm run build`, will overwrite the `web/` directory

### TODOs

- Detect when logged out, and notify the user to restart sign in again
- Allow saving of defaults using localstorage/vuex-persist
- Link to projects/tasks from time listing
- Allow user to edit time records
- Don't load all tasks, takes way too long. Load tasks from projects in time listing

### Notes

- No client auth, use config file to do it python-side, or do this in a different secure way
- Currently only gets the last month of time records
