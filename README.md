# RECIPE
It is a part of Udacity FSND
> You will develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.


## Project Screen Shot(s)


## Installation and Setup Instructions
1. Download and install [Vagrant](https://www.vagrantup.com/downloads.html).

2. Download and install [VirtualBox](https://www.virtualbox.org/wiki/Downloads).

3. Clone or download the Vagrant VM configuration file from [here](https://github.com/udacity/fullstack-nanodegree-vm).

4. Open the above directory and navigate to the `vagrant/` sub-directory.

5. Open terminal, and type

   ```bash
   vagrant up
   ```

   This will cause Vagrant to download the Ubuntu operating system and install it. This may take quite a while depending on how fast your Internet connection is.

6. After the above command succeeds, connect to the newly created VM by typing the following command:

   ```bash
   vagrant ssh
   ```

8. Type `cd /vagrant/` to navigate to the shared repository.

9. Download or clone this repository, and navigate to it.

11. Install or upgrade Flask:
    ```bash
    sudo python3 -m pip install --upgrade flask
    ```
12. Run the following command to set add some data:
    ```bash
    python seeder.py
    ```
13. Run this application:
    ```bash
    python3 application.py
    ```
14. Open `http://localhost:5000/` in your browser.


## API Reference


## Technology:
- HTML
- JS
- Ajax
- Bootstrap 4


## Resources I used them:

## Future Checklist:
- [ ] create ico
- [ ] add more categories
- [ ] add filters
- [ ] add search box
- [ ] add page navgator
- [ ] optimize the website
- [x] completed
