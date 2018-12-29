# RECIPE
It is a part of Udacity FSND the catalog project
> You will develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.
It is a web application for recipes and allow you to create your own recipes and share them with other in the app.

## Project Screen Shot(s)
Home page
![](https://github.com/iAbrar/catalog/blob/master/home.png)

Flash message
![](https://github.com/iAbrar/catalog/blob/master/flash%20message.png)

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
13. Run this application:
    ```bash
    python3 application.py
    ```
14. Open `http://localhost:5000/` in your browser.


## API Reference
- [Google API](https://console.developers.google.com/)

## Technology, Languages and Freamworks:
- HTML
- JS
- Ajax
- Bootstrap 4
- Flask
- Python


## Resources I used them:
1. Images & icons
    - [PNG MART](https://www.pngmart.com/)
    - [pic png](https://www.picpng.com/)
    - [PNG ALL](http://www.pngall.com/)
    - [Flat icon](https://www.picpng.com/)
    - [Pexels](https://www.pexels.com)
    - [Foodiesfeed](https://www.foodiesfeed.com/)
    - [Flat icon](https://www.picpng.com/)
2. [Google Fonts](https://fonts.google.com/)
3. [Boostrap Template](https://templatemo.com/tm-509-hydro)
4. [HTML Beautifier](http://beautifytools.com/)
5. Some recipes and images from [Hello Freash](https://www.hellofresh.com/)

## Future Checklist:
- [ ] create ico
- [ ] add more categories
- [ ] add more APIs such: facebook, outlook, twitter ..etc
- [ ] add filters
- [ ] add search box
- [ ] add page navgator
- [ ] optimize the website
- [ ] change upload image style
- [ ] upgrade bootstrap 3 to bootstrap 4
- [ ] fix login style
- [ ] allow user to upload image from his/her device
- [ ] add date to each recipe
- [ ] create pravite view for recipes
- [ ] add print recipe
- [ ] add more category such: snaks ..  etc
- [ ] add rating the recipe
- [x] completed
