'''
Cache the results to remove the need for future API calls. Code 
modified from https://realpython.com/caching-external-api-requests/
'''
import requests
import requests_cache
import re
import random
from time import sleep

requests_cache.install_cache(cache_name='wikipedia_internal_links_cache', backend='filesystem')

'''
Code for get_internal_links modified from code produced by ChatGPT. 
Sets user agent header per MediaWiki policy. Gets all internal links 
from a Wikipedia page. Continues to get links until all internal links
are retrieved.
'''
def get_internal_links(page_title):
    """ Get all internal links from a Wikipedia page
    
    Args:
        title (str): the title of the page to get links from. Use 
        underscores in place of any spaces.

    Returns:
        list[str]: a list of all internal links from the page
    """
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'titles': page_title,
        'prop': 'links',
        'format': 'json',
        'pllimit': 'max'  # Set pllimit to 'max' to retrieve as many links as possible in each batch
    }

    headers = {
        'User-Agent': 'Get Wikipedia Page Internal Links/1.0 (jerilbills@gmail.com)'
    }

    all_links = []

    # Make as many calls as needed to get all the links
    while True:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        ''' 
        'query': 'pages' contains data about the page as nested JSON 
        objects. For the Music of Tanzania Wikipedia article, the value
        of 'pages' is '245835', which itself is a key with values that
        are key-value pairs. The keys are 'pageid', 'ns', 'title', and 
        'links'. The value of links is a list of links, each with 'ns'
        and 'title' properties.
        Here is an example of what data returns for 'Music of 
        Tanzania':
        {'batchcomplete': '', 'query': {'normalized': 
        [{'from': 'Music_of_Tanzania', 'to': 'Music of Tanzania'}], 
        'pages': {'245835': {'pageid': 245835, 'ns': 0, 'title': 
        'Music of Tanzania', 'links': [{'ns': 0, 'title': 
        'Administrative divisions of Tanzania'}, {'ns': 0, 'title': 
        'Africa Development'},...
        And so on
        '''
        pages = data["query"]["pages"]

        # loop through the pages. But there should only be one.
        for k, v in pages.items():
            ''' 
            get the value of 'links', a list of dictionaries with two
            keys each: 'ns' and 'title'. We want 'title.' Second
            parameter is an empty list default value in case the key
            'links' is not found.
            '''
            links = v.get("links", [])
            # get the titles of all the links
            for link in links:
                all_links.append(link["title"])

        # Check if there's more data to retrieve
        if 'continue' in data:
            # to avoid making too many requests at once
            sleep(2)
            params.update(data['continue'])  # Update parameters with continuation data
        else:
            break  # Break the loop if there's no more data to retrieve

    return all_links

def clean_up_links(internal_links):
    """ Clean up the list so it only contains articles

    Args:
        internal_links(list[str]): a list of all the internal links
        from a Wikipedia page (or more correctly, a list of titles of
        the linked pages)

    Returns:
        list[str]: a list of all the internal links from a Wikipedia
        page, but with unwanted pages removed (i.e. 'Template:', 'Help:', 
        and 'Portal:' pages) so that we only end up with actual
        articles (or more accurately, article titles)
    """
    # We want to remove titles starting with any of these values
    expression_to_search = "^Wikipedia:|Template:|Template talk:|Help:|Category:|Portal:"
    # Clean up internal_links so it only gives us regular Wikipedia pages
    cleaned_up_links = [ item for item in internal_links if (re.search(expression_to_search, item)) == None]
    return cleaned_up_links

def get_random_link(internal_links):
    """ Gets a random link from the list

    Args:
        internal_links(list[str]): a list of all the internal links
        from a Wikipedia page (or more correctly, a list of titles of
        the linked pages)

    Returns:
        str: a randomly selected article title from the list of
        internal links
    """
    # last_index = len(internal_links) - 1
    # random_index = random.randint(0, last_index)
    # random_link = internal_links[random_index]
    # return random_link
    random_link = random.choice(internal_links)
    return random_link

# next step: write a function to convert user input to a usable title string (capitalize and replace spaces with underscores)
# convert user input to a usable title string
# def make_title_input_usable(user_input):
    # capitalize only capitalizes first word
    # capitalized = user_input.capitalize()

# follow a redirect

def random_list_of_links(internal_links):
    ''' Shuffles a list of links

    Args:
        internal_links(list[str]): a list of all the internal links
        from a Wikipedia page (or more correctly, a list of titles of
        the linked pages)
        
    Returns:
        new_list(list[str]): a randomly shuffled copy of internal_links
    '''
    new_list = internal_links.copy()
    random.shuffle(new_list)
    return new_list

pittsburgh_history_links = get_internal_links('History_of_Utah')
shuffled_links = random_list_of_links(pittsburgh_history_links)
#for link in shuffled_links:
#    print(link)

music_of_eritrea = get_internal_links('Music_of_Russia')
print(random_list_of_links(music_of_eritrea))