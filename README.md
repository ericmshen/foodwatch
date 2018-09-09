# FoodWatch #
![banner](https://i.imgur.com/s4gUu2p.png)

## Inspiration ##
FoodWatch is a platform that allows users to track and manage their groceries. Users can create, edit, and access their inventory, and receive SMS updates when expiry dates approach.

## Description ##
FoodWatch operates via SMS messages between the user and the platform. To add items to their inventory (the groceries they currently have), the user provides a description and expiry date. To view their inventory, the user may send a message to FoodWatch, and is returned with a full list of items and their expiry dates. In addition, the user may also view their list online. The user may also remove items upon consumption; a user guide can be found below.

At time points of one week, three days, and one day before an item’s expiry date, as well as the expiry date itself, the user will also receive messages informing them of the upcoming expiry. The usage of SMS as a means of communication means that an internet connection is not required for checking or updating lists, and the list can be accessed via users’ mobile devices.

## Compilation and Usage ##
Dependencies:
* Firebase Admin 2.13.0 or later
* Jinja2 2.10 or later
* Flask 1.0.2 or later
* Twilio 6.16.4 or later

We used the following technologies:
* User interaction via Programmable SMS on Twilio
* Database hosting on Firebase
* Frontend deployment on Flask microframework

User actions:
* Add item to inventory: “add (quantity) (commodity name) (expiry date)”
* Viewing inventory: “pantry”
* Remove item from inventory: “remove (quantity) (commodity name) (expiry date)”

## Next Steps ##
Our main goal for improving FoodWatch would be improving accessibility. Mainly, we want to add compatibility with Google Home and Alexa, so that user inventory can also be edited through voice commands (e.g. using the Google Assistant API for Google Home).

Currently, we also have a way for users to access their inventory online, where all their items are listed via the Flask microframework. Aside from the task of finding web hosting and a domain name, in the future, we would like to set up an authentication system to ensure users access their own lists. This feature would add an extra level of convenience to checking groceries and upcoming expiry dates. 

## Screenshots ##
![SMS message interface](https://i.imgur.com/IBs0WBF.png)
![Online access](https://i.imgur.com/Xi5U3hO.png)
