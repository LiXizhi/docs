# Quest Item
Quest is a complex rule item, which is defined by an xml file.

A quest rule contains:
* preconditions: such as how many items must be collected by the triggering entity before the quest is active. 
* goals: a list of goals to complete before the quest can be completed. 
* cost: a list of items to remove when rule is finished.  
* reward: a list of items to receive when rule is finished.
* startdialog: dialogs to show to the user, when pre-condition is met, but froms and goals are not met, 
* enddialog: dialogs to show to the user, when froms and goals are met, before rule is executed. 
* repeatable: if quest can be repeatly done.
