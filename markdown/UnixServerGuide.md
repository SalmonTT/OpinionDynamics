# Using UNIX server

## Credentials:
host: sepc623.se.cuhk.edu.hk
username: fy20fti
password: Gjhu^hn4

## Using python3 in terminal：
To use python3 codes directly in terminal type in the following commands:
```bash
conda activate
```

## Using Jupyter Notebook on Local Browser
First enter the following commands in UNIX Terminal:
```bash
conda activate
jupyter notebook
```
You will see the following:
```bash
[C 12:35:20.912 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///run/user/1005/jupyter/nbserver-273789-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/?token=863640e36a586f508e0802160ab8b855cce45a8705b4fd2d
```

Now that Jupyter Notebook is running on server, we would like to open it with browser on local computer. Open up terminal on your local computer and enter the following:

```bash
ssh -N -f -L localhost:8000:localhost:8888 fy20fti@sepc623.se.cuhk.edu.hk
```
**Note**: the first "localhost:8000" refers to the port you would like to run on you local computer, and the second "localhost:8888" refers to the host running on the remote server. 

Your password will then be prompted:

```bash
C:\Users\Simon>ssh -N -f -L localhost:8000:localhost:8888 fy20fti@sepc623.se.cuhk.edu.hk
fy20fti@sepc623.se.cuhk.edu.hk's password:
```

After entering the password, go to your browser and open "localhost:8000". When opening for the first time you will be prompted to enter a token. This is the token found in :
```bash
[C 12:35:20.912 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///run/user/1005/jupyter/nbserver-273789-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/?token=863640e36a586f508e0802160ab8b855cce45a8705b4fd2d
```
for the above example, the token is:
```bash
863640e36a586f508e0802160ab8b855cce45a8705b4fd2d
```
And you are now running jupyter notebook!

## Uploading files to server:
on local command prompt enter the following:
```bash
scp path/to/local/file.ext user@remote-host:path/to/remote/file.ext
```
e.g.
```bash
C:\Users\Simon\Desktop\ftec4003\4003Task1\insurance-train.csv fy20fti@sepc623.se.cuhk.edu.hk:DataMining\insurance-train.csv
```

## Downloading files from server:
```bash
scp your_username@remotehost.edu:foobar.txt /local/dir
```
e.g.
```bash
scp fy20fti@sepc623.se.cuhk.edu.hk:DataMining\insurance-test.csv C:\Users\Simon\Desktop
```