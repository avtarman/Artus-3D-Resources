import logging

class ArtusLogger:
    def __init__(self):
        pass

    '''
    message list

    _wifi_
    connection made (i)
    connection lost (e)

    _spi_
    command error (e)
    stm #s

    _general operation_
    cmd sent (i)
    ack received (i)
    grasp saved (i)
    '''

    def configLogFile(self,filename,filedir):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s:%(message)s',datefmt='%m/%d/%Y %I:%M:%S %p',
            filename=filedir+filename,
            filemode='a'
        )
 
    def logSTMerror(self,debugmessage:str):
        i=2
        listdebug = debugmessage.split(' ') # split string with spaces
        while i < len(listdebug):
            
            # set main error type
            if listdebug[1] == 'T':
                newdebug = 'Target SPI Error:'
            elif listdebug[1] == 'C':
                newdebug = 'Calibrate Error:'
            elif listdebug[1] == 'SH':
                newdebug = 'Shut Down SPI Error:'
            elif listdebug[1] == 'ST':
                newdebug = 'Start SPI Error:'
            sublist = [*listdebug[i]]

            # add stm # to string log
            if sublist[1].isnumeric():
                newdebug+='STM'+''.join(sublist[:2])
            else: 
                newdebug+='STM'+sublist[0]

            # log error
            logging.error(newdebug)
    
    def rmbrackets(self,message:str):
        message = message.replace('[','').replace(']','')
        return message

    def logFeedbackMessage(self,message:str):
        feedbackobj = ['feedback joint positions (degrees): ','current draw of actuators (mA): ','temperatures of actuators (*C): ']
        
        # check for ACK
        substring = message[message.index(':')]
        if substring == '1':
            logging.info('ACK received from masterboard')
            return

        start_index = 0
        for i in range(3):
            substring = message[message.index('[',start_index):message.index(']',start_index)]
            message = feedbackobj[i] + substring
            logging.info(message)
            start_index = message.index(']') # new start index

            # warning for current 
            if i == 1:
                substring = self.rmbrackets(substring)
                substring = substring.split(',')
                for i in range(16):
                    if int(substring[i]) > 1000: # 1A
                        logging.warning('actuator #'+str(i)+' HIGH current draw - '+substring[i])
            # warning for temperature
            if i == 2:
                substring = self.rmbrackets(substring)
                substring = substring.split(',')
                for i in range(16):
                    if int(substring[i]) > 60: # 1A
                        logging.warning('actuator #'+str(i)+' HIGH temperature - '+substring[i])

        return