#!/usr/bin/env python2
# Copyright (c) 2014-2015 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Test addressindex generation and fetching
#

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import *

class AddressHistoryTest(BitcoinTestFramework):

  def setup_chain(self):
    print("Initializing test directory "+self.options.tmpdir)
    initialize_chain_clean(self.options.tmpdir, 4)

  def setup_network(self):
    self.nodes = []
    self.nodes.append(start_node(0, self.options.tmpdir, ["-debug"]))
    self.nodes.append(start_node(1, self.options.tmpdir, ["-debug", "-addressindex"]))
    self.nodes.append(start_node(2, self.options.tmpdir, ["-debug"]))
    self.nodes.append(start_node(3, self.options.tmpdir, ["-debug", "-addressindex"]))
    connect_nodes(self.nodes[0], 1)
    connect_nodes(self.nodes[0], 2)
    connect_nodes(self.nodes[0], 3)

    self.is_network_split = False
    self.sync_all()

  def run_test(self):
    print "Mining blocks..."
    self.nodes[0].generate(105)
    self.sync_all()

    chain_height = self.nodes[1].getblockcount()
    assert_equal(chain_height, 105)
    assert_equal(self.nodes[1].getbalance(), 0)
    assert_equal(self.nodes[2].getbalance(), 0)

    # block 106
    txid1 = self.nodes[0].sendtoaddress("mo9ncXisMeAoXwqcV5EWuyncbmCcQN4rVs", 10)
    self.nodes[0].generate(1)
    self.sync_all()

    # block 107
    txid2 = self.nodes[0].sendtoaddress("mo9ncXisMeAoXwqcV5EWuyncbmCcQN4rVs", 15)
    self.nodes[0].generate(1)
    self.sync_all()

    # block 108
    txid3 = self.nodes[0].sendtoaddress("mo9ncXisMeAoXwqcV5EWuyncbmCcQN4rVs", 20)
    self.nodes[0].generate(1)
    self.sync_all()

    txids = self.nodes[1].getaddresstxids("mo9ncXisMeAoXwqcV5EWuyncbmCcQN4rVs")
    assert_equal(len(txids), 3)

    # mempool
    txid4 = self.nodes[0].sendtoaddress("mo9ncXisMeAoXwqcV5EWuyncbmCcQN4rVs", 25)
    self.sync_all()

    mempool = self.nodes[1].getaddressmempool({"addresses": ["mo9ncXisMeAoXwqcV5EWuyncbmCcQN4rVs"]})

    # cptx
    cptx1 = {
      "txid": "c16ca51582cb3a2c5f3d8bf7cae864feb396960c81484f35f89aa8509aaabd0e",
      "block_index" : 109
    }
    cptx2 = {
      "txid": "6ce87b074c2578fe40eb61eaceae1b7e9546d20ae9b805399f4689aeb822392a",
      "block_index" : 0
    }

    # address
    address = "mo9ncXisMeAoXwqcV5EWuyncbmCcQN4rVs"

    # paging
    page = 1
    per_page = 20

    history = self.nodes[1].getaddresshistory({"address": address, "cp_txs":[], "page":page, "per_page": per_page})

    print history
    #assert_equal(history["tx_count"], 6)
    #assert_equal(len(history["txids"]), 6)
    #assert_equal(history["txids"][0], cptx2["txid"])
    #assert_equal(history["txids"][1], txid4)
    #assert_equal(history["txids"][2], cptx1["txid"])
    #assert_equal(history["txids"][3], txid3)
    #assert_equal(history["txids"][4], txid2)
    #assert_equal(history["txids"][5], txid1)

    # paging
    #page = 1
    #per_page = 3

    #history = self.nodes[1].getaddresshistory({"address": address, "cp_txs":[], "page"    :page, "per_page": per_page})

    #print history
    #assert_equal(history["tx_count"], 6)
    #assert_equal(len(history["txids"]), 3)

if __name__=='__main__':
    AddressHistoryTest().main()