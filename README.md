
# Ticket Planner
#### Video Demo:  <URL HERE>
#### Description:
# Ticket Planner App

The **Ticket Planner** is a web-based application built with Flask that allows users to manage their tasks by creating tickets. Each ticket includes a title, description, and due date. The app also supports user registration and login, along with ticket management features like editing, deleting, and archiving.

## Features

- **User Authentication**: Registration and login system with unique usernames.
- **Create Tickets**: Users can create tickets with a title, description, and due date.
- **Ticket Management**: 
  - View all pending tickets.
  - Edit, delete, or archive tickets.
  - Archived tickets can be restored.
- **History Page**: View all tickets created, including the ability to permanently delete them.
- **Archived Tickets**: Manage archived tickets with options to edit, delete, or restore.

## Database Structure

The app uses an SQLite3 database to store data, with the following key tables:

- **Users table**: Stores information about registered users.
- **Tickets table**: Contains all user-created tickets, linked to the user by a foreign key.

The SQL scripts for creating these tables are located in the `sql_scripts` folder.

## File Structure

├── app.py # Flask application ├── sql_scripts # Folder containing SQL scripts │ └── create_tables.sql # SQL file to create the necessary tables ├── templates # Folder containing HTML templates │ ├── identification.html # Template for Register and Login forms │ ├── main.html # Dashboard to manage tickets │ └── edit_ticket.html # Page for editing tickets ├── static │ └── styles.css # CSS file for styling the app └── README.md # This file


## How It Works

### User Authentication

Users can register or log in via the `/register` and `/login` routes:

- **GET Request**: Displays the `identification.html` form for registration or login.
- **POST Request**: Processes the form data. Users must have a unique username to register. Once logged in, users are redirected to the `/main` dashboard.

### Dashboard (Main Page)

- The `/main` route displays the **Your Tickets** section with all the user's pending tickets.
- Users can create new tickets using the **Create New Ticket** form by providing a title, description, and due date.
- After submission, the ticket is added to the **Your Tickets** section in real time, using JavaScript to update the dashboard without refreshing the page.

### Ticket Actions

- **Edit**: Users can modify ticket details through the `/edit_ticket` route, which renders `edit_ticket.html`. The changes are saved and reflected on the dashboard.
- **Delete**: Deletes a ticket from the dashboard (without removing it from the database), setting the `is_deleted` flag in the database.
- **Archive**: Marks a ticket as archived by updating the `is_archived` flag.

### History and Archived Tickets

- **History Page**: Accessible via the left panel, this page shows all the user’s created tickets. Users can permanently delete tickets by calling the `/permanently_delete` route, which removes the ticket from the database.
- **Archived Tickets**: Users can view archived tickets and perform the following actions:
  - **Edit**: Modify the ticket details.
  - **Restore**: Unarchive the ticket and move it back to the dashboard using the `/restore_ticket` route.
  - **Permanently Delete**: Remove the ticket from the database.

## How to Run

1. Clone this repository.
2. Install the required Python packages using:

   ```bash
   pip install -r requirements.txt
   flask init-db  
   flask run


Pip install sqlite3 and flask
Must install sqlite3 via sudo-apt get sqlite3?
flask init-db to initialize the database fefe