# UrgencyModelService

This is a web service created with django Framework to consume an emergency context model classification and a rasa nlu model

  * The sentiment model classification classify short texts into urgent and noturgent
  * The rasa nlu model classify short texts into many intents
  

### How do I get set up? ###

The following section describes how to run the service locally.

* virtualenv venv
* source venv/bin/activate
* pip install -r requirements.txt
* python manage.py runserver
* navigate to [localhost](http://127.0.0.1:8000/api/blocker/)


## Running the webservice
 
To run this project use this command:
```
python manage.py runserver
```

To test this web service input should be a json object and contains 2 key: "id" and "message" and the 2 values must be string 

