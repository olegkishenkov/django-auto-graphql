import json
from graphene_django.utils.testing import GraphQLTestCase


class ViewsTestCase(GraphQLTestCase):
    def test_query_one_question(self):
        response = self.query('''
query {
  oneQuestion(id: 1) {
    id
    questionText
  }
}
            ''')
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content, json.loads('''
            {
              "data": {
                "oneQuestion": {
                  "id": "1",
                  "questionText": "How are you?"
                }
              }
            }
            '''))

        response = self.query('''
query {
  oneQuestion(id: "1") {
    id
    questionText
  }
}
            ''')
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content, json.loads('''
            {
              "data": {
                "oneQuestion": {
                  "id": "1",
                  "questionText": "How are you?"
                }
              }
            }
            '''))

    def test_query_one_question_w_wrong_arg_type(self):
        response = self.query('''
query {
  oneQuestion(id: "hello") {
    id
    questionText
  }
}
            ''')
        self.assertResponseHasErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['errors'].pop()['message'], "Field 'id' expected a number but got 'hello'.")

    def test_query_one_choice_nested_along_many2one_and_many2many(self):
        response = self.query('''
query {
  allChoices {
    id
    choiceText
    question {
      id
      polls {
        id
      }
    }
  }
}
            ''')
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        choices = content['data']['allChoices']
        self.assertEqual(
            [[c['id'], c['question']['id'], [p['id'] for p in c['question']['polls']]] for c in choices],
            [
                ['1', '1', ['1', '2']],
                ['2', '1', ['1', '2']],
                ['3', '1', ['1', '2']],
                ['4', '2', ['1']],
                ['5', '2', ['1']],
            ]
        )

    def test_query_all_questions(self):
        response = self.query('''
query MyQuery {
  allQuestions {
    id
    polls {
      id
    }
    tags {
      id
    }
  }
}
        ''')
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content, json.loads('''
            {
              "data": {
                "allQuestions": [
                  {
                    "id": "1",
                    "polls": [
                      {
                        "id": "1"
                      },
                      {
                        "id": "2"
                      }
                    ],
                    "tags": [
                      {
                        "id": "1"
                      }
                    ]
                  },
                  {
                    "id": "2",
                    "polls": [
                      {
                        "id": "1"
                      }
                    ],
                    "tags": []
                  },
                  {
                    "id": "3",
                    "polls": [],
                    "tags": [
                      {
                        "id": "2"
                      }]
                  }
                ]
              }
            }
            '''))

    def test_query_all_questions_w_args(self):
        response = self.query('''
query MyQuery {
  allQuestions(id: [1, 2]) {
    id
  }
}
            ''')
        self.assertResponseHasErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['errors'].pop()['message'], "Unknown argument 'id' on field 'Query.allQuestions'.")

    def test_query_filter_questions_by_id(self):
        response = self.query('''
query MyQuery {
  filterQuestion(id: 1) {
    id
    pubDate
  }
}
            ''')
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content, json.loads('''
            {
                "data": {
                    "filterQuestion": [
                            {
                                "id": "1",
                                "pubDate": "1970-01-01T00:00:00+00:00"
                            }
                        ]
                    }
                }
            '''))


    def test_query_filter_choices_by_fk(self):
        response = self.query('''
query MyQuery {
  filterChoice(question: 1) {
    choiceText
    id
    question {
      id
    }
  }
}
        ''')
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual([e['id'] for e in content['data']['filterChoice']], ['1', '2', '3'])

    def test_query_filter_questions_by_m2m(self):
            response = self.query('''
query MyQuery {
  filterQuestion(polls: [1]) {
    id
  }
}
                ''')
            self.assertResponseNoErrors(response)
            content = json.loads(response.content)
            self.assertEqual([e['id'] for e in content['data']['filterQuestion']], ['1', '2'])

            response = self.query('''
query MyQuery {
  filterQuestion(polls: [1, 2]) {
    id
  }
}
                ''')
            self.assertResponseNoErrors(response)
            content = json.loads(response.content)
            # Django ORM's behavior is replicated where for each row of the result of the underlying
            # SQL join query there is a separate value
            self.assertEqual(set([e['id'] for e in content['data']['filterQuestion']]), set(['1', '1', '2']))

    def test_query_filter_questions_by_two_m2ms(self):
            response = self.query('''
query MyQuery {
  filterQuestion(polls: [1], tags: [1]) {
    id
  }
}
                ''')
            self.assertResponseNoErrors(response)
            content = json.loads(response.content)
            self.assertEqual(set([e['id'] for e in content['data']['filterQuestion']]), set(['1', '1']))

