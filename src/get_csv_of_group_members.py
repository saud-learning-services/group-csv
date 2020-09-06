import pandas as pd
from canvasapi import Canvas
import getpass
import sys
from IPython.display import display, HTML
from helpers import createCSV, createInstance, getCourseFromID
from datetime import datetime

OUTPUT = "output"

def getGroupData():
    # ask for the API_KEY
    API_KEY = getpass.getpass("Enter Token: ")

    try: 
        course_id, course = getCourseFromID(createInstance(API_URL, API_KEY))
        groups = course.get_groups(per_page=50)
        course_name = course.name

        all_groups = []

        for group in groups:
            
            users_list = group.get_users()
            
            for user in users_list:
                group_dict = {}
                group_dict['group_id'] = group.id
                group_dict['group_name'] = group.name
                #group_dict['group_created_at'] = group.created_at
                group_dict['course_name'] = course.name
                group_dict['course_id'] = course.id
                #print(group, user)
                group_dict['user_id']= user.id
                group_dict['user_name']= user.name
            
                all_groups.append(group_dict)

            # membership_list = group.get_memberships()
            # for member in membership_list:
            #     group_dict['moderator'] = member.moderator
            #     #group_dict['workflow_state'] = member.workflow_state
            #     #group_dict['membership_id'] = member.id
            
        return(pd.DataFrame(all_groups), course_id, course_name)

    except Exception as e:
        print("Something went wrong: {}".format(str(e)))
        sys.exit(1)


# use the df created in previous steps (Jupyter only)
# confirm 

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H%M%S")

df, course_id, course_name = getGroupData()
display(df)
output_name = "{}/{}_{}_Group Information_{}.csv".format(OUTPUT, course_id, course_name, timestamp)
createCSV(df, output_name)