import pandas as pd
from email_config import EmailConfig
from jinja2 import Environment, FileSystemLoader
class EmailSender:
    @staticmethod
    def read_template(template_file):
        with open(template_file, 'r') as file:
            return file.read()

    @staticmethod
    def send_email_from_csv(job_info_csv, template_file):
        # Read the CSV file
        job_info_df = pd.read_csv(job_info_csv)
        
        # Iterate through each job entry
        for _, row in job_info_df.iterrows():
            # Extract job information
            recipient_email = row['Recipient Email']
            job_name = row['Job Name']
            jobId = row['Job Id']
            job_status = row['Job Status']
            execution_time = row['Execution Time']
            error_message = row['Error Message'] if job_status == 'Failed' else ""
            date= row['Date']
            start_time = row['Start Time']
            end_time= row['End Time']
            # Load the HTML template

            context = {
                'recipient_name': recipient_email.split("@")[0],  # Extracting the name from email
                'job_name': job_name,
                'job_id':jobId,
                'job_status': job_status,
                'execution_time': execution_time,
                'error_message': error_message,
                'Date': date,
                'start_time': start_time,
                'end_time': end_time
            }

            env = Environment(loader=FileSystemLoader('templates'))
            #template = EmailSender.read_template(template_file)
            template = env.get_template(template_file)
            html_content  = template.render(context)
            
            # Replace placeholders in the template
            #html_content = template.replace("{{ recipient_name }}", recipient_email.split("@")[0])
            #html_content = html_content.replace("{{ job_name }}", job_name)
            #html_content = html_content.replace("{{ job_status }}", job_status)
            #html_content = html_content.replace("{{ execution_time }}", execution_time)
            #html_content = html_content.replace("{{ error_message }}", error_message)
            
            # Send the email
            subject = f"Job {job_name} {job_status}"
            EmailConfig.send_email(recipient_email, subject, html_content)
