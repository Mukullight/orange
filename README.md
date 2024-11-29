# ![Orange](https://github.com/Mukullight/system-design-/blob/main/Screenshot%202024-11-27%20183903.png)
> An AI based messaging service


[![web framework](https://img.shields.io/badge/web_framework-django-green))](https://www.djangoproject.com/)[![ai model](https://img.shields.io/badge/Artifical_intelligence-Mistral-%23ff8d33)](https://mistral.ai/news/le-chat-mistral/) [![license](https://img.shields.io/github/license/nhn/tui.editor.svg)](https://github.com/Mukullight/orange?tab=MIT-1-ov-file) [![PRs welcome](https://img.shields.io/badge/PR-violet)](https://github.com/Mukullight/orange/pulls)


An AI based messaging service with MISTRAL AI integration

In this service the user will be able to engage in conversations share intresting facts, fact check, using mistral ai's powerful AI capabilities.

## Section 1:  User registration

- User registration page allows the users to create a new user registration where the form fields include 



<img src="https://github.com/Mukullight/system-design-/blob/main/Registration_form.png" />



| Registration form | Example response |
| --- | --- |
| **Name** | **john doe** |
|**Username** | **john_man** |
| **Email** | **johndoe12@gmail.com** |
| **Password** | __*******__ |
| **Password confirmation**| __*******__  |

The registration page has a section togoack to the login page 

## Login Page

<img src="https://github.com/Mukullight/system-design-/blob/main/login_form.png" />

the User can user there **email** and **password** to login into the account


## Home page

The home page primarily consists of 3 different sections they are Topics to the left and the main middle section consisting of Room names with the username, time of creation, topic and the number of participants as the attributes and the third main section consisting of recent activties consisting of the users and there messages


<img src="https://github.com/Mukullight/system-design-/blob/main/home_feed.png" />


## NavBar
The nav bar displays the logo of the chat platform along with settings and logout 


<img src="https://github.com/Mukullight/system-design-/blob/main/login_settings_js_button.png" />

The settings page has following attributes The user can add there profile picture, Nmae, Username, email, Bio 


<img src="https://github.com/Mukullight/system-design-/blob/main/settings_jpg.png" />


## Room Page


The room page has 3 main sections they are 
**1. AI Response** - The AI response section contains the text box allows the user to talk with the ai 


**2. Message Window**- The message window allows the user to send messages and the messages section diplays the host and the room description.

The message windows will also allows the user to edit the details of the Room or delete the room 

**3. Participants** - The participants shows the users that are present in the That particular chat room 


<img src="https://github.com/Mukullight/system-design-/blob/main/room.png" />

## Edit Room Page


<img src="https://github.com/Mukullight/system-design-/blob/main/room_creation.png"/>


## Topic page 

Topic page will allows the user to check the list of rooms in each sub topic 

<img src="https://github.com/Mukullight/system-design-/blob/main/Travel_topic.png"/>

<img src="https://github.com/Mukullight/system-design-/blob/main/art_topic.png"/>


## User profile
<img src="https://github.com/Mukullight/system-design-/blob/main/profile_page.png"/>




# Directory structure 


``` sh
C:.
├───-p
├───base
│   ├───api
│   │   └───__pycache__
│   ├───migrations
│   │   └───__pycache__
│   ├───templates
│   │   └───base
│   └───__pycache__
├───orange
│   └───__pycache__
├───screenshots
├───static
│   ├───images
│   │   └───icons
│   ├───js
│   └───styles
└───templates
    
```

# Data model 
### User Model
The `User` model extends Django's built-in `AbstractUser` model, which provides basic user functionalities like authentication and user management.

- **name**: A character field to store the user's name, with a maximum length of 200 characters. It can be null.
- **email**: An email field that must be unique for each user. It can be null.
- **bio**: A text field to store a biography or description of the user. It can be null.
- **avatar**: An image field to store the user's avatar. It defaults to "avatar.svg" if not provided. It can be null.
- **USERNAME_FIELD**: Specifies that the email field will be used for authentication instead of the default username.
- **REQUIRED_FIELDS**: Specifies that the username field is required when creating a user.

### Topic Model
The `Topic` model represents a category or subject that rooms can be associated with.

- **name**: A character field to store the name of the topic, with a maximum length of 200 characters.

### Room Model
The `Room` model represents a chat room or discussion forum.

- **host**: A foreign key to the `User` model, representing the user who created the room. If the host is deleted, the room's host will be set to null.
- **topic**: A foreign key to the `Topic` model, representing the topic associated with the room. If the topic is deleted, the room's topic will be set to null.
- **name**: A character field to store the name of the room, with a maximum length of 200 characters.
- **description**: A text field to store a description of the room. It can be null and blank.
- **participants**: A many-to-many field to the `User` model, representing the users who are participating in the room. It can be blank.
- **updated**: A datetime field that automatically updates to the current date and time whenever the room is updated.
- **created**: A datetime field that automatically sets to the current date and time when the room is created.
- **Meta**: Specifies that rooms should be ordered by the `updated` and `created` fields in descending order.

### Message Model
The `Message` model represents a message sent within a room.

- **user**: A foreign key to the `User` model, representing the user who sent the message. If the user is deleted, the message will also be deleted.
- **room**: A foreign key to the `Room` model, representing the room where the message was sent. If the room is deleted, the message will also be deleted.
- **body**: A text field to store the content of the message.
- **updated**: A datetime field that automatically updates to the current date and time whenever the message is updated.
- **created**: A datetime field that automatically sets to the current date and time when the message is created.
- **Meta**: Specifies that messages should be ordered by the `updated` and `created` fields in descending order.

### Relationships
- **User to Room**: A user can host multiple rooms and participate in multiple rooms.
- **Topic to Room**: A topic can be associated with multiple rooms.
- **User to Message**: A user can send multiple messages.
- **Room to Message**: A room can contain multiple messages.

This data model sets up a basic structure for a chat application where users can create and participate in rooms, and send messages within those rooms. The `Topic` model adds a layer of categorization to the rooms.




## Setup

Fork `main` branch into your personal repository. Clone it to local computer. Install the requirements file. Before starting development, you should check if there are any errors.

```sh
git clone https://github.com/Mukullight/orange.git

cd orange

conda create -n your_virtual_env python==3.9.20

conda activate your_virtual_env

pip install -r requirements.txt

python manage.py runserver

```



> The home page will be hosted on the http://127.0.0.1:8000/


Creating a superuser for the database admin

```sh
python manage.py createsuperuser
```
###  Migratig the data base 
```sh
python manage.py makemigrations
python manage.py migrate
```

## Admin page

The admin page allows the superuser to create all the avaialble data models and user details 

<img src="https://github.com/Mukullight/system-design-/blob/main/admin.png"/>

> The admin page will be hosted on the http://127.0.0.1:8000/admin




# Video Content

## Embedded Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>






## 📜 License

This software is licensed under the [MIT](https://github.com/Mukullight/orange?tab=MIT-1-ov-file) © [Mukul Namagiri](https://github.com/Mukullight).


