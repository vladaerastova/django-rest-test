Getting start
====================================

Install poetry and dependencies

 
  poetry install 
  poetry shell
  
  
Set up MAILGUN_API_KEY and CLEARBIT_API_KEY in blog.settings.py

https://www.mailgun.com - for email validation

https://clearbit.com/enrichment - for getting additional data for the user on signup


Running
====================================

  python manage.py runserver


Testing
====================================

  python manage.py test


