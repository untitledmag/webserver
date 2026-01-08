# Minimalistic Webserver Implimentation Using Flask
## Dependencies Used
- flask[async]
- colorama
- requests
- aiosqlite
- httpx

## Features
- Frontend with landing page.
- 3 different webpages including fetching cat images
- API server using flask
  - `handshake` endpoint for checking api connection (auth protected)
  - `developer` endpoint to get information about developer
  - `get-cat` endpoint to get a random cat picture (auth protected)
  - `register` endpoint to get a auth token and register in database
  - `ip/lookup` endpoint to get information about any ip address (auth protected)
- 404 Error handling in frontend

## Configurations
- ### Host

  Head over to `config.py`. There you can see/change app's host ip and port

  
- ### Webpages

  To change webpages, create your own html pages and add them in `templates` folder and add these things in `app.py`
  ```py
  @app.route('/<your_webpage_name>')             # name that you want to give your webpage. It will be used like this: `http://localhost:8080/<your_webpage_name>`
  def render_<name>():                           # you can chose any name as long as it is not already in use
    return render_template('<filename>')         # NOTE: make sure to add file's extension or it will not work

- ### API Endpoints

  To add API endpoints, you'll need to add these things in `app.py`
  - **Asynchronus**
    ```py
    @app.route('/api/v1/<endpoint>')                        # replace `<endpoint>` with name of your choice. Make sure the name you are using is not already in use.
    @auth_protected                                         # auth_protected if you wan't only authorized people can access it. NOTE: `auth_protected` decorator can only work with asynchronus functions not synchronus
    async def something():                                  # again it can be anything as long as i is not already used
      return jsonify({'code':200,'body':'Success'})         # Your endpoint should return something. Must be json
  - **Synchronus**
    ```py
    @app.route('/api/v1/<endpoint>')
    def something():                                        #Used `def` instead of `async def`
      return jsonify({'code':200,'body':'Success'})
