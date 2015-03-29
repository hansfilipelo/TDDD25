# -----------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# -----------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 31 July 2013
#
# Copyright 2012 Linkoping University
# -----------------------------------------------------------------------------

import random

"""Module for the distributed mutual exclusion implementation.

This implementation is based on the second Rikard-Agravara algorithm.
The implementation should satisfy the following requests:
    --  when starting, the peer with the smallest id in the peer list
        should get the token.
    --  access to the state of each peer (dictinaries: request, token,
        and peer_list) should be protected.
    --  the implementation should gratiously handle situations when a
        peer dies unexpectedly. All exceptions comming from calling
        peers that have died, should be handled such as the rest of the
        peers in the system are still working. Whenever a peer has been
        detected as dead, the token, request, and peer_list
        dictionaries should be updated acordingly.
    --  when the peer that has the token (either TOKEN_PRESENT or
        TOKEN_HELD) quits, it should pass the token to some other peer.
    --  For simplicity, we shall not handle the case when the peer
        holding the token dies unexpectedly.

"""

NO_TOKEN = 0
TOKEN_PRESENT = 1
TOKEN_HELD = 2


class DistributedLock(object):

    """Implementation of distributed mutual exclusion for a list of peers.

    Public methods:
        --  __init__(owner, peer_list)
        --  initialize()
        --  destroy()
        --  register_peer(pid)
        --  unregister_peer(pid)
        --  acquire()
        --  release()
        --  request_token(time, pid)
        --  obtain_token(token)
        --  display_status()

    """

    def __init__(self, owner, peer_list):
        self.peer_list = peer_list
        self.owner = owner
        self.time = 0
        self.token = None
        self.request = {}
        self.state = NO_TOKEN

    def _prepare(self, token):
        """Prepare the token to be sent as a JSON message.

        This step is necessary because in the JSON standard, the key to
        a dictionary must be a string while in the token the key is
        integer.
        """
        return list(token.items())

    def _unprepare(self, token):
        """The reverse operation to the one above."""
        return dict(token)

    # Public methods

    def initialize(self):
        """ Initialize the state, request, and token dicts of the lock.
        
        Since the state of the distributed lock is linked with the
        number of peers among which the lock is distributed, we can
        utilize the lock of peer_list to protect the state of the
        distributed lock (strongly suggested).

        NOTE: peer_list must already be populated when this
        function is called.
        
        """
        
        self.peer_list.lock.acquire()
        if self.peer_list.get_peers() and min(self.peer_list.get_peers().keys()) != self.owner.id:
            self.token = {self.owner.id: self.time}
            self.request = {self.owner.id: self.time}
            for pid in self.peer_list.get_peers().keys():
                self.token.update({pid: 0})
                self.request.update({pid: 0})
        else:
            self.token = {self.owner.id: self.time}
            self.state = TOKEN_PRESENT
        self.peer_list.lock.release()

    def destroy(self):
        """ The object is being destroyed.

        If we have the token (TOKEN_PRESENT or TOKEN_HELD), we must
        give it to someone else.
        """
        self.peer_list.lock.acquire()
        if self.state in list((TOKEN_PRESENT, TOKEN_HELD)) and self.peer_list.get_peers():
            
            self.release()
            
            if self.state != NO_TOKEN:
                for key in list(self.peer_list.get_peers().keys()):
                    self.peer_list.peer(key).obtain_token(self._prepare(self.token))
                    self.state = NO_TOKEN
                    break
        self.peer_list.lock.release()
        
    def register_peer(self, pid):
        """Called when a new peer joins the system."""
        
        self.peer_list.lock.acquire()
        self.token[pid] = 0
        self.request[pid] = 0
        self.peer_list.lock.release()
        

    def unregister_peer(self, pid):
        """Called when a peer leaves the system."""
        
        self.peer_list.lock.acquire()
        del self.token[pid]
        del self.request[pid]
        self.peer_list.lock.release()
        

    def acquire(self):
        """Called when this object tries to acquire the lock."""
        print("Trying to acquire the lock...")
        self.peer_list.lock.acquire()
        self.time = self.time + 1
        
        if self.state == NO_TOKEN:
            self.peer_list.lock.release()
            for id in self.peer_list.get_peers():
                print("Requesting token from id: " + str(id))
                try:
                    self.peer_list.get_peers()[id].request_token(self.time, self.owner.id)
                except Exception as e:
                    print(type(e).__name__ + " - Arguments: ", end="")
                    print(e.args)
            while self.state != TOKEN_HELD:
                pass
            
        if self.state == TOKEN_PRESENT:
            self.obtain_token(self._prepare(self.token))
            self.peer_list.lock.release()
        

    def release(self):
        """Called when this object releases the lock."""
        
        self.peer_list.lock.acquire()
        
        self.state = TOKEN_PRESENT
        
        # Create a list that starts with our ID and goes higher, then cycles to lower IDs
        peers = list(self.peer_list.get_peers().keys())
        print(peers)
        frontOfPeers = []
        backOfPeers = []
        
        i = 0
        stop = len(peers)
        while i < stop:
            if peers[i] > self.owner.id:
                frontOfPeers.append(peers[i])
            else:
                backOfPeers.append(peers[i])
            i = i + 1
        
        peers = frontOfPeers + backOfPeers
        # ------
        
        for id in peers:
            if self.request[id] > self.token[id]:
                self.state = NO_TOKEN
                self.token[self.owner.id] = self.time
                self.peer_list.get_peers()[id].obtain_token(self._prepare(self.token))
                break
            
        self.peer_list.lock.release()

    def request_token(self, time, pid):
        """Called when some other object requests the token from us."""
        
        self.peer_list.lock.acquire()
        
        self.request[pid] = max(self.request[pid],time)
        
        if self.state == TOKEN_PRESENT and time > self.token[pid]:
            self.peer_list.get_peers()[pid].obtain_token(self._prepare(self.token))
            self.state = NO_TOKEN
        
        self.peer_list.lock.release()
        

    def obtain_token(self, token):
        """Called when some other object is giving us the token."""
        print("Receiving the token...")
        
        self.peer_list.lock.acquire()
        
        self.token = self._unprepare(token)
        if self.time > self.token[self.owner.id]:
            self.token[self.owner.id] = self.time
            self.state = TOKEN_HELD
        else:
            self.state = TOKEN_PRESENT
        
        self.peer_list.lock.release()

    def display_status(self):
        """Print the status of this peer."""
        self.peer_list.lock.acquire()
        try:
            nt = self.state == NO_TOKEN
            tp = self.state == TOKEN_PRESENT
            th = self.state == TOKEN_HELD
            print("State   :: no token      : {0}".format(nt))
            print("           token present : {0}".format(tp))
            print("           token held    : {0}".format(th))
            print("Request :: {0}".format(self.request))
            print("Token   :: {0}".format(self.token))
            print("Time    :: {0}".format(self.time))
        finally:
            self.peer_list.lock.release()
