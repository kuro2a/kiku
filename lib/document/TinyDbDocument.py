#!/usr/bin/python3

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage

from lib.document import BaseDocument
from lib.const import ConfigKey


def get_json_time(timestamp):
    return '{0:04d}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}.{6:03d}Z'.format(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second, timestamp.microsecond % 1000)


class TinyDbDocument(BaseDocument):
    def __init__(self, config):
        super(TinyDbDocument, self).__init__(config)
        self.dbType = 'tinydb'
        self.db = TinyDB('.{0}'.format(self.engine.path))

    def addOsLog(self, timestamp, hostname, type, group, cpu_ratio, cpu_user, cpu_system, cpu_idle, cpu_wait, cpu_steal, mem_ratio, mem_free, mem_buffer, mem_cache, mem_swapped, swap_in, swap_out, io_in, io_out, option=None):
        self.db.insert(
            {'os':
                {
                    'timestamp': timestamp,
                    'hostname': hostname,
                    'type': type,
                    'group': group,
                    'cpu': {
                        'ratio': cpu_ratio,
                        'user': cpu_user,
                        'sys': cpu_system,
                        'idle': cpu_idle,
                        'wait': cpu_wait,
                        'steal': cpu_steal
                    },
                    'memory': {
                        'ratio': mem_ratio,
                        'free': mem_free,
                        'buff': mem_buffer,
                        'cache': mem_cache,
                        'swapped': mem_swapped
                    },
                    'swap': {
                        'swap_in': swap_in,
                        'swap_out': swap_out
                    },
                    'io': {
                        'block_in': io_in,
                        'block_out': io_out
                    },
                    'option': option
                }
             })

    def addCpuLog(self, timestamp, hostname, type, group, total_ratio, option=None):
        self.db.insert({
            "cpu": {
                "timestamp": get_json_time(timestamp),
                "hostname": hostname,
                "type": type,
                "group": group,
                "total_ratio": total_ratio,
                "option": option
            }
        })

    def searchCpuLog(self, hostname, time_from, time_to):
        q = Query()
        res = []
        for i in self.db.search((q.cpu.hostname == hostname) & (q.cpu.timestamp >= get_json_time(time_from)) & (q.cpu.timestamp <= get_json_time(time_to))):
            res.append(
                {'timestamp': i['cpu']['timestamp'], 'ratio': i['cpu']['ratio']})
        return res

    def latestCpuLog(self, hostname):
        q = Query()
        res = []
        latest_log = max(self.db.search(
            (q.cpu.hostname == hostname)), key=lambda x: x['cpu']['timestamp'])
        res.append(
            {'timestamp': latest_log['cpu']['timestamp'], 'ratio': latest_log['cpu']['ratio']})
        return res

    def addMemoryLog(self, timestamp, hostname, type, group, ratio, option=None):
        self.db.insert({
            "memory": {
                "timestamp": get_json_time(timestamp),
                "hostname": hostname,
                "type": type,
                "group": group,
                "ratio": ratio,
                "option": option
            }
        })

    def searchMemoryLog(self, hostname, time_from, time_to):
        q = Query()
        res = []
        for i in self.db.search((q.memory.hostname == hostname) & (q.memory.timestamp >= get_json_time(time_from)) & (q.memory.timestamp <= get_json_time(time_to))):
            res.append(
                {'timestamp': i['memory']['timestamp'], 'ratio': i['memory']['ratio']})
        return res

    def latestMemoryLog(self, hostname):
        q = Query()
        res = []
        latest_log = max(self.db.search(
            (q.memory.hostname == hostname)), key=lambda x: x['memory']['timestamp'])
        res.append(
            {'timestamp': latest_log['memory']['timestamp'], 'ratio': latest_log['memory']['ratio']})
        return res

    def addSwapLog(self, timestamp, hostname, type, group, ratio, option=None):
        self.db.insert({
            "swap": {
                "timestamp": get_json_time(timestamp),
                "hostname": hostname,
                "type": type,
                "group": group,
                "ratio": ratio,
                "option": option
            }
        })

    def searchSwapLog(self, hostname, time_from, time_to):
        q = Query()
        res = []
        for i in self.db.search((q.swap.hostname == hostname) & (q.swap.timestamp >= get_json_time(time_from)) & (q.swap.timestamp <= get_json_time(time_to))):
            res.append(
                {'timestamp': i['swap']['timestamp'], 'ratio': i['swap']['ratio']})
        return res

    def latestSwapLog(self, hostname):
        q = Query()
        res = []
        latest_log = max(self.db.search(
            (q.swap.hostname == hostname)), key=lambda x: x['swap']['timestamp'])
        res.append(
            {'timestamp': latest_log['swap']['timestamp'], 'ratio': latest_log['swap']['ratio']})
        return res

    def addStorageLog(self, timestamp, hostname, type, group, device_name, ratio, option=None):
        self.db.insert({
            "storage": {
                "timestamp": get_json_time(timestamp),
                "hostname": hostname,
                "type": type,
                "group": group,
                "device_name": device_name,
                "ratio": ratio,
                "option": option
            }
        })

    def searchStorageLog(self, hostname, device_name, time_from, time_to):
        q = Query()
        res = []
        for i in self.db.search((q.storage.hostname == hostname) & (q.storage.device_name == device_name) & (q.storage.timestamp >= get_json_time(time_from)) & (q.storage.timestamp <= get_json_time(time_to))):
            res.append(i['storage'])
        return res

    def latestStorageLog(self, hostname, device_name):
        q = Query()
        res = []
        latest_log = max(self.db.search((q.storage.hostname == hostname) & (
            q.storage.device_name == device_name)), key=lambda x: x['storage']['timestamp'])
        res.append(
            {'timestamp': latest_log['storage']['timestamp'], 'ratio': latest_log['storage']['ratio']})
        return res

    def addIoLog(self, timestamp, hostname, type, group, read, write, option=None):
        self.db.insert({
            "diskio": {
                "timestamp": get_json_time(timestamp),
                "hostname": hostname,
                "type": type,
                "group": group,
                'read': input,
                'write': write,
                "option": option
            }
        })

    def searchIoLog(self, hostname, time_from, time_to):
        q = Query()
        res = []
        for i in self.db.search((q.diskio.hostname == hostname) & (q.diskio.timestamp >= get_json_time(time_from)) & (q.diskio.timestamp <= get_json_time(time_to))):
            res.append(i['diskio'])
        return res

    def latestIoLog(self, hostname):
        q = Query()
        res = []
        latest_log = max(self.db.search(
            (q.diskio.hostname == hostname)), key=lambda x: x['diskio']['timestamp'])
        res.append(
            {'timestamp': latest_log['diskio']['timestamp'], 'read': latest_log['diskio']['read'], 'write': latest_log['diskio']['write']})
        return res
