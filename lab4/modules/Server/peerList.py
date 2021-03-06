# -----------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# -----------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 31 July 2013
#
# Copyright 2012 Linkoping University
# -----------------------------------------------------------------------------

"""Package for handling a list of objects of the same type as a given one."""

import time
import threading
from Common import orb
from Common.objectType import object_type


class PeerList(object):

    """Class that builds a list of objects of the same type as this one."""

    def __init__(self, owner):
        self.owner = owner
        self.lock = threading.Condition()
        self.peers = {}

    # Public methods

    def initialize(self):
        """Populates the list of existing peers and registers the current
        peer at each of the discovered peers.

        It only adds the peers with lower ids than this one or else
        deadlocks may occur. This method must be called after the owner
        object has been registered with the name service.

        """
        self.lock.acquire()
        try:

            for peerInfo in self.owner.name_service._rmi("require_all", object_type):
                if peerInfo[0] < self.owner.id:
                    try:
                        # We only add the peers to the list that we can reach them and register them
                        serverPeer = orb.Stub(tuple(peerInfo[1]))
                        serverPeer.register_peer(self.owner.id, self.owner.address)
                        self.peers[peerInfo[0]] = serverPeer
                        print("success to register to id: " + str(peerInfo[0]) + " added to peerList")
                    except:
                        print("failed  to register to id: " + str(peerInfo[0]))
        finally:
            self.lock.release()

    def destroy(self):
        """Unregister this peer from all others in the list."""
        
        
        self.lock.acquire()
        try:
            
            
            for peer in self.peers:
                try:
                    self.peers[peer].unregister_peer(self.owner.id)
                except:
                    print("Cant'reach peer with ID %s", peer)
                    # If we can't reach the other peer we can't do nothing later either, because this peer will be destroyed anyways
                    continue
        
        finally:
            self.lock.release()

    def register_peer(self, pid, paddr):
        """Register a new peer joining the network."""

        # Synchronize access to the peer list as several peers might call
        # this method in parallel.
        self.lock.acquire()
        try:
            self.peers[pid] = orb.Stub(paddr)
            print("Peer {} has joined the system.".format(pid))
        finally:
            self.lock.release()

    def unregister_peer(self, pid):
        """Unregister a peer leaving the network."""
        # Synchronize access to the peer list as several peers might call
        # this method in parallel.

        self.lock.acquire()
        try:
            del self.peers[pid]
        except:
            print("Failed to destroy peer %s", pid)
            raise Exception("No peer with id: '{}'".format(pid))
        finally:
            self.lock.release()

    def display_peers(self):
        """Display all the peers in the list."""

        self.lock.acquire()
        try:
            pids = sorted(self.peers.keys())
            print("List of peers of type '{}':".format(self.owner.type))
            for pid in pids:
                addr = self.peers[pid].address
                print("    id: {:>2}, address: {}".format(pid, addr))
        finally:
            self.lock.release()

    def peer(self, pid):
        """Return the object with the given id."""

        self.lock.acquire()
        try:
            return self.peers[pid]
        finally:
            self.lock.release()

    def get_peers(self):
        """Return all registered objects."""

        self.lock.acquire()
        try:
            return self.peers
        finally:
            self.lock.release()
