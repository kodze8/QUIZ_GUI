import requests

map_category = {"books": 10, "films": 11, "music": 12, "computers": 18, "art": 25, "mythology": 20}


class Questions:

    def __init__(self, category):
        parameters = {"amount": 20,
                      "category": map_category[category],
                      "type": "multiple"}
        q = requests.get("https://opentdb.com/api.php", params=parameters).json()["results"]
        self.ques = {}
        for i in q:
            q = i["question"]
            temp = i["incorrect_answers"]
            temp.insert(0, i["correct_answer"])
            self.ques[q] = temp
