from services.core.ConfigService import ConfigService

class NotificationService:
    
#region initialiser
    def __init__(self, config_service, email_service, slack_service):
        self._config_service = config_service
        self._email_service = email_service
        self._slack_service = slack_service
        self.__read_config()
#endregion

#region public methods
    def send(self):
        pass

    
    def send_bulk(self):
        pass
#endregion

#region private methods
    def __read_config(self):
        pass


    def __lock_message_file(self):
        self._config_service.update_config("notifications.message_file_locked", True)


    def __unlock_message_file(self):
        self._config_service.update_config("notifications.message_file_locked", False)
#endregion











import copy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from slackclient import SlackClient
from services.core.ConfigService import ConfigService
from utilities.core.DateUtils import DateUtils
from utilities.core.OsUtils import OsUtils
from utilities.core.TimeUtils import TimeUtils


class NotificationService:

#region initialiser
    def __init__(self, config_service):
        self._config_service = config_service
        self._email_enabled = False
        self._slack_enabled = False
        self._message_file_locked = True
        self._message_file = None
        self.__read_config()
#endregion


#region public methods
    def send(self, message):
        try:
            while True:
                if self._config_service.message_file_locked:
                    TimeUtils.sleep_for_time_period(3)
                else:
                    self.__lock_message_file()
                    existing_messages = self.__load_messages()

                    if self._config_service.service_name not in existing_messages:
                        existing_messages[self._config_service.service_name] = []
    
                    existing_messages[self._config_service.service_name].append({
                        "message": message,
                        "datetime": DateUtils.convert_date_to_isoformat_str(DateUtils.get_current_date_time())
                    })

                    self.__save_messages(existing_messages)
                    self.__unlock_message_file()
                    return
        except Exception as ex:
            print(ex)
        finally:
            self.__unlock_message_file()


    def process_and_send_all_messages(self):
        self.__lock_message_file()
        existing_messages = self.__load_messages()

        if existing_messages:
            if self._email_enabled:
                self.__format_and_send_email(existing_messages)

            if self._slack_enabled:
                self.__format_and_send_slack(existing_messages)

            self.__clear_message_file()
            
        self.__unlock_message_file()
#endregion


#region private methods
    def __read_config(self):
        self._email_enabled = self._config_service.email_notifications_enabled
        self._slack_enabled = self._config_service.slack_notifications_enabled
        self._message_file_locked = self._config_service.message_file_locked
        self._message_file = self._config_service.message_file


    def __lock_message_file(self):
        self._config_service.update_config("notifications.message_file_locked", True)


    def __unlock_message_file(self):
        self._config_service.update_config("notifications.message_file_locked", False)


    def __clear_message_file(self):
        OsUtils.write_to_file(self._config_service.message_file, "{}")


    def __load_messages(self):
        if not OsUtils.does_file_exist(self._message_file):
            OsUtils.write_to_file(self._message_file, "{}")

        with open(self._message_file) as message_file:
            message_json = json.load(message_file)
            message_file.close()
        return message_json


    def __save_messages(self, messages_json):
        with open(self._message_file, "w") as message_file:
            json.dump(messages_json, message_file, sort_keys=True, indent=4)


    def __format_and_send_email(self, message_groups):
        html_content = self.__generate_html_for_email(message_groups)
        text_content = self.__generate_text_for_notification(message_groups)
        self.__send_email(self._config_service.email_to_notify, "Testing the HTML formatting", text_content, html_content)


    def __generate_html_for_email(self, message_groups):
        html_template = "<html><head></head><body>{0}</body></html>"
        section_template = "<h3>{0}</h3><p>{1}</p>"
        ul_list_template = "<ul>{0}</ul>"
        list_item_template = "<li>{0}</li>"

        all_sections = ""

        for key in message_groups:
            list_items = ""
            for message_details in message_groups[key]:
                item = copy.deepcopy(list_item_template)
                list_items = list_items + item.format(message_details["message"])
            
            ul_list = copy.deepcopy(ul_list_template)
            ul_list = ul_list.format(list_items)
            section = copy.deepcopy(section_template)
            all_sections = all_sections + section.format(key, ul_list)

        return html_template.format(all_sections)


    def __generate_text_for_notification(self, message_groups):
        all_text_content = []
        for key in message_groups:
            current_text_content = ""
            for message_details in message_groups[key]:
                current_text_content = current_text_content + message_details["message"] + '\n'
            all_text_content.append(key + '\n' + current_text_content)

        text_content = ""
        for content in all_text_content:
            if text_content:
                text_content = text_content + '\n'
            text_content = text_content + content

        return text_content


    def __format_and_send_slack(self, message_groups):
        message = "```" + self.__generate_text_for_notification(message_groups) + "```"
        self.__send_slack_message(message, "notifications")


    def __send_email(self, recipient, subject, text_body, html_body):
        sent_from = self._config_service.email_username  
        to = recipient

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sent_from
        msg['To'] = to

        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')

        msg.attach(part1)
        msg.attach(part2)

        server = smtplib.SMTP_SSL(self._config_service.email_server, self._config_service.email_port)
        server.ehlo()
        server.login(self._config_service.email_username, self._config_service.email_password)
        server.sendmail(sent_from, to, msg.as_string())
        server.close()


    def __send_slack_message(self, message, channel):
        sc = SlackClient(self._config_service.slack_token)
        sc.api_call('chat.postMessage', channel=channel, 
                    text=message, username=self._config_service.slack_username,
                    icon_emoji=':newspaper:')
#endregion
