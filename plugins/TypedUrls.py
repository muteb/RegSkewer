import json
import logging
import traceback
from collections import OrderedDict
from lib.helper import convert_datetime
from lib.helper import ComplexEncoder
from lib.hive_yarp import get_hive
from yarp import *
from lib.helper import strip_control_characters

class TypedUrls():

    def __init__(self,prim_hive,log_files):
        self.prim_hive = prim_hive
        self.log_files = log_files

    def run(self):
        lst = []
        TypedUrls_user_settings_path = u"Software\\Microsoft\\Internet Explorer\\TypedURLs"
        hive = get_hive(self.prim_hive,self.log_files)
        TypedUrls_user_settings_key = hive.find_key(TypedUrls_user_settings_path)
        if TypedUrls_user_settings_key:
            #for sid_key in TypedUrls_user_settings_key.subkeys():
            sid_key_values = iter(TypedUrls_user_settings_key.values())
            while True:
                try:
                    value = next(sid_key_values)
                except StopIteration:
                    break
                except Exception as error:
                    logging.error(u"Error getting next value: {}".format(error))
                    continue

                value_name = value.name()
                url_data =value.data()
                timestamp = TypedUrls_user_settings_key.last_written_timestamp().isoformat()
                record = OrderedDict([
                    ("Key_Timestamp",timestamp),
                    ("Url Name", value_name),
                    ("Url", strip_control_characters(url_data)),
                    ("@timestamp",timestamp)
                ])

                lst.append(u"{}".format(json.dumps(record, cls=ComplexEncoder)))

        else:
            logging.info(u"[{}] {} not found.".format('TypedUrls', TypedUrls_user_settings_path))

        return lst
