import json
from Translate import Translator
from Study import StudyTool

translator = Translator('en','ja')
studyTool = StudyTool()

with open('KanjiGroups.json') as json_file:
    data = json.load(json_file)
    grades = data['grades']
    for i in range(len(grades)):
        grade = grades[i]
        gradeArr = list(grade['grade' + str(i + 1)])
        studyTool.add_module('grade' + str(i + 1))
        for term in gradeArr:
            definition = translator.translate(term)
            studyTool.add_term('grade' + str(i + 1), [definition['input'],definition['translatedText'].lower()])
            print(definition['input'] + ':' + definition['translatedText'].lower())
