#Import Flask and create flask object
import flask
from flask import request, jsonify

#Import SharePlum and Office365 Class to connect to sharepoint
from shareplum import Site
from shareplum import Office365


#Sharepoint site information
server_url = "https://"
site_url = "https://"

username = "@yash.com"
passwd = ""
leave_mgmt_list = 'lm_emp_leave_balance_record'

#Get Authentication cookies
authcookie = Office365(server_url, username = username, password = passwd).GetCookies()

#Get all the data from sharepoint list
site = Site(site_url, authcookie=authcookie)
sp_list = site.List(leave_mgmt_list)
#data = sp_list.GetListItems(fields=['emp_id', 'sick_leave', 'casual_leave', 'accumulated_leave'])


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




#Run the app on All IP and 8081 port
app.run(host='0.0.0.0' , port=8081)

