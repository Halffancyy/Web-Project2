EDM 4 Life

The best EDM music form (for us)

Prerequisites
Ensure you have the following installed on your machine:
Python 3.x
pip (Python package installer)
virtualenv (optional but recommended)

Setup
1. Configure Virtual Environment
Open a terminal and navigate to your project directory. Then run the following commands to set up a virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
2. Install Dependencies
With the virtual environment activated, install the required packages:
pip install -r requirements.txt
3. Set Environment Variables
Set the FLASK_APP environment variable to point to your application entry point. This will tell Flask how to find your application.
On macOS/Linux:
export FLASK_APP=app.py
On Windows:
set FLASK_APP=app.py
4. Run the Application
Start the Flask development server:
flask run
By default, the application will run on http://127.0.0.1:5000/.

Stopping the Application
To stop the Flask development server, you can use Ctrl + C in the terminal where the server is running.

Killing the Process
If you need to kill the process manually (e.g., if the server is still running in the background), you can find the process ID (PID) and kill it:

On macOS/Linux:
Find the process ID using:
lsof -i :5000
Kill the process:
kill -9 <PID>

Usage
User Registration
Open your browser and navigate to the registration page.
Fill in the username, email, and password fields, then click "Register".
Upon successful registration, you will be redirected to the login page.
User Login
On the login page, enter your username and password, then click "Login".
After a successful login, you will be redirected to the dashboard page, displaying a welcome message and your points.
User Points System
The user points system rewards engagement through the following activities:
Daily Login: Earn 1 point each day you log in.
Likes: Earn 1 point for each like on another user's post (only the first 5 likes per day will earn points).
Comments: Earn points by commenting on posts. Comments with more than 50 characters earn 2 points, while comments with fewer than 50 characters earn 1 point (only the first 10 comments each day will earn points).
Posting: Earn 3 points for creating a new post (only the first 5 posts each day will earn points).
Creating and Managing Posts
Create a Post
On the dashboard page, click the "Create Request" button.
Fill in the post title and description, then click "Submit".
The new post will appear in the post list on the dashboard page.
Commenting and Liking Posts
Find a post you are interested in on the dashboard page.
Click the "Comment" button below the post, fill in your comment, and submit.
Click the "Like" button to like the post.
Editing and Deleting Comments
Edit a Comment
Locate the comment you want to edit in the comment list.
Click the "Edit" button next to the comment, modify the content, and submit.
Delete a Comment
Locate the comment you want to delete in the comment list.
Click the "Delete" button next to the comment, and confirm the deletion.

Contributing

| Name           | GitHub Username(s)           | Student ID     |
| -------------- | ---------------------------- | -------------- |
| Shijun Shao    | Halffancyy                   | [Your Student ID] |
| Weisi Zhang    | Wiz6666                      | [Your Student ID] |
| Chen Shen      | erryshenfewcher, wsscnha     | 23877677 |
| Jiaheng Gu     | HendrickGu                   | [Your Student ID] |



License
MIT License
