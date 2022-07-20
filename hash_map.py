
# Import DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def hash_index(self, key: str) -> int:
        '''Gets the hash index based on the passed key and relevant hash function'''
        # computes hash value of key, then computes index value based on prior hash value. Returns index value.
        hash = self.hash_function(key)
        index = hash % self.capacity

        return index

    def clear(self) -> None:
        '''Clears the contents of the hash map. Does not change capacity.'''
        self.size = 0

        # iterate through buckets dynamic array, and set a new linked list at each index
        for link in range(self.capacity):
            self.buckets.set_at_index(link, LinkedList())
        

    def get(self, key: str) -> object:
        '''Gets the value of a passed key if in hash map, returns None otherwise'''

        # find relevant bucket based on hash index and specified bucket's length
        index = self.hash_index(key)
        bucket = self.buckets[index]
        bucket_length = bucket.length()

        # iterate through bucket contents. If key is in bucket contents, return the value. If not, return None.
        while bucket_length != 0:
            if bucket.contains(key) != None:
                node = bucket.contains(key)
                return node.value
            bucket_length -= 1

        return None

    def put(self, key: str, value: object) -> None:
        '''Updates the key/value pair in the hashmap'''

        # find relevant bucket based on hash index and specified bucket's length
        index = self.hash_index(key)
        bucket = self.buckets[index]
        bucket_length = bucket.length()

        # if bucket is empty, insert node with key/value pair. Increment size.
        if bucket_length == 0:
            bucket.insert(key, value)
            self.size += 1
        # otherwise, iterate through bucket contents. If key is in contents, update that key's value.
        # if key is not in bucket, insert node with key/value pair. Increment size.
        else:
            while bucket_length != 0:
                if bucket.contains(key) != None:
                    node = bucket.contains(key)
                    node.value = value
                    return
                bucket_length -= 1
            bucket.insert(key, value)
            self.size += 1


    def remove(self, key: str) -> None:
        '''Removes a key/value from the hashmap'''

        # find relevant bucket based on hash index and specified bucket's length
        index = self.hash_index(key)
        bucket = self.buckets[index]
        bucket_length = bucket.length()
        
        # iterate through bucket contents. If bucket contains the node with pertaining key,
        # remove the node and decrement the size.
        while bucket_length != 0:
            if bucket.contains(key) != None:
                bucket.remove(key)
                self.size -= 1
                return
            bucket_length -= 1
                

    def contains_key(self, key: str) -> bool:
        '''Checks if hash table contains passed key'''

        # find relevant bucket based on hash index and specified bucket's length
        index = self.hash_index(key)
        bucket = self.buckets[index]
        bucket_length = bucket.length()

        # iterate through contents of bucket. If key is in the linked list, return True, if not return False.
        while bucket_length != 0:
            if bucket.contains(key) != None:
                return True
            bucket_length -= 1

        return False

    def empty_buckets(self) -> int:
        '''Returns number of empty buckets in hash table'''
        empty_buckets = 0

        # iterate through all buckets and check each buckets length.
        # if length is 0, increment empty_buckets
        for item in range(0, self.capacity):
            if self.buckets[item].length() == 0:
                empty_buckets += 1

        return empty_buckets

    def table_load(self) -> float:
        '''Returns hash table load factor'''
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        '''Resizes the table and adjusts the hashmap indices'''

        # initialize local variable(s)
        v_index = 0

        if new_capacity < 1:
            return
        else:
            # initialize two dynamic arrays: one of keys, one of values
            keys = self.get_keys()
            values = self.get_values()

            # set capacity to new_capacity, reset size to 0, set buckets equal to a new dynamic array
            self.capacity = new_capacity
            self.size = 0
            self.buckets = DynamicArray()
            
            # iterate through the buckets array and append a linked list at each index
            for _ in range(self.capacity):
                self.buckets.append(LinkedList())

            # for each key that existed prior to capacity update, rehash the index value,
            # and add key/value pair at relevant index
            for key in range(keys.length()):
                self.put(keys[key], values[v_index])
                v_index += 1

        
    def get_keys(self) -> DynamicArray:
        '''Gets the keys stored in the hash map and appends each key to a dynamic array'''

        # initialize key_array variable
        key_array = DynamicArray()

        # iterate through all buckets and check if each bucket is empty.
        # if not empty, append each existing nodes key to the key_array dynamic array.
        for item in range(self.capacity):
            if self.buckets[item].length() != 0:
                for node in self.buckets[item]:
                    key_array.append(node.key)

        return key_array

    def get_values(self) -> DynamicArray:
        '''Gets the value stored at each key and appends each value to a dynamic array'''

        # initialize values variable
        values = DynamicArray()

        # get array of keys and iterate through each key.
        keys = self.get_keys()

        # find the corresponding bucket and node for each key and append the value to the values array.
        for key in range(keys.length()):
            hash = self.hash_function(keys[key])
            index = hash % self.capacity
            bucket = self.buckets[index]
            if bucket.contains(keys[key]) != None:
                node = bucket.contains(keys[key])
                values.append(node.value)

        return values