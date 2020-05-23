import requests, os, json, random, datetime, sys
from colored import fg, attr

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Privacy():

    def __init__(self):

        """"""
        self.s = requests.session()
        self.resetUi()
        self.sessionId = '58104988-f95f-424e-b870-03378f1f629f'
        self.email = input('Login email: ')
        if '@' not in self.email or '.' not in self.email:
            print('{}Invalid email. Try again.{}'.format(fg(1),attr(0)))
            sys.exit()
        else:
            pass
        self.password = input('Password: ')


        self.token = self.getToken(self.email,self.password)

        cookies = {
            'sessionID': self.sessionId,
            'token': self.token,
        }

        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Dest': 'empty',
            'Authorization': 'Bearer '+self.token,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Accept-Language': 'en-US,en;q=0.9',
            'If-None-Match': 'W/"4bd14-7eHJQJkUeI7N8F2qdgv9Uw"',
        }

        self.cookies = cookies
        self.headers = headers

        print(self.printTime(),'Retrieving current card list..')

        self.cardList = self.getCards()['cardList']

        self.choice = self.options()


    def printTime(self):
        current_time = datetime.datetime.now()
        return '[{}]:'.format(str(current_time)[11:])


    def resetUi(self):
        cls()
        print(('%s'+('='*77)+'%s') % (fg(85),attr(0)))
        print(('%s'+('='*77)+'%s') % (fg(85),attr(0)))
        print(('%s'+('='*77)+'%s') % (fg(85),attr(0)))
        print('%s========================= Privacy Card Gen%s %sby chx#0001%s %s======================%s' % (fg(85),attr(0),fg(83),attr(0),fg(85),attr(0)))
        print(('%s'+('='*77)+'%s') % (fg(85),attr(0)))
        print(('%s'+('='*77)+'%s') % (fg(85),attr(0)))
        print(('%s'+('='*77)+'%s') % (fg(85),attr(0)))


    def getToken(self,email,password):

        cookies = {
            'sessionID': self.sessionId,
            #'experiments': 'CiQ3OTcxZDA2YS03ZjIxLTRlMGMtYmRhZS1lZjE3ODFkNjBhNWUSigE6D3Nob3VsZEhpZGVQbGFuc0ITc2hvdWxkSGlkZVNoYXJlQ2FyZEoZc2hvdWxkU2hvd0FjY291bnRTZXR0aW5nc1oSaGlkZVNpbmdsZUNhcmRDb3B5ahZzaG93T2xkU3BlbmRMaW1pdE1vZGFscglsYW5kaW5nVjKSAQ9oaWRlQ3VzdG9tU3R5bGU%3D',
        }

        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Dest': 'empty',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        data = '{"email":"'+email+'","password":"'+password+'","extensionInstalled":false,"captchaResponse":null}'

        response = self.s.post('https://privacy.com/auth/local', headers=headers, data=data, cookies=cookies)

        if response.status_code != 200:

            print(self.printTime(),'{}Login error | {} {}'.format(fg(1),response.json()["message"],attr(0)))

            sys.exit()

        responseJSON = response.json()
         
        if 'one-time' in responseJSON['message']:

            userToken = responseJSON['userToken']

            headers = {
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'Content-Type': 'application/json;charset=UTF-8',
                'Origin': 'https://privacy.com',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://privacy.com/tfa',
                'Accept-Language': 'en-US,en;q=0.9',
            }

            tfa_code = str(input('2FA Code: '))

            data = '{"code":"'+tfa_code+'","userToken":"'+userToken+'","rememberDevice":false}'

            response = self.s.post('https://privacy.com/auth/local/code', headers=headers, cookies=cookies, data=data)

            responseJSON = response.json()


        return responseJSON['token']


    def options(self):

        choice = input("""
        1. Get all cards (This will get ALL the cards.)
        2. Get unused cards only
        3. Generate cards
        4. Delete all active cards
        5. Delete all used cards
        6. Delete all unused cards
        7. Pause all cards
        8. Resume all cards

        > """)

        if choice == '1':
            self.getAllCards()

        elif choice == '2':
            self.getFreshCards()

        elif choice == '3':
            self.genCards()

        elif choice == '4':
            self.deleteAllOpen()

        elif choice == '5':
            self.deleteAllUsed()

        elif choice == '6':
            self.deleteAllUnused()

        elif choice == '7':
            self.pauseAll()

        elif choice == '8':
            self.resumeAll()

        else:
            print(self.printTime(),'Invalid selection.')


    def getCards(self):

        response = self.s.get('https://privacy.com/api/v1/card/', headers=self.headers, cookies=self.cookies)

        cardList = response.json()

        with open('priv_cards.json','w') as file:

            json.dump(cardList,file,indent=4)
            file.close()

        return cardList


    def getAllCards(self):

        all_cards = []

        with open('all cards.txt','w') as file:

            file.write('CardName\tCardNumber\tExpMon\tExpYear\tCVV\tSpendLimit\tStore\tUnused\tCardState\tSpentThisYear')

            for card in self.cardList:

                if len(card['hostname']) == 0:
                    hostname = 'UNLOCKED'
                card_out = card['memo']+'\t'+card['PAN']+'\t'+card['expMonth']+'\t'+card['expYear']+'\t'+card['CVV']+'\t'+str(card['spendLimit'])+'\t'+hostname+'\t'+str(card['unused']).upper()+'\t'+card['state']+'\t'+card['spentThisYear']
                print(self.printTime(),card_out)
                all_cards.append(card_out)
                file.write(card_out+'\n')

            file.close()

        print(self.printTime(),'Got {0} total cards since account created.'.format(len(all_cards)))


    def pauseAll(self):

        paused_cards = []

        for card in self.cardList:

            response = self.s.post('https://privacy.com/api/v1/card/'+card['cardID']+'/pause', headers=self.headers, cookies=self.cookies)
            if response.status_code == 200:
                print(self.printTime(),'Card {0} paused.'.format(card['cardID'][:-4]))
            else:
                print(self.printTime(),'Error pausing card ({0})'.format(response.json()["message"]))

        print(self.printTime(),'Paused {0} cards.'.format(len(paused_cards)))


    def resumeAll(self):

        for card in self.cardList:

            response = self.s.post('https://privacy.com/api/v1/card/'+card['cardID']+'/resume', headers=self.headers, cookies=self.cookies)
            if response.status_code == 200:
                print(self.printTime(),'Card {0} resumed.'.format(card['cardID'][:-4]))
            else:
                print(self.printTime(),'Error resuming card ({0})'.format(response.json()["message"]))
            print(self.printTime(),'Done.')


    def deleteAllOpen(self):

        del_cards = []

        for card in self.cardList:

            if card['state'] == 'OPEN':

                response = self.s.post('https://privacy.com/api/v1/card/'+card['cardID']+'/delete', headers=self.headers, cookies=self.cookies)
                if response.status_code == 200:
                    print(self.printTime(),'Card {0} deleted.'.format(card['lastFour']))
                    del_cards.append(card['lastFour'])
                else:
                    print(self.printTime(),'Error deleting card ({0})'.format(response.json()["message"]))


        print(self.printTime(),'Done. Deleted {0} cards.'.format(len(del_cards)))


    def deleteAllUsed(self):

        del_cards = []

        for card in self.cardList:

            if card['unused'] == False:

                response = self.s.post('https://privacy.com/api/v1/card/'+card['cardID']+'/delete', headers=self.headers, cookies=self.cookies)
                if response.status_code == 200:
                    print(self.printTime(),'Used card {0} deleted. Unused - {1}'.format(card['lastFour'],card['unused']))
                    del_cards.append(card['unused'])
                else:
                    print(self.printTime(),'Error deleting card ({0})'.format(response.json()["message"]))


        print(self.printTime(),'Deleted {0} used cards.'.format(len(del_cards)))


    def deleteAllUnused(self):

        print(self.printTime(),'Deleting All Unused cards. This might take a few minutes..')

        del_cards = []

        for card in self.cardList:

            if card['unused'] == True:

                response = self.s.post('https://privacy.com/api/v1/card/'+card['cardID']+'/delete', headers=self.headers, cookies=self.cookies)
                if response.status_code == 200:
                    print(self.printTime(),'Fresh card {0} deleted. Unused - {1}'.format(card['lastFour'],card['unused']))
                    del_cards.append(card['unused'])
                else:
                    print(self.printTime(),'Error deleting card.',response.text)

                time.sleep(1)


        print(self.printTime(),'Deleted {0} fresh cards.'.format(len(del_cards)))


    def genCards(self):

        #FOREVER, MONTHLY, TRANSACTION
        maxcards = input('Amount of cards to generate: ')
        maxcards = int(maxcards)
        spend_limit = input('Spend limit: ')
        spend_limit = int(spend_limit)
        limit_duration = input('Limit duration. (Will set same for all.)\n\n1.Per charge\n2.Monthly\n3.Total')

        if limit_duration == '1':
            limit_duration = 'TRANSACTION'
        elif limit_duration == '2':
            limit_duration = 'MONTHLY'
        else:
            limit_duration = 'FOREVER'

        card_str = random.choice('QWERTYUIOPASDFGHJKLZXCVBNM')+random.choice('QWERTYUIOPASDFGHJKLZXCVBNM')+random.choice('QWERTYUIOPASDFGHJKLZXCVBNM')
        new_cards = []

        for i in range(maxcards):
            memo = (random.choice('QWERTYUIOPASDFGHJKLZXCVBNM') * 3) + (str([i]))
            payload = {
                "reloadable":True,
                "spendLimitDuration":limit_duration,
                "memo":memo,
                "meta":{"hostname":""},
                "style":"",
                "spendLimit":spend_limit
            }
            response = self.s.post('https://privacy.com/api/v1/card/', headers=self.headers, cookies=self.cookies, json=payload)
            if response.status_code == 200:
                print(self.printTime(),'Card {0} created successfully! ({1})'.format(memo,response.json()['card']['lastFour']))
                new_cards.append(
                                {
                                'cc_num':response.json()['card']['PAN'],
                                'exp_mon':response.json()['card']['expMonth'],
                                'exp_year':response.json()['card']['expYear'],
                                'cvv':response.json()['card']['CVV']
                    }
                )
            else:
                print(self.printTime(),'Error creating card ({0})'.format(response.json()["message"]))

        with open('new cards.txt','w') as file:
            for card in new_cards:
                file.write(card['cc_num']+'\t'+card['exp_mon']+'\t'+card['exp_year']+'\t'+card['cvv']+'\n')
            file.close()

        print(self.printTime(),'Done. Generated {0} cards!'.format(len(new_cards)))


    def getFreshCards(self):

        fresh_cards = [card for card in self.cardList if card['state'] == 'OPEN' and card['unused'] == True]

        with open('fresh cards.txt','w') as file:
            for card in fresh_cards:
                file.write(card['PAN']+'\t'+card['expMonth']+'\t'+card['expYear']+'\t'+card['CVV']+'\n')
            file.close()

        print(self.printTime(),'Listed {0} cards to fresh cards.txt'.format(len(fresh_cards)))


Privacy()
