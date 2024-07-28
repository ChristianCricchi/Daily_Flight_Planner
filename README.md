# **Daily Flight Planner**

Daily Flight Planner is an application designed for the aviation industry, especially for operations/dispatchers, that allows the planning and assignment of daily flights at an airport to various dispatchers. There are two types of login with two different levels of privileges:

AdminOps Account:

- Home: Access to view daily flights and the privilege to edit and delete already dispatched flights and perform a search by name or flight number in the database.
- About: Access to a description of the app and a glossary of terms and abbreviations used in the app.
- Report: Ability to create and edit flight reports, similar to other users, as this is not an exclusive privilege of the AdminOps account because the Operations Manager will later review and archive the report definitively and store it for 90 days.
- Dispatch: Access to the names and IDs of dispatchers currently working at the airport, with the privilege to add, edit, and delete dispatch files.
- Register: Exclusive privilege to create login credentials for dispatchers.
- New Flight: Privilege to create and schedule daily flights.
This comprehensive access allows AdminOps to manage various aspects of flight operations efficiently.
- Log Out: Access to the Log Out page to sign out of their profile.

Dispatch Account:

- Home: Access to the home page where the dispatcher can view their daily flights and perform a search by name or flight number in the database.
- About: Access to a description of the app and a glossary of terms and abbreviations used in the app.
- Report: Ability to create and edit flight reports, similar to other users, the Operations Manager will later review and archive the report definitively and store it for 90 days.
- Log Out: Access to the Log Out page to sign out of their profile.

[Daily Flight Planner](https://daily-flight-planner-3bcd72540a25.herokuapp.com/)

![Daily Flight Planner is responsive](assets/img/AmIResponsive.png)

## Site owner Goals

- TThe purpose of this app is to provide a solution for companies operating in the aviation sector, enhancing the creation and planning of daily flights. This app is primarily aimed at AdminOps and Dispatchers.
- To provide the user an app where Operatives/Dispatch team can planning in a better way their daily ground service.
- To provide the user with an app that is easy to navigate, fully responsive, that invokes a sense of no-stress through the use of appropriate colors and layout.
- To provide the user the instructions of the app.

## User Stories

### First time user

- As a first time user I want to understand the main purpose of the DFP app.
- As a first time user I want to be able to intuitively navigate the DFP app.
- As a first time user I want a fully responsive app.
- As a first time user I want a full instructions to navigate and know how to use the DFP app.

### Returning User

- As a returning user I want to easily navigate to the Daily Flight planner app.
- As a returning user I want to choose different level of privilege that the different type user have on Daily Flight Planner.
- As a returning user I want to do my work intuitively, quickly, and securely.

### Frequent User

- As a frequent user I want to be familiar with the application, as it is intuitive and secure, so that using the app does not create stress during working hours.

## Design

### Imagery

The imagery used on the Daily Flight Planner site is very important to the overall experience of the user. A relaxed Red Arrows background, white background of container, different grade of pink is consistently used. This invoke a sense of calm in the user.

### Colours

The image shows an application with a vibrant and contrasting color scheme. Here’s a detailed description of the colors used:

- Main Background: An image with a light blue sky and acrobatic planes.
- Navigation bar: Intense pink (#C2185B).
- Title: Pink background with white text.
- Buttons:
    RESET: Orange background (#FF5722) with white text.
    SEARCH: Pink background (#C2185B) with white text.
Lower panel: Dark purple (#8E24AA) with white text.

General text: Mainly white, with some exceptions in black for improved readability.
In summary, the color scheme is vibrant and well-contrasted, designed to attract attention and facilitate visual interaction.


### Fonts

The Oswald font is the main font used throughout the whole website. This font was imported via Google Fonts. I am using Sans Serif as a backup font, in case for any reason the main font is not being imported into the site correctly.

## Wireframes
Wireframes were produced using Balsamiq. 

<details>

 <summary>Desktop Wireframe</summary>

![Desktop Wireframe](static/images/desktop/About.png)

![Desktop Wireframe](static/images/desktop/Dispatcher.png)

![Desktop Wireframe](static/images/desktop/Home.png)

![Desktop Wireframe](static/images/desktop/LogIn.png)

![Desktop Wireframe](static/images/desktop/NewFlight.png)

![Desktop Wireframe](static/images/desktop/Register.png)

![Desktop Wireframe](static/images/desktop/Report.png)
 </details>

 <details>
    <summary>Mobile Wireframe</summary>

![Mobile Wireframe](static/images/mobile/AboutMobile.png)

![Desktop Wireframe](static/images/mobile/DispatcherMobile.png)

![Desktop Wireframe](static/images/mobile/HomeMobile.png)

![Desktop Wireframe](static/images/mobile/LoginMobile.png)

![Desktop Wireframe](static/images/mobile/NewFlightMobile.png)

![Desktop Wireframe](static/images/mobile/RegisterMobile.png)

![Desktop Wireframe](static/images/mobile/ReportMobile.png)

 </details>

 ## Features

| Home Page| Image | 
| :---: | :---: | 
| When the user enters the application, it can easily orient themselves because there is: 
Header: At the top of the page, there is the text "© 2024 Daily Flight Planner" on the left and a "Log In" link on the right.
Login Form: In the center of the page, there is a login form with the following elements:
Title: "Log In" in large, visible characters.
Username Field: Labeled with the word "Username".
Password Field: Labeled with an icon of a lock and the word "Password".
Login Button: A rectangular button with the text "LOG IN".| ![Nav bar image]() |
