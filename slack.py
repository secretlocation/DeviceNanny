#
# Slack Messages
# Hudl
#
# Created by Ethan Seyl 2016
#

import configparser
import logging
import slacker
import os

working_dir = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read('{}/config/DeviceNanny.ini'.format(working_dir))

slack = slacker.Slacker(config['SLACK']['ApiKey'])
channel = config['SLACK']['channel']
team_channel = config['SLACK']['team_channel']


def help_message(device_name):
    """
    Sends a message to the device checkout slack channel that a device was taken
    without being checked out.
    :param device_name: Name of device taken
    """
    slack.chat.post_message(
        channel,
        "`{}` was taken without being checked out! Please remember to enter your name or ID "
        "after taking a device.".format(device_name),
        as_user=True,
        username="device-nanny")
    logging.debug("[slack][help_message] Help message sent.")


def user_reminder(slack_id, time_difference, device_name):
    """
    Sends a checkout expired reminder.
    :param slack_id: ID of user who checked out device
    :param time_difference: Time since device was checked out
    :param device_name: Name of expired device
    """
    try:
        slack.chat.post_message(
            slack_id,
            "It's been *{}* since you checked out `{}`. Please renew your checkout online or return it "
            "to the device lab.".format(time_difference, device_name),
            as_user=True,
            username="device-nanny")
        logging.debug("[slack][user_reminder] Reminder sent to user sent")
    except Exception as e:
        logging.warning("[slack][user_reminder] Incorrect Slack ID.")


def check_out_notice(user_info, device):
    """
    Sends a slack message confirming a device was checked out.
    :param user_info: First Name, Last Name, SlackID, Office of user who checked out device
    :param device: Device taken
    """
    slack.chat.post_message(
        user_info.get('SlackID'),
        "You checked out `{}`. Checkout will expire after 3 days. Remember to plug the "
        "device back in when you return it to the lab. You can renew your checkout from "
        "the DeviceNanny web page.".format(device),
        as_user=True,
        username="device-nanny")
    slack.chat.post_message(
        channel,
        "*{} {}* just checked out `{}`".format(
            user_info.get('FirstName'), user_info.get('LastName'), device),
        as_user=True,
        username="device-nanny")
    logging.debug("[slack][check_out_notice] Checkout message sent.")


def check_in_notice(user_info, device):
    """
    Sends a slack message confirming a device was checked in.
    :param user_info: First Name, Last Name, SlackID, Office of user who checked in device
    :param device: Device returned
    """
    logging.debug("[slack][check_in_notice] SlackID from user_info: {}".format(
        user_info.get('SlackID')))
    if user_info.get("FirstName") != "Missing":
        try:
            slack.chat.post_message(
                user_info.get('SlackID'),
                "You checked in `{}`. Thanks!".format(device),
                as_user=True,
                username="device-nanny")
            slack.chat.post_message(
                channel,
                "*{} {}* just checked in `{}`".format(
                    user_info.get('FirstName'),
                    user_info.get('LastName'), device),
                as_user=True,
                username="device-nanny")
            logging.debug(
                "[slack][check_in_notice] {} {} just checked in {}".format(
                    user_info.get('FirstName'),
                    user_info.get('LastName'), device))
        except Exception as e:
            print(str(e))


def post_to_channel(device_id, time_difference, firstname, lastname):
    """
    Sends a slack message to the device checkout channel with an update for an expired checkout.
    :param device_id: Device ID of device taken
    :param time_difference: Time since device was checked out
    :param firstname: First name of user with expired checkout
    :param lastname: Last name of user with expired checkout
    """
    slack.chat.post_message(
        channel,
        '`{}` was checked out *{}* ago by *{} {}*'.format(
            device_id, time_difference, firstname, lastname),
        as_user=True,
        username="device-nanny")
    logging.debug("[slack][post_to_channel] Posted to channel.")


def nanny_check_in(device_name):
    """
    Sends slack message to the device checkout channel. Sent when the Nanny discovers a
    connected device that wasn't checked in.
    :param device_name: Name of device checked in
    """
    slack.chat.post_message(
        channel,
        "`{}` was checked in by the Nanny.".format(device_name),
        as_user=True,
        username="device-nanny")
    logging.debug("[slack][nanny_check_in] Nanny check-in message sent.")


def missing_device_message(device_name, time_difference):
    """
    Send a message to the office channel about a device that's been missing from the lab
    for more than the set checkout time.
    :param device_name:
    :param time_difference:
    :return:
    """
    slack.chat.post_message(
        team_channel,
        "`{}` has been missing from the device lab for `{}`. If you have it, please return the device to the lab "
        "and check it out under your name.".format(device_name,
                                                   time_difference),
        as_user=True,
        username="device-nanny")
    logging.info(
        "[slack][missing_device_message] Slack reminder sent to team channel for {}".
        format(device_name))
