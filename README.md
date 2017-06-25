# scuttle
Experiments with raspberry pi bot

### Set up

    mkdir ~/scuttle
    virtualenv ~/.venv_scuttle
    . .venv_scuttle/bin/activate
    sudo mount -t cifs //scuttle/homes/repos/scuttle ~/scuttle -o username=david,noexec,rw
    pip install -r ~/scuttle/requirements.txt

Then, using pycharm it's possible to edit the code in the scuttle repo.
Commands need to be run in an ssh session on scuttle however.

    ssh 192.168.1.156
    cd ~/repos/scuttle
    sudo python startint_point.py
    
