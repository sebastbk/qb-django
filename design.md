# Design Document

This design document will cover views, models, and api calls for the quiz app.

## Description

Users can create questions with answers, question sets that compose of questions, from the lobby players can create and join rooms, re join an in progress quiz, or let match making setup a game for them.

Each room has a host who has control over the room and quiz settings. Allowing for the host to set the number of players, teams, and well as the quiz format and questions. Format rules can be adjusted and the questions can be chosen by category or question set.

## Contents

[Views](#views)

* [Landing Page](#landingPage)
* [Sign Up](#signUp)
* [Login](#login)
* [Create Question](#createQuestion)
* [Create Question Set](#createQuestionSet)
* [Lobby](#lobby)
  * [Rejoin Quiz](#rejoinGame)
  * [Quick Play](#quickPlay)
  * [Join Room](#joinRoom)
  * [Create Room](#createRoom)
* [Waiting Room](#waitingRoom)

[Models](#models)

* [Question](#questionModel)
* [Question Set](#questionSetModel)
* [Room](#roomModel)
* [Quiz](#quizModel)
  * [Questions](#quizQuestionRelatedModel)
  * [Teams](#quizTeamRelatedModel)
  * [Players](#quizPlayerRelatedModel)

[APIs](#apis)

* []()

[Contributors](#contributors)

## Views<a name="views"></a>

### Landing Page<a name="landingPage"></a>

The landing page will prodive updates notifications as well as a ling to create a new account if the user is not already logged in.

### Sign Up<a name="signUp"></a>

> Users are required to make an account to participate

* form
  * **username**
  * **email**
  * **password**
  * **confirm password**

### Login<a name="login"></a>

* form
  * **username**
  * **password**

### Create Question<a name="createQuestion"></a>

All questions are text strings (the aim is to have other formats in the future) and have one or more correct answers, incorrect answers can also be provided to support specific formats such as multiple-choice. Tags can be added to the question to help other users find the types of questions they are looking for.

Questions may be marked as private for use only by the creator.

> Note: Editing a question creates a new version of a question. Only the latest version of a question will show up when searching for questions.

* form
  * **private** [false] - whether the question is private
  * **category** [required] - question category
  * **difficulty** [1] - question difficulty
  * **tags** [parsable string [tag1,tag2,...], a-zA-Z0-9_] - keywords for lookup
  * **text** [required] - text that represents the question
  * **answers** [must have at least 1 required answer] - inline formset
    * **text** [required] - text that represents the answer
    * **correct** [true] - true if correct else false (must be at least 1 correct)

### Create Question Set<a name="createQuestionSet"></a>

Users may create question sets using any number of public questions along with any of their private questions. The question sets will then be used as the pool of questions for a quiz.

Like questions, question sets can also be made private.

> Note: Similar to questions, when editing the question pool, you will create a new version of the question set. Additionally only the latset version may be edited.

* form
  * **private** [false] - whether the question set is private
  * **name** [required] - the name of the quiz
  * **description** [required] - a short description of the types of questions in the set
  * **tags** [parsable string [tag1,tag2,...], a-zA-Z0-9_] - keywords for lookup
  * **questions** - list of questions
    * search - search for questions
      * **private** - only show private questions
      * **category** - the category of questions
      * **format** - questions that can support a given format
      * **keywords** - keywords

### Lobby<a name="lobby"></a>

The lobby is where players will go to find game rooms. From here you can rejoin a quiz, quick start, join a room, or create a room.

#### Rejoin Quiz<a name="rejoinQuiz"></a>

Rejoin any in-progress game that you are participating in. Usefull if your browser/computer dies or you cannot navigate back to the game page.

#### Quick Play<a name="quickPlay"></a>

Quick Play will allow players to automatically form a game.  After the game is finished players will be returned to the lobby.

> Note: There is no game host or room and the game will begin as soon as enough players are gathered. Additionally only a single category will be used for questions.

* form
  * **format** - the game format you want to play
  * **categories** - specify the categories of questions you want to play with. Selecting multiple categories will make game creation time faster.

#### Join Room<a name="joinRoom"></a>

A list of available rooms that a user can join will be dispalyed.

> Note: Rooms that have a game in progress cannot be joined.

* search rooms
  * form
    * **search** - the quiz name to search for
  * displays a list of rooms
    * **sort by**
      * created on
      * categories
      * format
      * players
  * join private room
    * form
      * **password** [required] - password for the room

#### Create Room<a name="createRoom"></a>

Create a new room as the host.

* form
  * **name** - the name of the game room
  * **private** - creates a private room
    * **password** - if the game is private a password is required

### Waiting Room<a name="waitingRoom"></a>

The waiting room is where players will assemble before the game begins. Here the host can change the settings for the room such as number of players or teams.

This host will also need to set up the game rules such as format, whether to use a question set or to randomly select questions based on categories.

> Depending on the format additional option must be set, such as, the number of questions or a specific score to reach.

* set player teams
* start game
* room form
  * **name** - the name of the game room
  * **private** - creates a private room
    * **password** - if the game is private set a password
  * **teams** - the number of teams
  * **players** - the number of players (players >= teams)
* rules form
  * **format** - the format for the quiz
  * **questions** - how to select questions
    * **question sets** - use a pre-made question set
    * **categories** - auto generate a question set
      * **difficulty** - the average difficulty of the randomly selected questions.

## Models<a name="models"></a>

The Models section covers the db models using django fields.

### Tag<a name="tagModel"></a>

* id [UUIDField] [primary key]
* text [CharField] [unique] [a-zA-Z0-9_]

### Answer<a name="answerModel"></a>

* id [UUIDField] [primary key]
* text [CharField] [max length 30]
* is_correct [BooleanField]
* question [ForeignKeyField] [Question]

### Question<a name="questionModel"></a>

* id [UUIDField] [primary key]
* created_on [DateTimeField]
* created_by [ForeignKeyField] [User]
* root_id [UUIDField]
* private [BooleanField]
* category [CharField] [choices]
* difficulty [PositiveSmallIntegerField]
* text [TextField]

### Question Set<a name="questionSetModel"></a>

* id [UUIDField] [primaryKey]
* created_on [DateTimeField]
* created_by [ForeignKeyField] [User]
* title [CharField] [max length 60]
* description [TextField]

### Room<a name="roomModel"></a>

* id [UUIDField] [primary]
* created_on [DateTimeField]
* host [ForeignKeyField] [User]
* title [CharField] [max length 60]
* max_slots [PositiveSmallIntegerField] [min 1] [max 16]

### Quiz<a name="quizModel"></a>

* id [UUIDField] [primary]
* active [BooleanField]
* format [CharField] [choices]
* question_set [ForeignKey] [QuestionSet]
* categories [CharField] [choices] [multiple]

#### Questions<a name="quizQuestionRelatedModel"></a>

* id [UUIDField] [primary]
* quiz [ForeignKeyField] [Quiz]
* question [ForeignKeyField] [Question]
* order [PositiveSmallIntegerField]

#### Teams<a name="quizTeamRelatedModel"></a>

* id [UUIDField] [primary]
* quiz [ForeignKey] [Quiz]
* name [CharField]
* score [IntegerField]

#### Players<a name="quizPlayerRelatedModel"></a>

* id [UUIDField] [primary]
* quiz [ForeignKey] [Quiz]
* team [ForeignKey] [Team]
* user [ForeignKey] [User]
* score [IntegerField]

## APIs<a name="apis"></a>

## Contributors<a name="contributors"></a>

Keifer Sebastian - <sebastbk@hotmail.com>
