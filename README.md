# [Your Project ]

**CS178: Cloud and Database Systems — Project #1**
**Author:** [Chidera Agu]
**GitHub:** [chefagunwani76]

---

## Overview

<!-- Describe your project in 2-4 sentences. What does it do? Who is it for? What problem does it solve? -->
This project runs queries over the world database to display the countries in the database and allow users to see information about specific countries. The app has a dynamoDB table that stores user information and utilizes a CRUD interface for the editing and reading of this table. The user signs in and can then have access to a world RDS database. 

---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for [describe what you stored]
- **AWS DynamoDB** — non-relational database for [describe what you stored]
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
ProjectOne/
├── flaskapp.py          # Main Flask application — routes and app logic
├── dbCode.py            # Database helper functions (MySQL connection + queries)
├── creds_sample.py      # Sample Credential file (see Credential Setup)

├── templates/
│   ├── home.html        # Landing page
│   ├── login.html       #Page for user to login so they can have access to RDS database queries
│   ├── add_user.html        # Page to add user to Users database 
│   ├── delete_user.html     # Page to delete user from Users database
│   ├── display_users.html   # Page to display all users from Users database
│   ├── update.html          #Page to update user lastname and city
│   ├── query.html           #Page to prompt user which country in database they would like to query
│   ├── all_countres.html    #Page to display all country in database
│   ├── country_result.html  #Page Shows information about the country the user chose from dropdown menu
├── .gitignore           # Excludes creds.py and other sensitive files
└── README.md
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/chefagunwani76/cs178-flask-app.git
   cd cs178-flask-app
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)
   ```bash
   pip install awscli
   aws configure
      input on prompts
   ```
   create creds.py file with your username and password 
   reference creds_sample.py
   ```

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://52.91.47.166:8080
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
```

---

## Database Design

### SQL (MySQL on RDS)

<!-- Briefly describe your relational database schema. What tables do you have? What are the key relationships? -->

**Example:**

- `[country]` — stores information about countries including their continent, surface area, government form, life expectancy, etc; primary key is `[Code]`
- `[city]` — stores information about a city's district and population; foreign key `[ID]`links to `[country]`;foreign key `[CountryCode]`links to `[countrylanguage]`
- `[countrylanguage]` — stores information about a country's language including if it is official and the amount of people in the country that speaks it; foreign key `[countrycode]`links to `[city]`; foreign key `[Language]`links to `[country]`

The JOIN query used in this project: 
The JOIN query that was used was between city and countrylanguage to see how many people speak a language in a city.

### DynamoDB

<!-- Describe your DynamoDB table. What is the partition key? What attributes does each item have? How does it connect to the rest of the app? -->

- **Table name:** `[Users]`
- **Partition key:** `[Name]`
- **Used for:** [In order to utilize a CRUD interface for users I created a DynamoDB table. The table keeps track of users' names
  and favorite city. The table can be updated, users can be deleted, added, and displayed. This table is used for the login.html page so a user's queries on the world database
  can be seperate for them to access.]

---

## CRUD Operations

| Operation | Route      | Description    |
| --------- | ---------- | -------------- |
| Create    | `/add-user` | [Adds a new user to the Users database] |
| Read      | `/display-users` | [Displays all the users in the Users database] |
| Update    | `/update-user` | [Updates the users last name and city in the Users database] |
| Delete    | `/delete-user` | [Removes a user from the Users database] |

---

## Challenges and Insights

<!-- What was the hardest part? What did you learn? Any interesting design decisions? -->
The hardest part of this assignment was getting the project properly configured with my credentials. Since I decided to use my own
RDS instance so I could use the world database, I had a few more steps to complete the setup and my machine was having quite a few issues. 
The primary thing I learned was how to use dynamoDB and SQL in one functional site. I found that really interesting. Keeping the functions seperate in my head
was also pretty difficult, I kept trying to use SQL functions on the dynamoDB I created. I do not think I had an interesting design decision, I put the world db querying behind the login. So only the Users CRUD interace was avaialable if the user was not signed in.

---

## AI Assistance

<!-- List any AI tools you used (e.g., ChatGPT) and briefly describe what you used them for. Per course policy, AI use is allowed but must be cited in code comments and noted here. -->
I used ChatGPT for the bootstraps and formatting of the login.html, user_stats.html, all_countries.html, country_result.html files so they would all match. 