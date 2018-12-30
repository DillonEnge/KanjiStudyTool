import os, json

# Notes:
# Create logic chain for new additions, ie. Enter term >> Enter definition.
# Create listing of terms when given a module name

class PromptChain:
    def __init__(self):
        with open('promptChain.json') as json_file:
            data = json.load(json_file)
            self.chain = [ data['chain'], None ]

    def increment(self, key):
        keyExists = False
        if self.chain[0]['responses']:
            for responseObj in self.chain[0]['responses']:
                keyComp = responseObj['response']
                if key == keyComp:
                    keyExists = True
                    self.chain = [ responseObj, self.chain ]
                    break
            if not keyExists:
                print('Response not valid, try again.')
    def decrement(self):
        self.chain = self.chain[1]



class StudyTool:
    def __init__(self):
        self.promptChain = PromptChain()
        self.tempModuleName = ''
        if not os.path.isfile('book.json'):
            with open('book.json', 'w') as outfile:
                json.dump({'modules': []}, outfile, indent=4)
    def study(self, moduleName):
        skipNum = 0
        book = self.get_book()
        for i in range(len(book['modules'])):
            if book['modules'][i]['title'] == moduleName:
                for j in range(len(book['modules'][i]['terms'])):
                    for key, value in book['modules'][i]['terms'][j].items():
                        while True:
                            if skipNum > 0:
                                print('Skipping term: ' + key)
                                skipNum -= 1
                                break
                            answer = input(key + '?: ')
                            if '-h' in answer:
                                if len(answer.split(' ')) > 1:
                                    print(value[:int(answer.split(' ')[1])])
                                print(value[:1])
                            elif answer == '-a':
                                print('(' + value + ')')
                            elif answer == '-c':
                                self.modify_term(moduleName, key)
                                print('updating book...')
                                book = self.get_book()
                            elif '-s' in answer:
                                if len(answer.split(' ')) > 1:
                                    print('Skipping ' + answer.split(' ')[1] + ' terms...')
                                    print(int(answer.split(' ')[1]))
                                    skipNum = int(answer.split(' ')[1])
                                print('Skipping...')
                                break
                            elif answer == book['modules'][i]['terms'][j][key]:
                                print('Correct!')
                                break
                            else:
                                print('Incorrect!')

    def add_term(self, moduleName, term):
        book = self.get_book()
        for i in range(len(book['modules'])):
            if book['modules'][i]['title'] == moduleName:
                book['modules'][i]['terms'].append({term[0]: term[1]})
                break
        self.write_book(book)
    def add_module(self, moduleName):
        book = self.get_book()
        book['modules'].append({'title': moduleName, 'terms': []})
        self.write_book(book)
    def modify_term(self, moduleName, keyInput):
        book = self.get_book()
        for i in range(len(book['modules'])):
            if book['modules'][i]['title'] == moduleName:
                for j in range(len(book['modules'][i]['terms'])):
                    for key, value in book['modules'][i]['terms'][j].items():
                        if key == keyInput:
                            newTerm = input('What would you like to change ' + key + ' to? (definition)\n')
                            book['modules'][i]['terms'][j] = {newTerm.split(':')[0]:newTerm.split(':')[1]}
                            break
        self.write_book(book)
    def list_modules(self):
        book = self.get_book()
        print()
        for module in book['modules']:
            if module == book['modules'][len(book['modules']) - 1]:
                print(module['title'])
            else:
                print(module['title'] + ', ')
    def list_terms(self, moduleName):
        book = self.get_book()
        print()
        for i in range(len(book['modules'])):
            if book['modules'][i]['title'] == moduleName:
                for termObj in book['modules'][i]['terms']:
                    print(termObj)
            
    def remove_term(self, moduleName, termName):
        book = self.get_book()
        for i in range(len(book['modules'])):
            if book['modules'][i]['title'] == moduleName:
                for j in range(len(book['modules'][i]['terms'])):
                    for key, _ in book['modules'][i]['terms'][j].items():
                        if key == termName:
                            book['modules'][i]['terms'].pop(j)
        self.write_book(book)
    def remove_module(self, moduleName):
        book = self.get_book()
        for i in range(len(book['modules'])):
            if book['modules'][i]['title'] == moduleName:
                book['modules'].pop(i)
                break
        self.write_book(book)
    def get_book(self):
        with open('book.json') as json_file:
            book = json.load(json_file)
            return book
    def write_book(self, book):
        with open('book.json', 'w') as outfile:
            json.dump(book, outfile, indent=4)
    def process_key(self, key, response):
        if key == 'add_term':
            term = response.split(':')
            self.add_term(self.tempModuleName, term)
        elif key == 'add_module':
            self.add_module(response)
        elif key == 'lm':
            self.list_modules()
        elif key == 'add_to_module':
            self.tempModuleName = response
            self.promptChain.increment('module_name')
        elif key == 'modify_module':
            self.tempModuleName = response
            self.promptChain.increment('module_name')
        ##elif key == 'modify_term':
        ##    self.modify_term(self.tempModuleName, response)
        ##    self.promptChain.decrement()
        elif key == 'study':
            self.study(response)
        elif key == 'remove_term':
            self.remove_term(self.tempModuleName, response)
        elif key == 'remove_from_module':
            self.tempModuleName = response
            self.promptChain.increment('module_name')
        elif key == 'remove_module':
            self.remove_module(response)

    def start(self):
        while True:
            response = input(self.promptChain.chain[0]['prompt'])
            if response == 'q':
                self.promptChain.decrement()
                continue
            elif response.split(' --')[0] == 'lt':
                self.list_terms(response.split('--')[1])
            elif response == 'lm':
                self.list_modules()
            elif 'key' in self.promptChain.chain[0]:
                key = self.promptChain.chain[0]['key']
                self.process_key(key, response)
            else:
                self.promptChain.increment(response)

s = StudyTool()
s.start()