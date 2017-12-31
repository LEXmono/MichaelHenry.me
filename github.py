import logging
import os
import requests

logger = logging.getLogger()

# Environment Variables for credentials
github_user = os.environ['GITHUB_USER']
github_api_key = os.environ['GITHUB_API_KEY']


def get_data(url="https://api.github.com", params={},
             headers={}, data={}, auth=(github_user, github_api_key)):
    """Get Data from GitHub

    Args:
        url:        <class 'str'> - API Endpoint.
                    Default: https://api.github.com
        params:     <class 'dict'> - URL Query Parameters
        headers:    <class 'dict'> - URL Headers.
        data:       <class 'dict'> - Request payload.
        auth:       <class 'tuple'> - Auth Parameters.
                    Default: (github_user, github_api_key)

    Returns:
        A requests object if the request was successful, else False
    """
    request = requests.get(
        url, params=params, headers=headers, data=data, auth=auth)
    # Add required GitHub Accept Header.
    headers['Accept'] = 'application/vnd.github.v3+json'
    if request.ok:
        logger.debug("Successfully retrieved data from GitHub.")
        return request
    else:
        logger.error("Error getting data from GitHub. "
                     "{}".format(request.content))
        return False


def get_repos():
    """Get Public Repos from GitHub"""
    url = 'https://api.github.com/user/repos'
    params = {
        'visibility': 'public',
        'sort': 'updated'
    }
    request = get_data(url=url, params=params)
    if request:
        response = request.json()
    else:
        response = [
            {
                'name': "q",
                'html_url': "https://github.com/LEXmono/q",
                'description': 'Q, (standing for Quartermaster), is a job '
                               'title rather than a name. Q is the head of Q '
                               'Branch, the research and development division '
                               'of the British Secret Service MI6. In his '
                               'free time, he patrols, my slack channel '
                               'offering his wisdom and insight to our lives.'
            },
            {
                'name': "HealthDash",
                'html_url': "https://github.com/LEXmono/HealthDash",
                'description': 'Python Health Dashboard to aggregate all of my'
                               ' health information in on place. '
            }
        ]
    return response
