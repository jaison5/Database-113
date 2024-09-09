from flask import Flask, render_template_string
import mysql.connector

app = Flask(__name__)

# MySQL configurations
db_config = {
    'user': 'root',
    'password': '31415926',
    'host': 'localhost',
    'database': 'sys',
}

# Route to display data from sys_config table
@app.route('/')
def show_sys_config():
    try:
        # Establish MySQL connection
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        # Execute the query
        cursor.execute("SELECT * FROM sys_config")
        data = cursor.fetchall()
        
        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Render the data in an HTML table
        template = """
        <html>
        <head>
            <title>sys_config Data</title>
        </head>
        <body>
            <h1>sys_config Data</h1>
            <table border="1">
                <tr>
                    <th>Variable</th>
                    <th>Value</th>
                    <th>Set Time</th>
                    <th>Set By</th>
                </tr>
                {% for row in data %}
                <tr>
                    <td>{{ row['variable'] }}</td>
                    <td>{{ row['value'] }}</td>
                    <td>{{ row['set_time'] }}</td>
                    <td>{{ row['set_by'] }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
        """
        return render_template_string(template, data=data)
    
    except mysql.connector.Error as err:
        return f"Error: {err}"

if __name__ == '__main__':
    app.run(debug=True)
