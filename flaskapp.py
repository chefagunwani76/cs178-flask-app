# author: Chidera Agu
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session
import boto3
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Users')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        last_name = request.form['last_name']
        city = request.form['city']
        
        if name and city:
            table.put_item(
                Item={
                    "Name": name,
                    "Last Name": last_name,
                    "City": city
                }
            )

            flash('User added successfully! Huzzah!', 'success')
        else:
            flash('Please fill in all fields.', 'warning')
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    # Render the form page if the request method is GET
    return render_template('add_user.html')

@app.route('/delete-user',methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        if name:
            table.delete_item(
                Key={
                    "Name": name
                }
            )
            flash('User deleted successfully! Hoorah!', 'success')
        else:
            flash('Please enter a name.', 'warning')
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    # Render the form page if the request method is GET
    return render_template('delete_user.html')

@app.route('/update-user', methods=['GET', 'POST'])
def update_user():

    if request.method == 'POST':
        name = request.form.get('name')         
        last_name = request.form.get('last_name')
        city = request.form.get('city')

        if name:
            try:
                table.update_item(
                    Key={
                        "Name": name
                    },
                    UpdateExpression="SET LastName = :ln, City = :c", 
                    ExpressionAttributeValues={
                        ":ln": last_name,
                        ":c": city
                    }
                )

                flash("User updated successfully!", "success")

            except Exception as e:
                print("Update error:", e)
                flash("Error updating user.", "danger")
        else:
            flash("Name is required.", "warning")

        return redirect(url_for('home'))

    return render_template('update_user.html')

@app.route('/display-users')
def display_users():
    response = table.scan()
    users_list = response['Items']
    return render_template('display_users.html', users=users_list)

@app.route('/log-in-user', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            name = request.form['name']

            response = table.get_item(Key={"Name": name})
            user = response.get('Item')

            if user:
                session['username'] = name
                flash("Login successful!", "success")
                return redirect(url_for('user_stats'))
            else:
                flash("User not found!", "warning")
                return redirect(url_for('login'))

        except Exception as e:
            print("Login error:", e)
            flash("Something went wrong. Try again.", "warning")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/display-user-stats')
def user_stats():
    key = {"Name": session['username']}  # retrieve from session
    response = table.get_item(Key=key)
    user = response.get('Item')
    if not user:
        flash("User not found", "warning")
        return redirect(url_for('login'))

    return render_template('user_stats.html', user=user)

@app.route('/country-query', methods=['GET','POST'])
def country_query():
    if 'username' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('login'))
    try:
        if request.method == 'GET':
            countries = execute_query("SELECT Name FROM country")
            return render_template('query.html', countries=countries)
        country = request.form.get('country')
        if not country:
            flash("Please select a country.", "warning")
            return redirect(url_for('country_query'))
        query = """
            SELECT Name, Capital, Region
            FROM country
            WHERE Name = %s
        """
        data = execute_query(query, (country,))

        if not data:
            flash("No results found for that country.", "warning")
            return redirect(url_for('country_query'))

        return render_template('country_result', data=data, country=country)

    except Exception as e:
        print("Country query error:", e)
        flash("Database error. Please try again.", "warning")
        return redirect(url_for('country_query'))
    
@app.route('/all-countries')
def all_countries():
    if 'username' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('login'))
    try:
        query = """
            SELECT Name, Capital, Region
            FROM country
            ORDER BY Name
        """
        countries = execute_query(query)
        return render_template('all_countries.html', countries=countries)

    except Exception as e:
        print("All countries error:", e)
        flash("Could not load countries.", "warning")
        return redirect(url_for('country_query'))
    
@app.route('/country-result/<country>')
def country_result(country):

    if 'username' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('login'))

    try:
        query = """
            SELECT Name, Population, Continent, Region, Capital, GovernmentForm
            FROM country
            WHERE Name = %s
        """

        data = execute_query(query, (country,))

        if not data:
            flash("Country not found.", "warning")
            return redirect(url_for('country_query'))

        return render_template('country_result.html',
                               country=country,
                               data=data[0])

    except Exception as e:
        print("Country result error:", e)
        flash("Database error.", "danger")
        return redirect(url_for('country_query'))
    
@app.route('/country-language', methods=['POST'])
def country_language():
    country = request.form.get('country')
    query = """
        SELECT l.Language
        FROM country c
        JOIN countrylanguage l ON c.Code = l.CountryCode
        WHERE c.Name = %s
    """
    data = execute_query(query, (country,))
    return render_template('language_result.html', data=data, country=country)

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
