# MyPassBook
Password Management with DB


The motive behind creating a Password managing app/UI is to have my own app that can store or save my different credentials for different website securely and I do not need to remember them all the time. I can access and keep tracking all of them with one security key/password.

Challenges: To create this interface/app, there are some challenges that I need to implement such as how a password manager vault works or what is hashing and how it works for password so It can get hashed in hash values. After reading some articles over encryption vs hashing, I got to conclusion that hashing is better in way to work with very sensitive info like passwords because Encryption is a two-way function; what is encrypted can be decrypted with the proper key. Hashing, however, is a one-way function that scrambles plain text to produce a unique message digest. ... An attacker who steals a file of hashed passwords must then guess the password.

My tasks:
• To create a SQL database.
  ➢ Store passwords and details of website or app to that database.
  ➢ And retrieve those passwords and details from SQL database.
• Create basic interface (for the moment I will stick with terminal interface, but I will try to implement it with GUI such as tkinter)
  ➢ First time user can create that master password with username that will be key to database.
  ➢ User will be asked every time to enter master password to access the database of password vault.
  ➢ Then it will show menu options such as save new credential, show all sites/app and their login id- passwords.
  ➢ For 1. Option it will ask for basic info like name/URL of website/app, email/login id and password.
  ➢ Optional: add saved password to clipboard to paste it easily anywhere, and search password by entering site/app name.
• One way hash Function to convert text password to hash value.
