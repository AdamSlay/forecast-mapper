# PNG Mapper
PNG Mapper is a simple application that creates *.png* map files from a given *.shp* file.
The app will convert **(lat,lon)** coordinates to **cartesian** coordinates that scale to fit within
the *.png* frame - default is 720px, 480px. The app includes a *.shp* file binary parser which will
separate and render the various shapes within the file. 

## Usage
The application is Dockerized for use on any platform. To run, pull the repo and execute the following 
commands in the project dir:
```bash
docker compose build
```
This may take a few minutes as Docker builds the image. Next, run:
```bash
docker compose up
```
This will run the image and create two directories in the current working directory. 

- **build** - this contains all the build files necessary to build the image
- **images** - this contains the *.png* map files