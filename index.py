#Import Flask and create flask object 
import flask
from flask import request, jsonify

#Import SharePlum and Office365 Class to connect to sharepoint
from shareplum import Site
from shareplum import Office365

#Python package for geocode location 
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Simple Application")

#Sharepoint site information
server_url = "https://ytpl.sharepoint.com"
site_url = "https://ytpl.sharepoint.com/sites/demosite/PowerApps/"

username = ""
passwd = "" 
leave_balance_list = 'lm_emp_leave_balance_record'
leave_records_list = 'lm_employee_leave_record'

#Get Authentication cookies
authcookie = Office365(server_url, username = username, password = passwd).GetCookies()
site = Site(site_url, authcookie=authcookie)

#Get all the data from sharepoint list which holds employess leave balance record 
sp_list = site.List(leave_balance_list)

#Get all the data from sharepoint list which holds employees leave records
leave_records = site.List(leave_records_list)


# Create an object of Flask Class  and configure it run in debug mode
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#------------------------------------------------------------------------------------------------------
#Route to get leave balance based on user id (email address - for example ashay.maheshwari@yash.com"
#-------------------------------------------------------------------------------------------------------
@app.route('/leaveapi/v1/balance', methods=['GET'])
def all_leave_balances():
        #Check if an id is passed as query string and read the data from sharepoint based on the value of id passed
        if 'id' in request.args:
                id = request.args['id']
		fields = ["emp_id", "sick_leave", "casual_leave", "accumulated_leave"]
		query = {'Where': [('Eq', 'emp_id', id)]}
		data = sp_list.GetListItems(fields = fields, query = query)
		return jsonify(data)
	
        else:
                return jsonify({"error": "404"})


#--------------------------------------------------------------------------------------------------------------
#Route to get Casual leave balance of a user 
#--------------------------------------------------------------------------------------------------------------
@app.route('/leaveapi/v1/balance/casualLeave', methods=['GET'])
def casual_leave_balance():
        #Check if an id is passed as query string and read the data from sharepoint based on the value of id passed
        if 'id' in request.args:
                id = request.args['id']
                fields = ["emp_id", "casual_leave"]
                query = {'Where': [('Eq', 'emp_id', id)]}
                data = sp_list.GetListItems(fields = fields, query = query)
                return jsonify(data)

        else:
                return jsonify({"error": "404"})


#--------------------------------------------------------------------------------------------------------------
#Route to get sick leave balance of a user
#--------------------------------------------------------------------------------------------------------------
@app.route('/leaveapi/v1/balance/sickLeave', methods=['GET'])
def sick_leave_balance():
        #Check if an id is passed as query string and read the data from sharepoint based on the value of id passed
        if 'id' in request.args:
                id = request.args['id']
                fields = ["emp_id", "sick_leave"]
                query = {'Where': [('Eq', 'emp_id', id)]}
                data = sp_list.GetListItems(fields = fields, query = query)
                return jsonify(data)

        else:
                return jsonify({"error": "404"})



#--------------------------------------------------------------------------------------------------------------
#Route to get Bereavement Leave balance of a user
#--------------------------------------------------------------------------------------------------------------
@app.route('/leaveapi/v1/balance/bereavementLeave', methods=['GET'])
def bereavement_leave_balance():
        #Check if an id is passed as query string and read the data from sharepoint based on the value of id passed
        if 'id' in request.args:
                id = request.args['id']
                fields = ["emp_id", "accumulated_leave"]
                query = {'Where': [('Eq', 'emp_id', id)]}
                data = sp_list.GetListItems(fields = fields, query = query)
                return jsonify(data)

        else:
                return jsonify({"error": "404"})



#--------------------------------------------------------------------------------------------------------------
#Route to get all leave records of an employee
#--------------------------------------------------------------------------------------------------------------
@app.route('/leaveapi/v1/leaves', methods = ['GET'])
def get_all_leave_records():
	if 'id' in request.args:
		id = request.args['id']
		fields = ["Title", "emp_name", "date_of_request", "leave_start_date", "leave_end_date", "manager", "leave_request_id", "leave_title", "leave_status", "leave_details", "no_of_leaves", "day_of_leave", "start_date_of_week", "end_date_of_week", "TimesheetWeek", "manager_email"]
		query = {'Where': [('Eq', 'Title', id)]}
		leave_data = leave_records.GetListItems(fields = fields, query = query)
		return jsonify(leave_data)




#--------------------------------------------------------------------------------------------------------------
#Route to get all approved leave records of an employee
#--------------------------------------------------------------------------------------------------------------
@app.route('/leaveapi/v1/leaves/approved', methods = ['GET'])
def get_approved_leave_records():
        if 'id' in request.args:
                id = request.args['id']
                fields = ["Title", "emp_name", "date_of_request", "leave_start_date", "leave_end_date", "manager", "leave_request_id", "leave_title", "leave_status", "leave_details", "no_of_leaves", "day_of_leave", "start_date_of_week", "end_date_of_week", "TimesheetWeek", "manager_email"]
                query = {'Where': ['And', ('Eq', 'Title', id), ('Eq', 'leave_status','Approved')]}
                leave_data = leave_records.GetListItems(fields = fields, query = query)
                return jsonify(leave_data)



#--------------------------------------------------------------------------------------------------------------
#Route to get all pending leave records of an employee
#--------------------------------------------------------------------------------------------------------------
@app.route('/leaveapi/v1/leaves/pending', methods = ['GET'])
def get_pending_leave_records():
        if 'id' in request.args:
                id = request.args['id']
                fields = ["Title", "emp_name", "date_of_request", "leave_start_date", "leave_end_date", "manager", "leave_request_id", "leave_title", "leave_status", "leave_details", "no_of_leaves", "day_of_leave", "start_date_of_week", "end_date_of_week", "TimesheetWeek", "manager_email"]
                query = {'Where': ['And', ('Eq', 'Title', id), ('Eq', 'leave_status','Pending')]}
                leave_data = leave_records.GetListItems(fields = fields, query = query)
                return jsonify(leave_data)





#--------------------------------------------------------------------------------------------------------------
#Route to get city name based on latitude and longitude  
#--------------------------------------------------------------------------------------------------------------
@app.route('/leaveapi/v1/location', methods = ['GET'])
def get_location():
	if 'lat' in request.args and 'lon' in request.args:
		latitute = request.args['lat']
		longitude = request.args['lon']
		lat_lon = latitute + "," + longitude
		location = geolocator.reverse(lat_lon)
		records = location.raw
		address = records['address']
		return jsonify(address)				

#Run the app on All IP and 8082 port
app.run(host='0.0.0.0' , port=8082)

