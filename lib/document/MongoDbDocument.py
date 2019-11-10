#!/usr/bin/python3

from pymongo import MongoClient

from lib.document import BaseDocument
from lib.const import ConfigKey


class MongoDbDocument(BaseDocument):
    def __init__(self, config):
        super(MongoDbDocument, self).__init__(config)
        self.dbType = 'mongodb'
        self.db = MongoClient(self.engine.hostname, self.engine.port).kiku

    def addVmstatLog(self, timestamp, hostname, type, group, cpu_ratio, cpu_user, cpu_system, cpu_idle, cpu_wait, cpu_steal, mem_ratio, mem_free, mem_buffer, mem_cache, mem_swapped, swap_in, swap_out, io_in, io_out, option=None):
        collection = self.db.VmstatLog
        collection.insert_one(
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
            })

    def addDfLog(self, timestamp, hostname, type, group, filesystem, fs_type, blocks, used, available, ratio, mounted_path, option=None):
        collection = self.db.DfLog
        collection.insert_one(
            {
                'timestamp': timestamp,
                'hostname': hostname,
                'type': type,
                'group': group,
                'storage': {
                    'filesystem': filesystem,
                    'type': fs_type,
                    '1k_blocks': blocks,
                    'used': used,
                    'available': available,
                    'ratio': ratio,
                    'mounted_path': mounted_path
                },
                'option': option
            })

    def searchCpuLog(self, hostname, time_from, time_to):
        collection = self.db.VmstatLog
        query = {
            '$and': [
                {'hostname': hostname},
                {'timestamp': {'$gt': time_from, '$lt': time_to}}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'cpu': True}))

    def searchMultipleCpuLog(self, hostnames, time_from, time_to):
        collection = self.db.VmstatLog
        query = {
            '$and': [
                {
                    '$or': list(map(lambda x: {'hostname': x}, hostnames))
                },
                {'timestamp': {'$gt': time_from, '$lt': time_to}}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'hostname': True, 'cpu.ratio': True}))

    def latestCpuLog(self, hostname):
        collection = self.db.VmstatLog
        query = {
            '$and': [
                {'hostname': hostname}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'cpu.ratio': True}).sort('timestamp', -1).limit(1))

    def searchMemoryLog(self, hostname, time_from, time_to):
        collection = self.db.VmstatLog
        query = {
            '$and': [
                {'hostname': hostname},
                {'timestamp': {'$gt': time_from, '$lt': time_to}}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'memory': True}))

    def searchMultipleMemoryLog(self, hostnames, time_from, time_to):
        collection = self.db.VmstatLog
        query = {
            '$and': [
                {
                    '$or': list(map(lambda x: {'hostname': x}, hostnames))
                },
                {'timestamp': {'$gt': time_from, '$lt': time_to}}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'hostname': True, 'memory.ratio': True}))

    def latestMemoryLog(self, hostname):
        collection = self.db.VmstatLog
        query = {
            '$and': [
                {'hostname': hostname}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'memory.ratio': True}).sort('timestamp', -1).limit(1))

    def searchSwapLog(self, hostname, time_from, time_to):
        collection = self.db.VmstatLog
        query = {
            '$and': [
                {'hostname': hostname},
                {'timestamp': {'$gt': time_from, '$lt': time_to}}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'memory.swapped': True}))

    def searchMultipleSwapLog(self, hostnames, time_from, time_to):
        collection = self.db.VmstatLog
        query = {
            '$and': [
                {
                    '$or': [
                        list(map(lambda x: {'hostname': x}, hostnames))
                    ]
                },
                {'timestamp': {'$gt': time_from, '$lt': time_to}}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'hostname': True, 'memory.swapped': True}))

    def latestSwapLog(self, hostname):
        collection = self.db.VmstatLog
        query = {
            '$and': [
                {'hostname': hostname}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'memory.swapped': True}).sort('timestamp', -1).limit(1))

    def addStorageLog(self, timestamp, hostname, type, group, device_name, ratio, option=None):
        collection = self.db.StorageLog
        collection.insert_one(
            {
                'timestamp': timestamp,
                'hostname': hostname,
                'type': type,
                'group': group,
                'device_name': device_name,
                'ratio': ratio,
                'option': option
            })

    def searchTargetStorageLog(self, hostname, mounted_path, time_from, time_to):
        collection = self.db.DfLog
        query = {
            '$and': [
                {'hostname': hostname},
                {'storage.mounted_path': mounted_path},
                {'timestamp': {'$gt': time_from, '$lt': time_to}}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'storage.ratio': True}))

    def searchStorageLog(self, hostname, time_from, time_to):
        collection = self.db.DfLog
        query = {
            '$and': [
                {'hostname': hostname},
                {'timestamp': {'$gt': time_from, '$lt': time_to}}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'storage.ratio': True, 'storage.mounted_path': True}))

    def searchMultipleTargetStorageLog(self, hostnames, mounted_path, time_from, time_to):
        collection = self.db.DfLog
        query = {
            '$and': [
                {
                    '$or': [
                        list(map(lambda x: {'hostname': x}, hostnames))
                    ]
                },
                {'storage.mounted_path': mounted_path},
                {'timestamp': {'$gt': time_from, '$lt': time_to}}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'hostname': True, 'storage.ratio': True}))

    def latestTargetStorageLog(self, hostname, mounted_path):
        collection = self.db.DfLog
        query = {
            '$and': [
                {'hostname': hostname},
                {'storage.mounted_path': mounted_path}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'storage.ratio': True}).sort('timestamp', -1).limit(1))

    def searchIoLog(self, hostname, time_from, time_to):
        collection = self.db.VmstatLog
        query = {
            '$and': [
                {'hostname': hostname},
                {'timestamp': {'$gt': time_from, '$lt': time_to}}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'io.block_in': True, 'io.block_out': True}))

    def searchMultipleIoLog(self, hostnames, io_type, time_from, time_to):
        collection = self.db.VmstatLog
        query = {
            '$and': [
                {
                    '$or': [
                        list(map(lambda x: {'hostname': x}, hostnames))
                    ]
                },
                {'timestamp': {'$gt': time_from, '$lt': time_to}}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'hostname': True, io_type: True}))

    def latestIoLog(self, hostname):
        collection = self.db.VmstatLog
        query = {
            '$and': [
                {'hostname': hostname}
            ]
        }
        return list(collection.find(query, {'_id': False, 'timestamp': True, 'io.block_in': True, 'io.block_out': True}).sort('timestamp', -1).limit(1))
