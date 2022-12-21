# PNG Mapper
PNG Mapper is a simple application that creates *.png* map files from a given *.shp* file.
The app will convert **(lat,lon)** coordinates to **cartesian** coordinates that scale to fit within
the *.png* frame - default is 720px, 480px. The app includes a *.shp* file binary parser which will
separate and render the various shapes within the file. 

## Usage
The application is Dockerized for use on any platform. To run, pull the repo and execute the following 
command in the project dir:
```bash
docker compose up
```
This will build then run the image and output the result of the application into the users current directory 