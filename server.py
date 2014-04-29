import settings
import citizen

import praw

# Returns a dict of accessed submissions
def get_accessed_submissions():
    # Returns an empty dict until the DB works.
    return []

# Polls subreddit for new posts, matches against filters and processes
def process_new_posts():
    r = praw.Reddit(user_agent=settings.USER_AGENT)
    r.login(settings.USERNAME, settings.PASSWORD)
    
    submissions = r.get_subreddit(settings.TARGET_SUBREDDIT).get_new(limit=10)
    accessed_submissions = get_accessed_submissions()

    for submission in submissions:
        # Prevents repeated submission processing
        if submission.id in accessed_submissions:
            break

        # Convert submission.title into something we can query
        details = submission.title.lower().split()

        # Types of submission
        if 'c' in details[0]:
            if "remove" in details[1]:
                citizen.remove(details[2])
            elif "add" in details[1]:
                citizen.add(details[2])
    
        if 'l' in details[0]:
            if 'revoke' in details[1]:
                print "remove law", details[2]
            else:
                # They wish to create a new law!
                # Try to parse the string as the law title.
                print "create a new law:", submission.title[4:]

        # Prevent duplicates
        accessed_submissions.append(submission.id)

process_new_posts()
