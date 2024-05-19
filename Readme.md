# EDM 4 Life

![EDM 4 Life](static/images/photos/1.png)

The best EDM music forum (for us)

## Purpose

EDM 4 Life is designed to create a vibrant community for EDM music enthusiasts. Users can register, log in, create posts, comment, and like posts. The points system encourages user engagement by rewarding daily logins, likes, comments, and posts. This application aims to foster a lively and interactive environment for EDM fans to share and discuss their favorite music.

## Prerequisites

Ensure you have the following installed on your machine:
- Python 3.x
- pip (Python package installer)
- virtualenv (optional but recommended)

## Setup

### macOS/Linux

#### 1. Configure Virtual Environment

Open a terminal and navigate to your project directory. Then run the following commands to set up a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2. Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

#### 3. Set Environment Variables

Set the `FLASK_APP` environment variable to point to your application entry point. This will tell Flask how to find your application.

```bash
export FLASK_APP=app.py
```

#### 4. Run the Application

Start the Flask development server:
```bash
flask run
```

### Windows

#### 1. Configure Virtual Environment
```bash
python3 -m venv venv
venv/bin/activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Set Environment Variables

```bash
set FLASK_APP=app.py
```

#### 4.Run the Application
```bash
flask run
```
By default, the application will run on [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

### Stopping the Application

To stop the Flask development server, you can use `Ctrl + C` in the terminal where the server is running.

### Killing the Process

If you need to kill the process manually (e.g., if the server is still running in the background), you can find the process ID (PID) and kill it:

On macOS/Linux:

Find the process ID using:

`lsof -i :5000`

Kill the process:

`kill -9 <PID>`


## Usage

### User Registration

1. Open your browser and navigate to the registration page.
2. Fill in the username, email, and password fields, then click "Register".
3. Upon successful registration, you will be redirected to the login page.

### User Login

1. On the login page, enter your username and password, then click "Login".
2. After a successful login, you will be redirected to the dashboard page, displaying a welcome message and your points.

### Points System

Our points system rewards user engagement with various activities on the platform:

- **Daily Login**: Earn 1 point each day you log in.
- **Likes**: Each like on another user's post earns you 1 point. Note that while you can like as many posts as you wish, only the first 5 likes per day will earn points.
- **Comments**: Earn points by commenting on posts. Comments with more than 50 characters earn 2 points, while comments with fewer than 50 characters earn 1 point. You can comment as often as you like, but only the first 10 comments each day will earn points.
- **Posting**: Creating a new post earns you 3 points. There is no limit to how many posts you can create, but only the first 5 posts each day will earn points.

This system is designed to encourage daily participation and contribute positively to our community. Thank you for being an active member!

### Creating and Managing Posts

#### Create a Post

1. On the dashboard page, click the "Create Request" button.
2. Fill in the post title and description, then click "Submit".
3. The new post will appear in the post list on the dashboard page.

#### Commenting and Liking Posts

1. Find a post you are interested in on the dashboard page.
2. Click the "Comment" button below the post, fill in your comment, and submit.
3. Click the "Like" button to like the post.

### Editing and Deleting Comments

#### Edit a Comment

1. Locate the comment you want to edit in the comment list.
2. Click the "Edit" button next to the comment, modify the content, and submit.

#### Delete a Comment

1. Locate the comment you want to delete in the comment list.
2. Click the "Delete" button next to the comment, and confirm the deletion.

## Testing

### 1. Unit Tests

Our unit tests test the email and password validation and request creation. To run unit tests, use the following command:
```bash
python -m unittest tests.test_basic
```

### 2. System Tests

Our system tests test login functionality and compatibility with Chrome browser. To run system tests, use the following command:

`python -m unittest tests.test_system`

## Contributing
<div align="center">

| Name  | Github Username(s) | Student ID |
| ---------- | -----------| -----------|
| Shijun Shao   | Halffancyy | 23926903 |
| Weisi Zhang   |Wiz6666   | 23210735 |
| Chen Shen | jerryshenfewcher, wsscnha | 23877677 |
| Jiaheng Gu | HendrickGu | 23925667 |

</div>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
