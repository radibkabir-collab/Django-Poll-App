# 🌐 Live Website

🔗 **https://radibdsi.pythonanywhere.com/**  
Access the deployed version of the Django Poll App here.

---

# Django Poll App

A simple polling application built with Django. Users can create or update polls, vote on them, and view results in real-time.

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, Tailwind CSS
- **Database:** PostgreSQL

## Features

### Poll Index

View all available polls in a card-based layout. Click "Vote Now" to participate or use the "+" card to create a new poll.

![Poll Index](Screenshots/poll-index.png)

### Create Poll

Create a new poll by entering a question and up to four choices.

![Create Poll](Screenshots/poll-create.png)

### Poll Details and Voting

Vote on a poll and view the poll summary with live vote counts.

![Poll Details](Screenshots/poll-details.png)

### Update Poll

Edit an existing poll's question and choices. After updating the vote count will reset.

![Update Poll](Screenshots/poll-update.png)

### Delete Poll

Remove a poll with a confirmation dialog.

![Delete Poll](Screenshots/poll-delete.png)

---

## 📱 Mobile Responsive Design

The app is fully responsive and works seamlessly on mobile devices.

<table>
  <tr>
    <td align="center">
      <img src="Screenshots/mob-poll-index.png" alt="Mobile Poll Index" width="250"><br>
      <b>Poll Index</b>
    </td>
    <td align="center">
      <img src="Screenshots/mob-poll-create.png" alt="Mobile Create Poll" width="250"><br>
      <b>Create Poll</b>
    </td>
    <td align="center">
      <img src="Screenshots/mob-poll-details.png" alt="Mobile Poll Details" width="250"><br>
      <b>Poll Details</b>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="Screenshots/mob-poll-update.png" alt="Mobile Update Poll" width="250"><br>
      <b>Update Poll</b>
    </td>
    <td align="center">
      <img src="Screenshots/mob-poll-delete.png" alt="Mobile Delete Poll" width="250"><br>
      <b>Delete Poll</b>
    </td>
    <td></td>
  </tr>
</table>

---

## Getting Started

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Navigate to the Django project:
   ```bash
   cd djangotutorial
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```
5. Open `http://127.0.0.1:8000/` in your browser
