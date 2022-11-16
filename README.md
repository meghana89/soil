# mlop_flask
Create a flask application for ML Ops following source code from 
#   https://www.datacamp.com/tutorial/tutorial-machine-learning-pipelines-mlops-deployment#application-programming-interface-api-
#   https://github.com/pycaret/deployment-heroku
#   Dependencies
#   PyCaret
    to instal pycaret 
    Install
    PyCaret is tested and supported on the following 64-bit systems:
        Python 3.6 – 3.8
        Python 3.9 for Ubuntu only
        Ubuntu 16.04 or later
    #   Windows 7 or later
    Install PyCaret with Python's pip package manager.
        pip install pycaret
    To install the full version (see dependencies below):
        pip install pycaret[full]
    If you want to try our nightly build (unstable) you can install pycaret-nightly from pip.
        pip install pycaret-nightly
    Environment
    In order to avoid potential conflicts with other packages, it is strongly recommended to use a virtual environment, e.g. python3 virtualenv (see python3 virtualenv documentation) or conda environments. Using an isolated environment makes it possible to install a specific version of pycaret and its dependencies independently of any previously installed Python packages. 
    # create a conda environment
    conda create --name yourenvname python=3.8

    # activate conda environment
    conda activate yourenvname

    # install pycaret
    pip install pycaret

    # create notebook kernel
    python -m ipykernel install --user --name yourenvname --display-name "display-name"
    PyCaret is not yet compatible with sklearn>=0.23.2.

    #   For MAC OS

    MAC users will have to install LightGBM separately using Homebrew, or it can be built using CMake and Apple Clang (or gcc). See the instructions below:

    Install CMake (3.16 or higher):

        >> brew install cmake
        Install OpenMP
        >> brew install libomp
        Run the following commands in terminal:

        git clone --recursive https://github.com/microsoft/LightGBM ; cd LightGBM
        mkdir build ; cd build
        cmake ..
        make -j4
    
#   Flask
    Prerequisite
    Python 2.6 or higher is usually required for installation of Flask. Although Flask and its dependencies work well with Python 3 (Python 3.3 onwards), many Flask extensions do not support it properly. Hence, it is recommended that Flask should be installed on Python 2.7.

    Install virtualenv for development environment
    virtualenv is a virtual Python environment builder. It helps a user to create multiple Python environments side-by-side. Thereby, it can avoid compatibility issues between the different versions of the libraries.

    The following command installs virtualenv

        $ #importing plotly and cufflinks in offline mode
import cufflinks as cf
import plotly.offline
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

    This command needs administrator privileges. Add sudo before pip on Linux/Mac OS. If you are on Windows, log in as Administrator. On Ubuntu virtualenv may be installed using its package manager.

    Sudo apt-get install virtualenv
    Once installed, new virtual environment is created in a folder.

        $ mkdir myproject
        $ cd myproject
        $ python3 -m venv venv

    #   To activate corresponding environment, on Linux/OS X, use the following −

        $ . venv/bin/activate
    #   On Windows, following can be used

    >venv\scripts\activate
    We are now ready to install Flask in this environment.

        $ pip install Flask
    The above command can be run directly, without virtual environment for system-wide installation.
#   Docker /https://www.freecodecamp.org/news/how-to-dockerize-a-flask-app/
    install the docker extension in vs studio code and install the docker desktop application on the local machine.
    connect to your docker hub account and create a repository.
    then;
    
    The below code should be the first line of every Dockerfile – it tells the Docker builder what syntax to use while parsing the Dockerfile and the location of the Docker syntax file. (Source)

            # syntax=docker/dockerfile:1
        While it is possible to create our own base images, there is no need to go that far because Docker allows us to inherit existing images. The following line tells Docker which base image to use — in this case, a Python image.

            FROM python:3.8-slim-buster
        To keep things organized, we also tell Docker which folder to use for the rest of the operations, so we use a relative path as shown below.

        In this case, we're telling Docker to use the same directory and name for the rest of its operations — it's a directory contained within our container image.

            WORKDIR /app
        In the fourth and fifth lines, we tell Docker to copy the contents of our requirements.txt file into the container image's requirements.txt file. Then run pip install to install all the dependencies in the same file to be used by the image.

            COPY requirements.txt requirements.txt
        RUN pip3 install -r requirements.txt
        Continuing with the copying, we now copy the remainder of the files in our local working directory to the directory in the docker image.

            COPY . .
        the next line of code tells docker to expose the specific port to external applications
        # expose port
            
            EXPOSE 5000

        Our image so far has all of the files that are similar to those in our local working directory. Our next task is to assist Docker in understanding how to run this image inside a container.

        This line specifically instructs Docker to run our Flask app as a module, as indicated by the "-m" tag. Then it instructs Docker to make the container available externally, such as from our browser, rather than just from within the container. We pass the host port:

            CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
            docker build -t follysage/pycaret:latest . # to build the the docker image
        docker run -d -p 5000:5000 follysage/pycaret  # to run the container
   
    ****NOTE*****
    the requirements.txt file is very essentisal to succesfully build a container.
    please do pip freeze to see what version of the following you are currently running and update accorginly
            pycaret==3.0.0rc4
            colorama==0.4.5
            click==8.1.3
            Flask==2.2.2
            Jinja2==3.1.2
            gunicorn==20.1.0
            certifi==2021.10.8
            itsdangerous==2.1.2
            scikit-learn==1.1.2
            MarkupSafe==2.1.1
            Werkzeug==2.2.2