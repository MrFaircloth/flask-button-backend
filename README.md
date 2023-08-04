# flask-button-backend

## Purpose

The Button was designed to function similar to a timer.
The goal of the button is to remain 'alive' until it reaches its completion date.
The timer length is determined by the provided interval and it will be broken up into chunks.
These chunks give a rough estimate of how far along the button is.
Once it reaches 0, the button's 'alive' status will be set to false and will become inoperable.
The status of the button will only be known once checked.
Upon checking, it report its alive status and it's current interval chunk along with any other relevant data.

## How to play

The rules to the game are quite simple. Keep the button alive for the allotted time. In this case, it's set to one month.
The button can be saved simply by posting `!save` in our groupme chat. The clock will be reset, and your score will be determined by how low the button was. The lower the score, the better.

Your score will ALWAYS be overridden. For example: If your past save was in the green zone and you send `!save` when it's blue, your score is now in the blue zone.
The button status will only be obtained by checking. Status alerts will not be sent to the chat. Additionally, you will not know what the other players have saved the button at (unless they tell you).

Lastly and most importantly, if the button dies, everyone loses.