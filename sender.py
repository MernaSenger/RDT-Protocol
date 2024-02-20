from network import NetworkLayer
class SenderProcess:
    """ Represent the sender process in the application layer  """

    __buffer = list()

    @staticmethod
    def set_outgoing_data(buffer):#el message
        """ To set the message the process would send out over the network
        :param buffer:  a python list of characters represent the outgoing message
        :return: no return value
        """
        SenderProcess.__buffer = buffer
        return

    @staticmethod
    def get_outgoing_data():
        """ To get the message the process would send out over the network
        :return:  a python list of characters represent the outgoing message
        """
        return SenderProcess.__buffer


class RDTSender:
    """ Implement the Reliable Data Transfer Protocol V2.2 Sender Side """

    def __init__(self, net_srv):
        """ This is a class constructor
            It initialize the RDT sender sequence number  to '0' and the network layer services
            The network layer service provide the method udt_send(send_pkt)
        """
        self.sequence = '0'
        self.net_srv = net_srv #netwrok layer object

    @staticmethod
    def get_checksum(data):#data will be only 1 character
        """ Calculate the checksum for outgoing data
        :param data: one and only one character, for example data = 'A'
        :return: the ASCII code of the character, for example ASCII('A') = 65
        """
        #Get the ascii code for the character
        # TODO provide your own implementation
        checksum = ord(data)  # you need to change that #ord function
        return checksum

    @staticmethod
    def clone_packet(packet):#nothing to do
        """ Make a copy of the outgoing packet
        :param packet: a python dictionary represent a packet
        :return: return a packet as python dictionary
        """
        pkt_clone = {
            'sequence_number': packet['sequence_number'],
            'data': packet['data'],
            'checksum': packet['checksum']
        }
        return pkt_clone

    @staticmethod
    def is_corrupted(reply):
        """ Check if the received reply from receiver is corrupted or not
        :param reply: a python dictionary represent a reply sent by the receiver
        :return: True -> if the reply is corrupted | False ->  if the reply is NOT corrupted
        """
        #ack
        #if the checksum is not for the sequence no
        ack=reply.get('ack')
        check_sum=reply.get('checksum')
        if ord(str(ack))==check_sum:
            return False
        else:
            return True

        # TODO provide your own implementation #use check_sum
        pass

    @staticmethod
    def is_expected_seq(reply, exp_seq):
        """ Check if the received reply from receiver has the expected sequence number
        :param reply: a python dictionary represent a reply sent by the receiver
        :param exp_seq: the sender expected sequence number '0' or '1' represented as a character
        :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        #check if seq_no is as excepcted
        #return true/false
        # TODO provide your own implementation
        seq= reply.get('ack')
        if seq == exp_seq:
            return True
        else:
            return False

        pass

    @staticmethod
    def make_pkt(seq, data, checksum):#nothing to do
        """ Create an outgoing packet as a python dictionary
        :param seq: a character represent the sequence number of the packet, the one expected by the receiver '0' or '1'
        :param data: a single character the sender want to send to the receiver
        :param checksum: the checksum of the data the sender will send to the receiver
        :return: a python dictionary represent the packet to be sent
        """
        packet = {
            'sequence_number': seq,
            'data': data,
            'checksum': checksum
        }
        return packet

    def rdt_send(self, process_buffer):
        """ Implement the RDT v2.2 for the sender
        :param process_buffer:  a list storing the message the sender process wish to send to the receiver process
        :return: terminate without returning any value
        """
        #buffer has all the data we want to send
        #we use for loop to get one character at a time
        # for every character in the buffer
        for data in process_buffer:

            checksum = RDTSender.get_checksum(data)
            pkt = RDTSender.make_pkt(self.sequence, data, checksum)
            pkt_clone=RDTSender.clone_packet(pkt)

            print("Sender expecting sequnce_number:",self.sequence)
            print("Sender sending", pkt)
            reply = self.net_srv.udt_send(pkt)

            #correct reply
            if (RDTSender.is_corrupted(reply)==False) and RDTSender.is_expected_seq(reply,self.sequence)==True:
                print("Sender received", reply)
                if self.sequence=='1':
                    self.sequence='0'
                else:
                    self.sequence='1'
            else:
                while(RDTSender.is_corrupted(reply) or RDTSender.is_expected_seq(reply,self.sequence)==False):
                    if (RDTSender.is_corrupted(reply)):
                        print("network_layer:corruption occurred", reply)
                    pkt_clone2 = RDTSender.clone_packet(pkt_clone)
                    print("Sender received", reply)
                   # pkt_clone=pkt_clone2
                    print("Sender excpecting sequnce_number:", self.sequence)
                    # print("Sender sending:{'sequence_number':",self.sequence,",'data':",data,",'checksum':",checksum,"}")
                    print("Sender sending", pkt_clone2)
                    reply = self.net_srv.udt_send(pkt_clone2)
                print("Sender received", reply)
                if self.sequence=='1':
                    self.sequence='0'
                else:
                    self.sequence='1'




             #implement the rest of the code upon the reply you get
            #check if ack is corrupted

        print(f'Sender Done!')
        return
