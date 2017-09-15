# Design Document

This design document will cover views, models, and api calls for the quiz bowl web application.

## Description

The original design has been scoped down to a single quiz format, the quiz bowl. This is a popular format in schools and universities.

In the quiz bowl format a reader will read out the question until a contestant thinks they know the answer. Contestants must buzz in before the other contestants to answer the question, at which point the reader will stop reading the question. If the contestant gets the answer correct they will get a point; if the contestant gets the question incorrect then the other contestants have an opportunity to answer the question.

Users may be given permission to create their own questions and a form (separate from the admin page) will be included to support this. Question moderation is left to the admins.

Users have the option to join matchmaking via a quick join method which will automatically create a game among several players or joining/creating a game room. Each room has a host who has control over the room and quiz settings. The host can set the number of players, teams, and question categories. They also have control over starting the quiz.

## Contents

[Views](#views)

* [Landing Page](#landingPage)
* [Sign Up](#signUp)
* [Login](#login)
* [Create Question](#createQuestion)
* [Lobby](#lobby)
  * [Rejoin Quiz](#rejoinGame)
  * [Quick Play](#quickPlay)
  * [Join Room](#joinRoom)
  * [Create Room](#createRoom)
* [Waiting Room](#waitingRoom)

[Models](#models)

* [Difficulty](#difficultyModel)
* [Category](#categoryModel)
* [Question](#questionModel)
* [Answer](#answerModel)
* [Room](#roomModel)
* [Quiz](#quizModel)
  * [Questions](#quizQuestionRelatedModel)
  * [Teams](#quizTeamRelatedModel)
  * [Players](#quizPlayerRelatedModel)

[APIs](#apis)

Coming soon!

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

All questions are text strings (the aim is to have other formats in the future) and have one or more correct answers. Tags can be added to the question to help other users find the types of questions they are looking for.

Questions may be marked as private, for use only by the creator.

> Note: Editing a question creates a new version of a question. Only the latest version of a question will show up when searching for questions.

* form
  * **difficulty** [required] - question difficulty
  * **category** [required] - question category
  * **text** [required] - text that represents the question
  * **answers** [required] - a form set for answers. See [Answer Model](#answerModel).

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

### Difficulty<a name="difficultyModel"></a>

Instead of hard coding difficulties, a model is used to allow admins to determine the tiers of difficulties.

* name [CharField]
* rank [PositiveIntegerField]

### Category<a name="categoryModel"></a>

The categories a question can belong to. Is used to select questions for a quiz.

* name [CharField] [max_length=30] [unique]

### Question<a name="questionModel"></a>

Contains meta data about a question, as well as, the question itself.

* created_on [DateTimeField]
* created_by [ForeignKey] [User]
* category [ForeignKey] [Category]
* difficulty [ForeignKey] [Difficulty]
* text [TextField] - possibly use a markdown to allow for some styling

### Answer<a name="answerModel"></a>

A single answer to a question. If there are multiple way to refer to the answer, they can be specified in a list separated by a comma.

Example a carbonated beverage might be referred to as:

    Coke, Pop, Soda

* question [ForeignKey] [Question]
* wordings [CharField] - comma separated list of wordings for an answer
* matching [CharField] [choices] [Fuzzy] [Strict] - matching method

Strict and Fuzzy matching both normalize the strings for comparison, however, fuzzy matching will check how similar the two strings are and accept strings that are close. This is implemented to help with spelling errors. In the future it might make sense to simply have a word autocomplete to help users avoid mistakes.

> Note: String normalization strips all punctuation, whitespace, and accents. It also converts all strings to lowercase.

### Room<a name="roomModel"></a>

* created_on [DateTimeField]
* host [ForeignKey] [User]
* title [CharField] [max length 60]
* max_slots [PositiveSmallIntegerField] [min 1] [max 9]

### Quiz<a name="quizModel"></a>

* active [BooleanField]
* format [CharField] [choices]
* question_set [ForeignKey] [QuestionSet]
* categories [CharField] [choices] [multiple]

#### Questions<a name="quizQuestionRelatedModel"></a>

* quiz [ForeignKey] [Quiz]
* question [ForeignKey] [Question]
* order [PositiveSmallIntegerField]

#### Teams<a name="quizTeamRelatedModel"></a>

* quiz [ForeignKey] [Quiz]
* name [CharField]
* score [IntegerField]

#### Players<a name="quizPlayerRelatedModel"></a>

* quiz [ForeignKey] [Quiz]
* team [ForeignKey] [Team]
* user [ForeignKey] [User]
* score [IntegerField]

## APIs<a name="apis"></a>

Coming Soon!

## Contributors<a name="contributors"></a>

Keifer Sebastian - <sebastbk@hotmail.com>
