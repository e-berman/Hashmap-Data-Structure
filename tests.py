import unittest
from hash_map import *


class TestCase(unittest.TestCase):

    def test_add_bucket(self):
        map = HashMap(100, hash_function_1)
        map.put('key1', 10)
        current_size = map.size

        self.assertLess(
            map.empty_buckets(), map.capacity,
            msg='Empty buckets matches bucket capacity! empty {} capacity {}'.format(
                map.empty_buckets(), map.capacity
            ))
        self.assertGreater(
            map.size, 0,
            msg='Size did not increment! prior size {} current size {}'.format(
                current_size, map.size
            ))
    
    def test_table_load(self):
        map = HashMap(100, hash_function_1)
        for i in range(5):
            map.put('key' + str(i), i * 10)
        self.assertEqual(
            map.table_load(), 0.05,
            msg='Table load does not match expected value. Expected {} current {}'.format(
                0.05, map.table_load()
            ))

    def test_clearing_size(self):
        map = HashMap(100, hash_function_1)
        map.put('key1', 10)
        map.put('key2', 20)
        map.clear()
        self.assertEqual(
            map.size, 0,
            msg='After cleared, size should be 0. Expected {} Current Size {}'.format(
                0, map.size
            ))
        
    def test_clear_on_table_resize(self):
        map = HashMap(50, hash_function_1)
        map.put('key1', 10)
        map.put('key2', 20)
        map.resize_table(100)
        map.clear()
        self.assertEqual(
            map.capacity, 100,
            msg='Table was not resized properly. Current capacity {}'.format(
                map.capacity
            ))
        self.assertEqual(
            map.size, 0,
            msg='After clear, size should be 0. Current Size {}'.format(
                map.size
            ))

    def test_contains_key(self):
        map = HashMap(10, hash_function_1)
        self.assertFalse(
            map.contains_key('key1'),
            msg='Hashmap should be empty.'
        )
        map.put('key1', 10)
        map.put('key2', 20)
        self.assertTrue(
            map.contains_key('key1'),
            msg='Hashmap should contain \'key1\''
        )
        map.remove('key1')
        self.assertFalse(
            map.contains_key('key1'),
            msg='Hashmap removed \'key1\'and should return False.'
        )
    
    def test_get(self):
        map = HashMap(150, hash_function_2)
        for i in range(200, 300, 7):
            map.put(str(i), i * 10)
        for i in range(200, 300, 21):
            self.assertIsNotNone(
                map.get(str(i)),
                msg='{} is not None'.format(
                    map.get(str(i))
                ))
            self.assertIsNone(
                map.get(str(i+1)),
                msg='{} should be a value, not None.'.format(
                    map.get(str(i+1))
                ))

    def test_remove(self):
        map = HashMap(50, hash_function_1)
        map.put('key1', 10)
        self.assertIsNotNone(
            map.get('key1'),
            msg='key1 is not in the hashmap'
        )

        map.remove('key1')
        self.assertIsNone(
            map.get('key1'),
            msg='The key exists in the hashmap'
        )

    def test_table_resize(self):
        map = HashMap(20, hash_function_1)
        map.put('key1', 10)
        self.assertTrue(
            map.contains_key('key1'),
            msg='Key not in hashmap'
        )

        map.resize_table(30)
        self.assertEqual(
            30, map.capacity,
            msg='Table capacity is incorrect. Current capacity {}'.format(
                map.capacity
            ))

    def test_get_keys(self):
        key_list = ['160', '110', '170', '120', '180', '130', '190', '140', '150', '100']
        mod_key_list = ['200', '160', '110', '170', '120', '180', '130', '190', '140', '150']

        map = HashMap(10, hash_function_2)
        for i in range(100, 200, 10):
            map.put(str(i), str(i * 10))

        for key1 in range(len(key_list)):
            self.assertEqual(
                key_list[key1], map.get_keys()[key1],
                msg='Key lists do not match. \
                    Current list: {}'.format(
                        map.get_keys()
                    ))
        
        map.resize_table(1)
        map.put('200', '2000')
        map.remove('100')
        map.resize_table(2)

        for key2 in range(len(mod_key_list)):
            self.assertEqual(
                mod_key_list[key2], map.get_keys()[key2],
                msg='Key lists do not match. \
                    Current list: {}'.format(
                        map.get_keys()
                    ))