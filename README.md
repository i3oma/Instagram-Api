# Instagram-Api
The Node class represents a node in a linked list and has properties such as Value, url, and next.

The ApiInstagram class is responsible for managing interactions with the Instagram API. It initializes the Instagram client, reads login credentials from files, and sets up email information. It also maintains a list of hashtags and words for captions.

The Login method attempts to log in to the Instagram account using the provided credentials. If successful, it prints a login success message; otherwise, it handles any checkpoint challenge that may arise.

The class includes methods for downloading videos, posting reels (videos) with captions, and sending email notifications for new and old posts. The GetNewPost method retrieves the latest post from a specified Instagram user, downloads the video, sends email notifications, interacts with the post by liking and commenting on it, and creates a story.

Additionally, there are functions for downloading and uploading video stories.

The code instantiates an ApiInstagram object and calls the GetNewPost method to retrieve the latest post from the 'wadl6' Instagram account.

Finally, there is commented-out code related to using the schedule library to schedule the execution of the GetNewPost method at a specific time daily.

This code demonstrates a basic implementation of Instagram API integration and showcases functionalities such as downloading videos, posting reels, sending email notifications, and interacting with posts and stories.
