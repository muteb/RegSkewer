import json
import logging
import traceback
from collections import OrderedDict
from lib.helper import convert_datetime
from lib.helper import ComplexEncoder
from lib.hive_yarp import get_hive
from yarp import *
# import struct
import binascii
import codecs
import string
from win32com.shell import shell
import codecs
from construct import *
from lib.helper import convert_datetime,from_fat
import datetime

class LastVisitedMRU():

    def __init__(self,prim_hive,log_files):
        self.prim_hive = prim_hive
        self.log_files = log_files

    def run(self):
        lst=[]
        LastVisitedPidMRU_settings_path = u"\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\LastVisitedPidlMRU"
        hive = get_hive(self.prim_hive,self.log_files)
        LastVisitedPidMRU_settings_key = hive.find_key(LastVisitedPidMRU_settings_path)
        if LastVisitedPidMRU_settings_key:
            if LastVisitedPidMRU_settings_key:
                sid_name = LastVisitedPidMRU_settings_key.name()
                dat_key =LastVisitedPidMRU_settings_key.last_written_timestamp().isoformat()
                cat = sid_name
                sid_key_values = iter(LastVisitedPidMRU_settings_key.values())
                while True:
                    try:
                        value = next(sid_key_values)
                        value_name = value.name()
                        if value_name != "MRUListEx" or value_name !="(Default)":
                            data = value.data()
                            format = Struct(
                                    'filename' / CString("utf16"),
                                    'CreationDate' /Int32ul
                                )
                            File_name = format.parse(data)

                            File_name = File_name.filename

                            data = data.hex()
                            data = data.split("0400efbe")
                            path = ""
                            counter = 0
                            a_time=""
                            c_time=""
                            for d in data:
                                if counter == 0 :
                                    a_time = "1601-01-01T00:00:00.00"
                                else:
                                    dax =bytes.fromhex(d)
                                    format = Struct(
                                            'CreationDate' / Bytes(4),
                                            'AccessDate' / Bytes(4),
                                            'idntifier'/ Bytes(4),
                                            'MFT_entry'/ Bytes(6),
                                            'sequence'/ Bytes(16),
                                            'unkowun' /Bytes(4),
                                            'Path' /CString("utf16")

                                        )
                                    dd = format.parse(dax)
                                    path += "\\"+dd.Path
                                    cc_time = dd.CreationDate
                                    aa_time = dd.AccessDate
                                    c_time  = from_fat(cc_time.hex())
                                    a_time = from_fat(aa_time.hex())




                                counter = counter + 1
                                if value_name == "MRUListEx":
                                    pass
                                else:
                                    record = OrderedDict([
                                        ("SequenceNumber", value_name),
                                        ("Key_timestamp", dat_key),
                                        ("CreationDate",c_time),
                                        ("AccessDate",a_time),
                                        ("@timestamp", a_time),
                                        ("File_name", File_name),
                                        ("path", path)
                                    ])
                            lst.append(u"{}".format(json.dumps(record, cls=ComplexEncoder)))

                    except StopIteration:
                        break
                    except Exception as error:
                        logging.error(u"Error getting next value: {}".format(error))
                        continue
                return lst
            else:
                logging.info(u"[{}] {} not found.".format('LastVisitedPidMRU', LastVisitedPidMRU_settings_path))
